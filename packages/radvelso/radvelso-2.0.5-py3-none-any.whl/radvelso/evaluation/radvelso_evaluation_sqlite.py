#/usr/bin/python3
import os
import tempfile
import numpy as np
import sqlite3
import time 
import glob
import dask
import dask.distributed
from dask.delayed import delayed
import copy
import sys
import datetime
import json
import radvelso
from numpy import save
from os.path import basename,splitext



def create_index_tables_elevation_azimuth(conn):
  """ Create index tables
  args:
    conn          : connextion to sqlite file
  output:
    Nothing
    index tables i sqlite file
 
  """

  order_sql ="""CREATE INDEX 
                  NOMINAL_PPI_ELEVATIONS 
                ON header (NOMINAL_PPI_ELEVATION);"""
  conn.execute(order_sql)

  order_sql ="""CREATE INDEX
                  CENTER_AZIMUTHS 
                ON header (CENTER_AZIMUTH);"""
  conn.execute(order_sql)

def avg_std_all(pathout,
                this_radar,
                start_date,
                end_date,
                number_min_obs,
                setting_average):

  """ STD and AVG for a time series

  This function calculates the STD and AVG for a time series.

  args:
    file_list                : list of json file to joint 
    pathout                  : output json file for a time series per radar and elevation
    this radar               : name of radar to evaluated
    start_date               : start date of the time series
    end_date        :         : end date of the time series

  output:
    This function outputs nothing

  """



  filememory_statistics=f'file:{os.path.basename(pathout)}_{this_radar}?mode=memory&cache=shared'
  print ( filememory_statistics)
  # https://tools.ietf.org/html/rfc3986  Uniform Resource Identifier (URI)
  # The advantage of using a URI filename is that query parameters on the
  # URI can be used to control details of the newly created database connection in parallel
  conn_filememory = sqlite3.connect(filememory_statistics, uri=True, check_same_thread=False)
  conn_filememory.execute("pragma temp_store = 2;")
  conn_filememory.execute("""PRAGMA journal_mode=OFF;""")
  conn_filememory.execute("""PRAGMA synchronous=OFF;""")
  schema = radvelso.find_schema('schema_statistics')
  with open(schema) as f:
                 schema = f.read()
  conn_filememory.executescript(schema)

 
  conn_elevation = sqlite3.connect(pathout)
  order_sql = """ SELECT 
                    distinct nominal_ppi_elevation 
                  FROM
                    header 
                  WHERE
                    id_stn = ?
                  ORDER BY 
                    1;"""
  nominal_ppi_elevations = [ np.round(elev[0],4) for elev in conn_elevation.execute(order_sql, (this_radar,)).fetchall() ]
  conn_elevation.close()


  for nominal_ppi_elevation in nominal_ppi_elevations:

    conn_ppi_db = make_input_ppi_db_statistics(pathout, 
                                               this_radar, 
                                               nominal_ppi_elevation)

                    
    conn_filememory.execute('ATTACH DATABASE "file::memory:?cache=shared" AS db_ppi') 
    
    order_sql =""" select distinct 
                   RANGE 
                 from  
                   db_ppi.header 
                 WHERE
                   abs(nominal_ppi_elevation-?) < .1 order by 1  ;
                   """
    ranges = [ range_[0] for range_ in conn_filememory.execute(order_sql,(nominal_ppi_elevation,)).fetchall() ]
    for rang in ranges:
                   
        order_sql =""" insert into statistics ( 
                    STDOMP,
                    AVGOMP,
                    RANGE,
                    VCOORD,
                    nominal_ppi_elevation,
                    id_stN,
                    Number_obs


                  )
                  select 
                    sqrt((sum((power(AVGompomp_AVGompomp,2)+power(AVGomp,2))*Number_obs)/sum(Number_obs))-(power((sum(AVGomp*Number_obs)/sum(Number_obs)),2))),
                    sum(AVGomp*Number_obs)/sum(Number_obs),
                    RANGE,
                    VCOORD,
                    nominal_ppi_elevation,
                    id_STN,
                    sum(Number_obs)
   
    
                  from 
                    db_ppi.header
                  where 
                    abs(range-?) < .1 ;"""

        conn_filememory.execute(order_sql,(rang,))
  
    conn_filememory.commit()
    conn_filememory.execute("DETACH DATABASE db_ppi")
    conn_ppi_db.close()


  pathfileout=pathout
  try:
      combine_statistics(pathfileout, filememory_statistics)
  except sqlite3.Error as error:
    print("Error while creating a single sqlite file:  {os.path.basename(filememory)}", error)
  conn_filememory.close()




def make_input_ppi_db(filein, 
                      stn, 
                      nominal_ppi_elevation,
                      ):

  """make a separate db for one PPI

   This db is saved in memory and allows quich search of averaging boxes

   args: 
     filein                 : input sqlite file containing many radars and times
     stn                    : radar for this one volume scan
     nominal_ppi_elevation  : nominal elevation

   output: 
     sqlite connection to the created db

  """

  
  # https://tools.ietf.org/html/rfc3986  Uniform Resource Identifier (URI)
  # The advantage of using a URI filename is that query parameters on the
  # URI can be used to control details of the newly created database connection in parallel
  conn_ppi_db = sqlite3.connect("file::memory:?cache=shared",uri=True)
  # off the journal
  conn_ppi_db.execute("""PRAGMA journal_mode=OFF;""")
  # SQLite continues without syncing as soon as it has handed data off to the operating system
  conn_ppi_db.execute("""PRAGMA synchronous=OFF;""")

  schema = radvelso.find_schema('schema')
  with open(schema) as f:
    schema = f.read()
  conn_ppi_db.executescript(schema)
  # improve searches with index tables
  create_index_tables_elevation_azimuth(conn_ppi_db)
#  create_index_tables_idobs_iddata(conn_ppi_db)
  # attach database
  conn_ppi_db.execute("ATTACH DATABASE ? AS db_all", (filein,)) 
  #select headers in desirec PPI
  order_sql = """ INSERT into header 
                  SELECT 
                    * 
                  FROM
                    db_all.header 

                  WHERE
                    id_stn = ?   
                    and round(nominal_ppi_elevation, 1) = ?;"""
  conn_ppi_db.execute(order_sql, (stn, nominal_ppi_elevation))
  #select associated data entries
  order_sql = """ INSERT into data 
                  SELECT
                    * 
                  FROM
                    db_all.data 
                  WHERE
                    id_obs in (SELECT
                                 id_obs 
                               FROM
                                 header);"""
  conn_ppi_db.execute(order_sql)

  conn_ppi_db.commit()

  return conn_ppi_db
def make_input_ppi_db_statistics(filein, 
                      stn, 
                      nominal_ppi_elevation,
                      ):

  """make a separate db for one PPI

   This db is saved in memory and allows quich search of averaging boxes

   args: 
     filein                 : input sqlite file containing many radars and times
     stn                    : radar for this one volume scan
     nominal_ppi_elevation  : nominal elevation

   output: 
     sqlite connection to the created db

  """

  
  # https://tools.ietf.org/html/rfc3986  Uniform Resource Identifier (URI)
  # The advantage of using a URI filename is that query parameters on the
  # URI can be used to control details of the newly created database connection in parallel
  conn_ppi_db = sqlite3.connect("file::memory:?cache=shared",uri=True)
  # off the journal
  conn_ppi_db.execute("""PRAGMA journal_mode=OFF;""")
  # SQLite continues without syncing as soon as it has handed data off to the operating system
  conn_ppi_db.execute("""PRAGMA synchronous=OFF;""")

  schema = radvelso.find_schema('schema_statistics')
  with open(schema) as f:
    schema = f.read()
  conn_ppi_db.executescript(schema)
  # improve searches with index tables
  # create_index_tables_elevation_azimuth(conn_ppi_db)
  #  create_index_tables_idobs_iddata(conn_ppi_db)
  # attach database
  conn_ppi_db.execute("ATTACH DATABASE ? AS db_all", (filein,)) 
  #select headers in desirec PPI
  order_sql = """ INSERT into header 
                  SELECT 
                    * 
                  FROM
                    db_all.header 
                  WHERE
                    id_stn = ?
                    and round(nominal_ppi_elevation, 1) = ? ;"""
  conn_ppi_db.execute(order_sql, (stn, nominal_ppi_elevation))

  conn_ppi_db.commit()

  return conn_ppi_db

def combine(pathfileout, filememory):
 
   
  """ Creating a single sqlite file from multiple sqlite files
 
  args:
    pathfileout   : output averaging  sqlite file 
    filememory    : name of the sqlite file in memory to copy
  output:
    Nothing
    A sqlite file is made with all averaged volume scans
  """

  # write in output averaging  sqlite file 
  conn_pathfileout = sqlite3.connect(pathfileout, uri=True, isolation_level=None, timeout=999)

  # off the journal
  conn_pathfileout.execute("""PRAGMA journal_mode=OFF;""")
  # SQLite continues without syncing as soon as it has handed data off to the operating system
  conn_pathfileout.execute("""PRAGMA synchronous=OFF;""")
  # Wait to read and write until the next process finishes
  # attach the sqlite file in memory for one PPI
  conn_pathfileout.execute("ATTACH DATABASE ? AS this_avg_db;", (filememory,))
  order_sql = """ INSERT into header
                    SELECT
                     *
                    FROM  this_avg_db.header
                    where 
                    AVGompomp_AVGompomp>=0
                    ;"""
  conn_pathfileout.execute(order_sql) 

  conn_pathfileout.commit()
  conn_pathfileout.execute(""" DETACH DATABASE this_avg_db """)
def combine_statistics(pathfileout, filememory):
 
   
  """ Creating a single sqlite file from multiple sqlite files
 
  args:
    pathfileout   : output averaging  sqlite file 
    filememory    : name of the sqlite file in memory to copy
  output:
    Nothing
    A sqlite file is made with all averaged volume scans
  """

  # write in output averaging  sqlite file 
  conn_pathfileout = sqlite3.connect(pathfileout, uri=True, isolation_level=None, timeout=999)

  # off the journal
  conn_pathfileout.execute("""PRAGMA journal_mode=OFF;""")
  # SQLite continues without syncing as soon as it has handed data off to the operating system
  conn_pathfileout.execute("""PRAGMA synchronous=OFF;""")
  # Wait to read and write until the next process finishes
  # attach the sqlite file in memory for one PPI
  conn_pathfileout.execute("ATTACH DATABASE ? AS this_avg_db;", (filememory,))
  order_sql = """ INSERT into statistics
                    SELECT
                     *
                    FROM  this_avg_db.statistics;"""
  conn_pathfileout.execute(order_sql) 


  conn_pathfileout.commit()
  conn_pathfileout.execute(""" DETACH DATABASE this_avg_db """)



def avg_std_one(this_file,
                this_radar,
                number_min_obs,
                pathout,
                setting_average):
  """  STD and AVG for PPI

  This function calculates the STD and AVG for one PPI

  args:
    this_file                : sqlite file where is the PPI
    pathout                  : output json file for a time series 
    
    this_radar               : name of radar to evaluated
    start_date               : start date of the time series
    end_date                 : end date of the time series

  output:
    This function outputs nothing

  """
  

  filememory_statistics=f'file:{os.path.basename(this_file)}_{this_radar}?mode=memory&cache=shared'
  print ( filememory_statistics)
  # https://tools.ietf.org/html/rfc3986  Uniform Resource Identifier (URI)
  # The advantage of using a URI filename is that query parameters on the
  # URI can be used to control details of the newly created database connection in parallel
  conn_filememory = sqlite3.connect(filememory_statistics, uri=True, check_same_thread=False)
  conn_filememory.execute("pragma temp_store = 2;")
  conn_filememory.execute("""PRAGMA journal_mode=OFF;""")
    
  conn_filememory.execute("""PRAGMA synchronous=OFF;""")
  schema = radvelso.find_schema('schema_statistics')
  with open(schema) as f:
                 schema = f.read()
  conn_filememory.executescript(schema)

 

  conn_elevation = sqlite3.connect(this_file)
  order_sql = """ SELECT 
                    distinct nominal_ppi_elevation 
                  FROM
                    header 
                  WHERE
                    id_stn = ?
                  ORDER BY 
                    1;"""
  nominal_ppi_elevations = [ np.round(elev[0],4) for elev in conn_elevation.execute(order_sql, (this_radar,)).fetchall() ]
  conn_elevation.close()

  tc_0 = time.time()

  for nominal_ppi_elevation in nominal_ppi_elevations:

    conn_ppi_db = make_input_ppi_db(this_file, 
                                    this_radar, 
                                    nominal_ppi_elevation)

    
   
    conn_filememory.execute('ATTACH DATABASE "file::memory:?cache=shared" AS db_ppi') 
    
    order_sql =""" select distinct 
                   RANGE 
                 from  
                   db_ppi.data order by 1 ;"""
    ranges = [ range_[0] for range_ in conn_filememory.execute(order_sql).fetchall() ]
    for rang in ranges:
      # STDEV = SQRT( round(((sum(omp)*sum(omp) - sum(omp * omp))/((count(*)-1)*(count(*)))),3))
      # STDEV = SQRT( AVG(omp*omp) - AVG(omp)*AVG(omp))
      order_sql =""" insert into header( 
    
                    DATE, TIME, AVGompomp_AVGompomp,AVGomp, RANGE,  VCOORD,  Number_obs ,ID_STN, NOMINAL_PPI_ELEVATION

                  )
                  select 
                    DATE, TIME, SQRT( (sum(omp*omp)/count(*)) - AVG(omp)*AVG(omp)), avg(omp), range, vcoord, count(*), ID_STN, NOMINAL_PPI_ELEVATION
    
                  from 
                    db_ppi.header natural join db_ppi.data 
                  where 
                    abs(range-?) < .1 
                    and (nominal_ppi_elevation-?)<.1 
                    and NYQUIST > 30. 
                    and id_stn= ?;"""
      
      conn_filememory.execute(order_sql,(rang,nominal_ppi_elevation,this_radar ))
   
   
    conn_filememory.commit()
    conn_filememory.execute("DETACH DATABASE db_ppi")
    conn_ppi_db.close()
 
  pathfileout=pathout
  try:
      combine(pathfileout, filememory_statistics)
  except sqlite3.Error as error:
    print("Error while creating a single sqlite file:  {os.path.basename(filememory)}", error)
  # close connection 
  conn_filememory.close()


  tc_1 = time.time()
        

def main(start_date,
         end_date,
         desired_radar_list,
         infile_list, 
         pathoutwork, 
         n_cpus,
         setting_average,
         model):
  """launch computation of std and avg omp for time series  possibly in parallel

   args:
     start_date:     start time of time series
     end_date  :     end   time of time series
     radar_list:     list of radars to process
     infile_list:    input sqlite file to average
     pathout:        where json  files will be put
     n_cpus:         number of rays for averaging
 
  output:
    Nothing

  """
  from termcolor import colored
  #################################################################################################
  # launch evaluation_one_6h: STD and AVG for all PPI in a time series
  #################################################################################################
  tc_0 = time.time()
  evaluation_one_6 = True
  evaluation_one_6_clobber = False
  number_min_obsforaverage = [1]
  #number_min_obsforaverage = [1]
  import shutil 
  pathout_serie=f"{pathoutwork}/series_{start_date.strftime('%Y%m%d%H')}_{end_date.strftime('%Y%m%d%H')}/"
  if not os.path.isdir(pathout_serie):
      os.makedirs(pathout_serie)

  pathout_serie_sqlite=f"{pathoutwork}/series_{start_date.strftime('%Y%m%d%H')}_{end_date.strftime('%Y%m%d%H')}/sqlite_{start_date.strftime('%Y%m%d%H')}_{end_date.strftime('%Y%m%d%H')}"
  if os.path.isfile(pathout_serie_sqlite):
    os.remove(pathout_serie_sqlite)
  #init large output file
 # print (pathout_serie_sqlite)
  conn_pathfileout = sqlite3.connect(pathout_serie_sqlite)
  conn_pathfileout.execute("pragma temp_store = 2;")
  schema =radvelso.find_schema('schema_statistics')
  with open(schema) as f:
    schema = f.read()
  conn_pathfileout.executescript(schema)
  conn_pathfileout.close


  if evaluation_one_6:
   if evaluation_one_6_clobber:
     print ("remove do evaluation_one_6")
     if os.path.isdir(pathout_serie):
        shutil.rmtree(pathout_serie)
   if not os.path.isdir(pathout_serie):
      os.makedirs(pathout_serie)
    # make list of files, radars and times that will be processed in parallel
   infile_list.sort()

   tc_00 = time.time()

   for this_file in infile_list:
        this_date = datetime.datetime.strptime(os.path.basename(this_file)[0:10], '%Y%m%d%H')
        vol_scan_list = []
        tc_0 = time.time()
        with sqlite3.connect(this_file) as conn_loops:
          conn_loops.execute("pragma temp_store = 2;")
          conn_loops.execute("""PRAGMA journal_mode=OFF;""")
          conn_loops.execute("""PRAGMA synchronous=OFF;""")

          try:
             conn_loops.execute("CREATE INDEX times on header (time);")
          except:
           pass
          try:
             conn_loops.execute("CREATE INDEX reles on header (NOMINAL_PPI_ELEVATION);")
          except:
            pass
          try: 
             conn_loops.execute("CREATE INDEX radar on header (ID_STN);")
          except:
            pass

          # list of radars in the file
          order_sql = """select distinct
                           ID_STN 
                         from 
                           header order by 1;"""

         
          avail_radar_list  = [ stn[0] for stn in conn_loops.execute(order_sql).fetchall() ]

          for this_radar in avail_radar_list:


            if desired_radar_list != 'all':
                 if this_radar not in desired_radar_list:
                    continue
                  
            for number_min_obs in number_min_obsforaverage:
            
                  #pathout_serie_number_min_obs=f"{pathout_serie}/{this_radar}/"#elevation_{round(this_elevation,1)}/number_min_obs_average_{number_min_obs}_{setting_average}/"
                 # if not os.path.isdir(pathout_serie_number_min_obs):
                  #  os.makedirs(pathout_serie_number_min_obs)
                  vol_scan_list.append( {'file':this_file, 
                                         'radar':this_radar,
                                         'number_min_obs':number_min_obs,
                                         'setting_average': setting_average})
                     
                 # print (this_file,this_radar)

          print ("launch vg_std_one: STD and AVG for all PPI in a time series")

          if n_cpus == 1:
           #serial execution, usefull for debugging
           for vscan in vol_scan_list:
             avg_std_one(vscan['file'], vscan['radar'], vscan['number_min_obs'],  pathout_serie_sqlite, vscan['setting_average']) 
          else:
           print (colored(f'Computed {len(vol_scan_list)} PPI in parallel ', 'green'))
           with tempfile.TemporaryDirectory() as tmpdir:
             #the directory dask-worker-space/ will be in tmpdir
             dask.config.set({'distributed.comm.timeouts.connect': '20s'})
             with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                         n_workers=n_cpus, 
                                       local_directory=tmpdir, 
                                       silence_logs=40) as client:
               #delay data 
               joblist = [delayed(avg_std_one)(vscan['file'], vscan['radar'], vscan['number_min_obs'],
                                            pathout_serie_sqlite, vscan['setting_average']) for vscan in vol_scan_list]
               dask.compute(joblist)
           tc_1 = time.time()
           print(f"Runtime list  total: {round(tc_1-tc_0,4)} s")


       # file_control=np.append(file_control, this_file)
       # save(f'file_control_radvelsoe/file_control_{desired_radar_list}_{setting_average}', file_control)



 
  tc_3 = time.time()
  print(f"Runtime total: {round(tc_3-tc_00,4)} s")


  #################################################################################################
  # launch avg_std_all:  STD and AVG for time series
  #################################################################################################
  tc_0 = time.time()
  evaluation_all_one_6= True
  evaluation_all_one_6_clobber=False
  pathout_plot = f"{pathoutwork}/plot_{start_date.strftime('%Y%m%d%H')}_{end_date.strftime('%Y%m%d%H')}"
  if evaluation_all_one_6:

    if evaluation_all_one_6_clobber:

      if os.path.isdir(pathout_plot):
        shutil.rmtree(pathout_plot)
    file_list = []
    for number_min_obs in number_min_obsforaverage:
     
     
      avail_radar_list  = [ stn[0] for stn in conn_loops.execute(order_sql).fetchall() ]
      for this_radar in avail_radar_list:

        if desired_radar_list != 'all':
          if this_radar not in desired_radar_list:
             continue
      
       # ppi_list = glob.glob(f'{pathout_serie}/{this_radar}/*')
       # for this_ppi in ppi_list:


        file_list.append( {'pathout': pathout_serie_sqlite,'radar':this_radar,'start_date':start_date,'end_date':end_date,'number_min_obs':number_min_obs, 'setting_average': setting_average})
      # avg_std_all
      if n_cpus == 1:

        #serial execution, usefull for debugging
        for ppi in file_list:
          avg_std_all( ppi['pathout'], ppi['radar'], ppi['start_date'],ppi['end_date'],ppi['number_min_obs'], ppi['setting_average'] ) 
      else: 
        print (colored(f'Computed {len(file_list)} VS in parallel for time serie (N_OBS ={number_min_obs})', 'green'))
        with tempfile.TemporaryDirectory() as tmpdir:
          #the directory dask-worker-space/ will be in tmpdir
          dask.config.set({'distributed.comm.timeouts.connect': '20s'})
          with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                     n_workers=n_cpus, 
                                     local_directory=tmpdir, 
                                     silence_logs=40) as client:

            #delay data 
            joblist = [delayed(avg_std_all)(ppi['pathout'], ppi['radar'], ppi['start_date'], ppi['end_date'], ppi['number_min_obs'], ppi['setting_average']) for ppi in file_list]
            dask.compute(joblist)


    # close connection 
  order_sql = """INSERT into info(name) values(?);"""
  conn_pathfileout = sqlite3.connect(pathout_serie_sqlite, uri=True, isolation_level=None, timeout=999)
  conn_pathfileout.execute( order_sql, (setting_average,))
  conn_pathfileout.commit()
  conn_pathfileout.close()
  tc_1 = time.time()
  print(f"Runtime otal: {round(tc_1-tc_0,4)} s")


def arg_call():

  import argparse 

  parser = argparse.ArgumentParser()
  parser.add_argument('--start_date',   default='undefined', type=str,  help="YYYYMMDDHH start time of time serie")
  parser.add_argument('--end_date',     default='undefined', type=str,  help="YYYYMMDDHH end   time of time serie")
  parser.add_argument('--radar_list', nargs="+", default='all',         help="List of radars to process")
  parser.add_argument('--inputfiles', nargs="+",   default='undefined', type=str,   help="input sqlite file to average")
  parser.add_argument('--pathin',       default='undefined', type=str,  help="directory where are input sqlite files")
  parser.add_argument('--pathout',      default=os.getcwd(), type=str,  help="where json  files will be put")
  parser.add_argument('--n_cpus',       default=3,           type=int,  help="Number of rays for averaging" )
  parser.add_argument('--averaged',     default='undefined', type=str,  help="setting for averaged" )
  parser.add_argument('--model',       default='HRDPS', type=str,  help="setting for averaged" )

  args = parser.parse_args()
  if args.inputfiles == 'undefined' and args.pathin == 'undefined':
    args.start_date  = '2019061500'
    args.end_date    = '2019071500'

    args.window_width = 6
    #option1: explicitely specify inputfiles
    #args.inputfiles = ['/space/hall4/sitestore/eccc/cmd/a/dlo001/data/doppler_qc/doppler_qc_v0.3/sqlite_v1.0.0_qc/split_6h/USVNX/2019073100_ra',
    #                   '/space/hall4/sitestore/eccc/cmd/a/dlo001/data/doppler_qc/doppler_qc_v0.3/sqlite_v1.0.0_qc/split_6h/CASRA/2019073100_ra']
    #option2: specify pathin + infile_struc and let Python search for files
    #full path of radvelso module
    radvelso_dir = os.path.dirname(radvelso.__file__)
    #root path of radvelso package (one dir up from radvelso module)
    package_dir = os.path.dirname(radvelso_dir)
    #full path of schema we are looking for
    args.pathin = f'{package_dir}/test_data/evaluation'
    args.averaged = '50%_bgck2'
    args.pathin = f'/home/dlo001/data_maestro/eccc-ppp3/maestro_archives/HR900E19_N10_R10km_bgck2/banco/bgckalt/'
   # args.pathin = f'test'

   # args.pathin = f'/fs/homeu1/eccc/cmd/cmda/dlo001/RADAR/radvelso/radvelso/evaluation/test_trials/'
   # args.pathin = '/fs/homeu1/eccc/cmd/cmda/dlo001/RADAR/radvelso/radvelso/evaluation/tt/'
   # args.pathin = '/home/dlo001/data_maestro/eccc-ppp3/maestro_archives/RADAR/banco/bgckalt/'
    args.pathout = './radvelsoe_bgck2'
  #  args.radar_list = 'casbv'  
    args.radar_list = 'all'
  #  args.radar_list = 'casbv' /home/dlo001/data_maestro/eccc-ppp3/maestro_archives/HDJA900E19DLO_N10_R10km/banco/bgckalt/
    args.timing = False
    args.n_cpus = 40
    print(f'superobs called with no input filename(s)')
    print(f'We are running demo with:')
    for arg in vars(args):
      print(f'--{arg}  {getattr(args, arg)}')

  #argument checking

  if args.start_date == 'undefined':
      raise ValueError('Start date must be provided')
  else:
     args.start_date = datetime.datetime.strptime(args.start_date, '%Y%m%d%H')
 
  if args.end_date == 'undefined':
      raise ValueError('End date must be provided')
  else:
     args.end_date = datetime.datetime.strptime(args.end_date, '%Y%m%d%H')
 
  if args.inputfiles != 'undefined':
    #if inputfiles argument is provided, we use that
    infile_list = args.inputfiles 

  elif args.pathin != 'undefined': 
    #alternatively, search for files with pathin+infile_struc 
    if not os.path.isdir(args.pathin):
      raise ValueError(f'pathin: {args.pathin} does not exist.')
    infile_list = glob.glob(f'{args.pathin}/*')
  else:
    raise ValueError('At least one of inputfiles ot pathin must be provided')

  #check infile_list
  if len(infile_list) == 0:
    raise ValueError('infile_list is empty, we stop here')

  else:
    for this_file in infile_list:
      if not os.path.isfile(this_file):
        raise ValueError(f'inputfiles: {this_file} does not exist.')
  if not os.path.isdir(args.pathout):
    os.mkdir(args.pathout)
  #sys.exit is used to the return status of main is catched and passed to caller
  sys.exit(main(args.start_date,
                args.end_date,
                args.radar_list,
                infile_list, 
                args.pathout,
                args.n_cpus,
                args.averaged,
                args.model))

if __name__ == '__main__':
    arg_call()
