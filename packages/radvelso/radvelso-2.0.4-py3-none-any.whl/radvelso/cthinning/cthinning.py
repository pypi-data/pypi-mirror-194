#!/usr/bin/python3

import os
import tempfile
import argparse 
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
import radvelso
import scipy.spatial
import domutils.radar_tools as radar_tools
import domutils.geo_tools as geo_tools
from collections import Counter
#from pathlib import Path

from pathlib import Path
import domcmc.fst_tools as fst_tools

def make_input_db(filein, this_time):

    """make a separate db oneintervale of time
  
    This db is saved in memory and allows quich search of observation
  
    args: 
    ---------------
    
    filein                 : input sqlite file containing many radars and times
    this_time              : end time of this one volume san
    
    output:
    ----------------

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
  
    schema = radvelso.qcavg.find_schema('schema')
    with open(schema) as f:
        schema = f.read()
    conn_ppi_db.executescript(schema)
    # improve searches with index tables
    radvelso.qcavg.create_index_tables_elevation_azimuth(conn_ppi_db)
    radvelso.qcavg.create_index_tables_idobs_iddata(conn_ppi_db)
    # attach database
    conn_ppi_db.execute("ATTACH DATABASE ? AS db_all", (filein,)) 
    #select headers in desirec PPI
    order_sql = """ INSERT into header 
                    SELECT 
                      * 
                    FROM
                      db_all.header 
                    WHERE
                      time = ? 
                      ;"""
    conn_ppi_db.execute(order_sql, ( this_time,))
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
                                   header  );"""
    conn_ppi_db.execute(order_sql)
  
    conn_ppi_db.commit()
  
    return conn_ppi_db
  
def create_info_midas_tables(filein,conn_pathfileout):

    """ Create header entry
    A header is created matching a bunch of entries in data table
  
    args:
    ----------------

    filein        : input sqlite file with raw data
    conn_pathfileout  : connextion to output file
    
    output:
    ----------------

    Nothing
      info table entry is written in output sqlite file
    
    """
    
    conn_pathfileout.execute("""ATTACH DATABASE ? AS db_all""", (filein,) ) 
  
    # Info table
    order_sql ="""CREATE TABLE info( NAME, DESCRIPTION, UNIT );"""
    conn_pathfileout.execute( order_sql)
    order_sql =""" INSERT  into  info (
                     NAME, DESCRIPTION, UNIT) 
                   SELECT * 
                     from  db_all.info """
    conn_pathfileout.execute( order_sql)
  
  
    # Resume table 
    order_sql ="""CREATE TABLE resume(date integer , time integer , run varchar(9));"""
    conn_pathfileout.execute( order_sql)
  
    order_sql = """INSERT into resume (
                      date, time, run) 
                    SELECT * 
                     from  db_all.resume """
    conn_pathfileout.execute( order_sql)
    
    # rdb4_schema table
    order_sql ="""CREATE TABLE rdb4_schema( schema  varchar(9) );"""
    conn_pathfileout.execute( order_sql)
    order_sql ="""INSERT into rdb4_schema (
                   schema)
                  SELECT *   
                     from  db_all.rdb4_schema  """
    conn_pathfileout.execute( order_sql)
  
    # commint and detach database
    conn_pathfileout.commit()
    conn_pathfileout.execute("DETACH DATABASE db_all")

def getHfromRange(beamRange, radarAltitude, beamElevation):
    
    """Computation of height of the radar beam
              from range of the radar beam
    args:
    ----------------
    
    beamRange: range in radar beam for observation
    radarAltitude: radar antenna altitude
    beamElevation: radar beam elevation
    
    output:
    ----------------

    beamHeight: the altitude from the given range
    
    """

    ec_wgs_R2 = radvelso.qcavg.dict_constans()['approximate_radius_of_earth']
    #! effective radius of the earth
    Re = ec_wgs_R2*(4./3.)
    #! height of radar beam  from range at beamElevation and radarAltitude 
    beamHeight = np.sqrt(beamRange**2.+(Re+radarAltitude)**2.+2.*beamRange*(Re+radarAltitude)*np.sin(np.radians(beamElevation)))-(Re)

    return  beamHeight 

def couple_interval_height(Height_interval, Height_test1, Height_test2, indsort):
    
    """Given a couple, calculate the height interval to apply the horizontal thinning.

    args:
    ----------------

    Height_interval: vertical thinning intervals
    Height_test1: altitude of the first member of the pair
    Height_test2:altitude of the second  member of the pair
    indsort: index in descending order as a function of the distance between the 
                     observation pair originating from different radar.

    output:
    ----------------
             
    max(values) and  min(values): maximum altitude value and minimum altitude value of 
             the layer where the horizontal thinning will be applied for that pair of observations 
             from the different radar.

    """
    
    id_height_top1    = np.where(Height_interval>Height_test1[indsort])[0]
    id_height_bottom1 = np.where(Height_interval<Height_test1[indsort])[0][::-1]
    id_height_top2    = np.where(Height_interval>Height_test2[indsort])[0]
    id_height_bottom2 = np.where(Height_interval<Height_test2[indsort])[0][::-1]
    values = [Height_interval[id_height_top1[0]], Height_interval[id_height_top2[0]] ,Height_interval[id_height_bottom1[0]], Height_interval[id_height_bottom2[0]]]
  
    return max(values), min(values)

def obs_interval_height(Height_interval, Height_obs):

    """Given a obs, calculate the height interval to apply the horizontal thinning.

    args:
    ----------------
           
    Height_interval: vertical thinning intervals
    Height_obs: altitude of the observation

    output:
    ----------------
    max(values) and  min(values): maximum altitude value and minimum altitude value of 
               the layer where the horizontal thinning will be applied

    """
  
    id_height_top    = np.where(Height_interval>Height_obs)[0]
    id_height_bottom = np.where(Height_interval<Height_obs)[0][::-1]
    values = [Height_interval[id_height_top[0]], Height_interval[id_height_bottom[0]]]
  
    return max(values), min(values)

def get_obs_from_interval_time(conn_filein, conn_filememory, filein, startdate, enddate):

    """ Copies in memory only the observations to be processed in the required time interval
         
    args:
    ----------------

    conn_filein: connection to initial sqlite file
    conn_filememory: memory connection
    filein: qlite file
    startdate: start date to use observation
    enddate: final date to use observation
    
    output:
    ----------------

    obs have been copied into memory for your use.
    """
   
    result = conn_filein.execute(f"select distinct DATE, printf('%06d', TIME) from header;").fetchall()
    datetime_list  = [datetime.datetime.strptime(f'{date_time[0]}{date_time[1]}', '%Y%m%d%H%M%S') for date_time in result]
    datetime_list.sort()
    conn_filein.close()
  
    for this_datetime in datetime_list:

        if (this_datetime > startdate) and (this_datetime <= enddate):
            #zero padded string 020100
            hhmiss_pad =  this_datetime.strftime('%H%M%S') 
            #no zeros on left but still 0 if 000000
            hhmiss_nopad = str(int(hhmiss_pad))
  
            conn_ppi_db = make_input_db(filein, hhmiss_nopad)
  
            #temporarily attach ppi db to output file
            conn_filememory.execute('ATTACH DATABASE "file::memory:?cache=shared" AS conn_ppi_db') 
            order_sql = """ INSERT into header
                          SELECT
                           *
                          FROM conn_ppi_db.header;"""
            conn_filememory.execute(order_sql) 
            order_sql = """ INSERT into data
                          SELECT
                            *
                          FROM conn_ppi_db.data;"""
            conn_filememory.execute(order_sql)
  
            conn_filememory.commit()
            conn_filememory.execute(""" DETACH DATABASE conn_ppi_db """)
  
            conn_ppi_db.close()

def make_dict_of_obs(conn_filememory,model_lons,model_lats):
    
    """ Makes a dictionary with the information from the observations involved in thinning
         
    args:
    ----------------
    conn_filememory: memory connection
    model_lons: longitudes of each pixes of the model
    model_lats: latitudes of each pixes of the model
        
    output:
    ----------------
     
    dict_obs: dictionary with the information from the observations involved in thinning

    """

    # Should this be done at the moment of reading the model grid? 
    # this computation would not have to be repeated for each parallel task

    # to know the closest pixel of each observation to the model
    source_xy = np.transpose(np.vstack((model_lons.ravel(),model_lats.ravel())))
    kdtree = scipy.spatial.cKDTree(source_xy, balanced_tree=False)
  
    c = conn_filememory.cursor()
    c.row_factory = sqlite3.Row


    query = ("""select
                   ID_OBS, LAT, LON, ANTENNA_ALTITUDE, 
                   CENTER_ELEVATION, CENTER_AZIMUTH, DATE, TIME, ID_STN 
                 from header
                 ORDER BY id_obs ASC;""")
    c.execute(query)
    header_entries = c.fetchall()
  
    #numpy arrays and lists are two very different thing in Python. 
    #appending to either takes a while. There is probably a better way to do this. 
    
   
    query = ("""select
                   count(*)                   
                from data ;""")
    c.execute(query)
    all_data_entries = c.fetchone()


    # initialitation list
    np_indices    = np.zeros(all_data_entries[0], int)
    np_id_data    = np.zeros(all_data_entries[0], int)
    np_id_stn     = np.empty(all_data_entries[0], dtype=object)
    np_obs_lats   = np.zeros(all_data_entries[0])
    np_obs_lons   = np.zeros(all_data_entries[0])
    np_beamHeight = np.zeros(all_data_entries[0])
    
    # initialization positio in np
    ii = 0
    for header_entry in header_entries:
        query = (  f'select RANGE, OMP, OMA, ID_DATA, VCOORD  from data where ( id_obs = ? ) ORDER BY id_obs ASC ;')
        c.execute(query, (header_entry['ID_OBS'],))
        data_entries = c.fetchall()

        beamElevation  = header_entry['CENTER_ELEVATION']
        beamAzimuth    = header_entry['CENTER_AZIMUTH']
        radarAltitude  = header_entry['ANTENNA_ALTITUDE']
        radar_lon = header_entry['LON']
        radar_lat = header_entry['LAT']
        for data_entry in data_entries:
            this_range   = data_entry['RANGE']
            this_id_datas = data_entry['ID_DATA']
            this_beamHeight = getHfromRange(data_entry['RANGE'], radarAltitude, beamElevation)
                           
            dist_earth = radar_tools.model_43(elev=beamElevation, dist_beam=this_range/1e3, hrad=radarAltitude/1e3, want='dist_earth')
            lons, lats = geo_tools.lat_lon_range_az(radar_lon ,radar_lat, dist_earth, beamAzimuth)
            #lons int the interval 0 - 360)
            lons = np.where(lons < 0., lons + 360., lons)
            #index kdtree to know pixel of model for observation
            dest_xy = np.transpose(np.vstack((lons, lats)))
            # indices plural but only one result
            _, this_index = kdtree.query(dest_xy, k=1)
            # indices plural for a single index is confusing
            np_indices[ii]    = this_index
            np_id_data[ii]    = this_id_datas
            np_id_stn[ii]     = header_entry['id_stn']
            np_obs_lats[ii]   = lats
            np_obs_lons[ii]   = lons
            np_beamHeight[ii] = this_beamHeight
            # increase positio in np 
            ii += 1

    # make dict  
    dict_obs = {'indices' : np_indices, 
                'id_data' : np_id_data, 
                'id_stn'  : np_id_stn,
                'obs_lats': np_obs_lats,
                'obs_lons': np_obs_lons,
                'beamHeight': np_beamHeight}
    return dict_obs

def get_couple_thinning( dict_obs, 
                         delta_distance_neighbours_m,
                         delta_height_vertical_m,
                         delta_distance_couple_m,
                         list_id_data_save_couples, 
                         list_id_data_remove_thinning):

    """ Applies horizontal thinning to the different vertical intervals for couples observations 
    
    arg:
    ----------------
    dict_obs: dictionary with the information from the observations involved in thinning
    delta_distance_neighbours_m: min distance neighbours (m)
    delta_height_vertical_m:delta distance for vertical interval (m)
    delta_distance_couple_m: min distance for couple of different radars is considered (m)

    list_id_data_save_couple: id_data list for the observation couples of different radar saved
    list_id_data_save_thinning: id_data list of observations saved and are not couples of different radar
    list_id_data_remove_thinning: id_data list of observations flagged as not assimilable
    
    output:
    ------------------------
    update list_id_data_save_couple

                       _thinning    
                       _remove_thinning
    """


    # get vertical interval to make horizontal thinning
    height_interval = list(np.arange(0, int(max(dict_obs['beamHeight'])+delta_height_vertical_m), delta_height_vertical_m))
    counts = Counter(dict_obs['indices'])
    list_unique_indices =  [id for id in dict_obs['indices'] if counts[id] > 1]
    # It will remove the duplicates.
    list_unique_indices = np.unique(list_unique_indices) 

    id_save1 = np.array(())
    id_save2 = np.array(())
    distance = np.array(())

    # check model tiles sharing multiple radar observations
    for unique_indices in list_unique_indices:
        # again please use nonzero
        inds = np.nonzero(dict_obs['indices'] == unique_indices)
        couple_obs1  = np.array((),int)
        couple_obs2  = np.array((),int)
        distance_test = np.array(())
        height_test1 = np.array(()) 
        height_test2 = np.array(())
        if (len(Counter(dict_obs['id_stn'][inds]))) > 1:
            for ind1 in inds[0]:
                for ind2 in inds[0]:
                    if (dict_obs['id_stn'][ind1] != dict_obs['id_stn'][ind2]):
                        lat1 = dict_obs['obs_lats'][ind1]
                        lon1 = dict_obs['obs_lons'][ind1]
                        lat2 = dict_obs['obs_lats'][ind2]
                        lon2 = dict_obs['obs_lons'][ind2]
                        dista = radvelso.qcavg.distance_between_two_points(lat1, lon1, lat2, lon2)
                        if dista < delta_distance_couple_m:
                            distance_test = np.append(distance_test, dista)
                            couple_obs1 = np.append( couple_obs1, dict_obs['id_data'][ind1])   
                            couple_obs2 = np.append( couple_obs2, dict_obs['id_data'][ind2]) 
                            # why a capital letter here?
                            height_test1 = np.append( height_test1, dict_obs['beamHeight'][ind1]) 
                            height_test2 = np.append( height_test2, dict_obs['beamHeight'][ind2]) 
         
        indssort = np.argsort( distance_test)    
        # best couple in pixel
        for indsort in  indssort:
            if (couple_obs1[indsort] in list_id_data_save_couples) or (couple_obs2[indsort] in list_id_data_save_couples):
                continue
            if (couple_obs1[indsort] in list_id_data_remove_thinning) or (couple_obs2[indsort] in list_id_data_remove_thinning):
                continue
    
            list_id_data_save_couples = np.append(list_id_data_save_couples, couple_obs1[indsort])
            list_id_data_save_couples = np.append(list_id_data_save_couples, couple_obs2[indsort])
            
            max_height, min_height =couple_interval_height(height_interval, height_test1, height_test2, indsort)
            indx = np.where(np.logical_and(dict_obs['beamHeight'] >= min_height, dict_obs['beamHeight'] < max_height)) 
            index = np.where(dict_obs['id_data'] == couple_obs1[indsort])
           
            
    
            lat = dict_obs['obs_lats'][index[0][0]]
            lon = dict_obs['obs_lons'][index[0][0]] 
            
            # Loop  index in Height interval
            for id1  in range(0,len(indx[0])):
                ind1= indx[0][id1]
                if dict_obs['id_data'][ind1] in list_id_data_remove_thinning:
                    continue
                if dict_obs['id_data'][ind1] in list_id_data_save_couples:  
                    continue
                lat_neighbor = dict_obs['obs_lats'][ind1]
                lon_neighbor = dict_obs['obs_lons'][ind1]   
                distance = radvelso.qcavg.distance_between_two_points(lat, lon, lat_neighbor, lon_neighbor)
                if distance > delta_distance_neighbours_m:
                    continue
                list_id_data_remove_thinning = np.append(list_id_data_remove_thinning, dict_obs['id_data'][ind1])
        
    return list_id_data_save_couples, list_id_data_remove_thinning


def get_all_thinning(dict_obs, 
                     delta_distance_neighbours_m,
                     delta_height_vertical_m,
                     delta_distance_couple_m,
                     list_id_data_save_couples,
                     list_id_data_save_thinning,
                     list_id_data_remove_thinning,
                     kdtree):
 
    """ Applies horizontal thinning to the different vertical intervals for all observations in memory 
    
    arg:
    ----------------
    dict_obs: dictionary with the information from the observations involved in thinning
    delta_distance_neighbours_m: min distance neighbours (m)
    delta_height_vertical_m:delta distance for vertical interval (m)
    delta_distance_couple_m: min distance for couple of different radars is considered (m)

    list_id_data_save_couple: id_data list for the observation couples of different radar saved
    list_id_data_save_thinning: id_data list of observations saved and are not couples of different radar
    list_id_data_remove_thinning: id_data list of observations flagged as not assimilable
    
    output:
    ------------------------
    update list_id_data_save_couples
                            _thinning    
                            _remove_thinning
    """

    # get vertical interval to make horizontal thinning
    Height_interval = list(np.arange(0, int(1.3*max(dict_obs['beamHeight'])), delta_height_vertical_m))
  
    # thinning
    for h in range(0,len(Height_interval)-1):
        min_height = Height_interval[h]
        max_height = Height_interval[h+1]
        indx = np.where(np.logical_and( dict_obs['beamHeight'] >= min_height, dict_obs['beamHeight'] < max_height)) 
        list_id_data_height = dict_obs['id_data'][indx]
        for id_data  in list_id_data_height:
            if id_data in list_id_data_remove_thinning:
                continue
            if id_data in list_id_data_save_couples:  
                continue
            if id_data in list_id_data_remove_thinning:
                continue
            list_id_data_save_thinning = np.append(list_id_data_save_thinning, id_data)
            index = np.where(dict_obs['id_data'] == id_data)[0][0]
            lats = dict_obs['obs_lats'][index]
            lons = dict_obs['obs_lons'][index]
            Height_obs = dict_obs['beamHeight'][index]
            max_height, min_height = obs_interval_height(Height_interval, Height_obs)
             
            dest_xy = np.transpose(np.vstack((lons, lats)))
            _ , indicess = kdtree.query(dest_xy,k=100)
            
            indicess = np.unique(indicess)
            lonlat = kdtree.data[indicess[:-1]]
            for index, lonlat in enumerate(lonlat):
                lat_neighbor = lonlat[1]
                lon_neighbor = lonlat[0]
                distance_mx = radvelso.qcavg.distance_between_two_points(lats, lons, lat_neighbor, lon_neighbor)
                indx = np.where(np.logical_and( dict_obs['obs_lats'] == lat_neighbor,  dict_obs['obs_lons'] == lon_neighbor))[0][0]
                id_data_neighbor = dict_obs['id_data'][indx]
                h_ref = dict_obs['beamHeight'][indx]
                distance_m= np.sqrt(distance_mx**2+h_ref**2)  
                if list_id_data_height is not dict_obs['id_data']:
                    continue
                if id_data_neighbor  in list_id_data_remove_thinning:
                    continue
                if id_data_neighbor  in list_id_data_save_couples: 
                    continue
                if distance_m > delta_distance_neighbours_m: 
                    continue
                if id_data_neighbor in list_id_data_save_thinning:
                    continue
                list_id_data_remove_thinning = np.append(list_id_data_remove_thinning, id_data_neighbor)
    return list_id_data_save_couples, list_id_data_save_thinning,list_id_data_remove_thinning

def thinning(pathfileout,
             filein, 
             startdate,
             enddate,
             delta_distance_neighbours_m,
             delta_height_vertical_m,
             delta_distance_couple_m,
             model_lats,
             model_lons,
             timer=False):

    """ Average  a volume scan
    
    This function takes in raw measurements in an sqlite file and 
    creates an average volume scan based on the content of the 
    provided averaging structure. 
  
    args:
    ----------------
    filein        : input sqlite file with raw data
    this_datetime : vdistance_between_two_points(alid date time of radar observation 
    pathfileout   : output averaging  sqlite file 
    ray_list      : averaging template containing info for how to average PPIs
    ops_run_name  : name of operational run 
    timer         : activation of time analysis, only the first PPI in a volume scan will be averaged
  
    output:
    ----------------
    This function outputs nothing
    However, the thinning data is put in a sqlite file
  
    """ 
  
    #Prepare file in memory
    filememory=f'file:{os.path.basename(filein)}_{startdate}_{enddate}?mode=memory&cache=shared'
    print(filememory)
  
    #print(f'Averaging volume scan for radar {stn} at time {hhmiss_pad} into {os.path.basename(filememory)}')
    conn_filememory = sqlite3.connect(filememory, uri=True, check_same_thread=False)
    # off the journal
    conn_filememory.execute("""PRAGMA journal_mode=OFF;""")
    # SQLite continues without syncing as soon as it has handed data off to the operating system
    conn_filememory.execute("""PRAGMA synchronous=OFF;""")
  
    schema = radvelso.qcavg.find_schema('schema')
    with open(schema) as f:
        schema = f.read( )
    conn_filememory.executescript(schema)
    conn_filein = sqlite3.connect(filein)
  
  
    # get observation for the width of time 
    get_obs_from_interval_time(conn_filein, conn_filememory, filein, startdate, enddate)
    
    dict_obs = make_dict_of_obs(conn_filememory,model_lons,model_lats)
   
    # initialization the id_data list for the observation couples of different radar saved
    list_id_data_save_couples = np.array((),int)
    # initialization the id_data list of observations saved and are not couples of different radar
    list_id_data_save_thinning = np.array((),int)
    # initialization the id_data list of observations flagged as not assimilable
    list_id_data_remove_thinning = np.array((),int)

    #check number observation 
    if len(dict_obs['beamHeight'])>0:

        # lets agree for 4 spaces increments for nesting

        # Having the same variables for input and output is possible but very unusual

       #  kdtree
        source_xy = np.transpose(np.vstack((dict_obs['obs_lons'].ravel(), dict_obs['obs_lats'].ravel())))
        kdtree = scipy.spatial.cKDTree(source_xy, balanced_tree=False)

        
        (list_id_data_save_couples, 
         list_id_data_remove_thinning) = get_couple_thinning(dict_obs, 
                                                             delta_distance_neighbours_m,
                                                             delta_height_vertical_m,
                                                             delta_distance_couple_m,
                                                             list_id_data_save_couples, 
                                                             list_id_data_remove_thinning)
        (list_id_data_save_couples, 
         list_id_data_save_thinning, 
         list_id_data_remove_thinning) = get_all_thinning(dict_obs, 
                                                          delta_distance_neighbours_m,
                                                          delta_height_vertical_m,
                                                          delta_distance_couple_m,
                                                          list_id_data_save_couples, 
                                                          list_id_data_save_thinning, 
                                                          list_id_data_remove_thinning,
                                                          kdtree)
  
    # test for thinning 
    if (list_id_data_save_couples.size+list_id_data_remove_thinning.size+list_id_data_save_thinning.size) != dict_obs['id_data'].size:
        print (list_id_data_save_couples.size+list_id_data_remove_thinning.size+list_id_data_save_thinning.size)
        print (dict_obs['id_data'].size)
        raise ValueError('id_data save in at least two list')

    conn_filememory.commit()
  
    # combine in one file to Midas
    try:
        radvelso.qcavg.combine(pathfileout, filememory)
    except sqlite3.Error as error:
        print("Error while creating a single sqlite file:  {os.path.basename(filememory)}", error)
    # close connection 
    conn_filememory.close()

def find_sample_entry(src_dir, file_type, variable=None, prefix=None):
   
    """find first entry of a given variable in a given directory
    



    """

    if prefix is None:
        prefix = '2*'

    found = False
    if file_type == 'fst':
        file_list = sorted(Path(src_dir).glob(prefix))
        file_list = sorted(Path(src_dir).glob(prefix))
        file_list = sorted(Path(src_dir).glob(prefix))
        for this_file in file_list:
            if this_file.is_file():
                
                out_dict = fst_tools.get_data(str(this_file), var_name=variable, latlon=True )
                if out_dict is not None:
                    found = True
                    break

    else:
        raise ValueError('filetype not supported')

    if not found:
        raise ValueError(f'sample file not found in {src_dir}')

    return out_dict

def compute_thinning(center_time,
                     window_width,
                     infile_list, 
                     pathout, 
                     outfile_struc, 
                     timing, 
                     n_cpus,
                     delta_time_thinning_min,
                     delta_distance_neighbours_m,
                     delta_height_vertical_m,
                     delta_distance_couple_m,
                     pathin_model):
  

    """launch computation of average volums scans, possibly in parallel
  
    args:
    ----------------

    center_time  : datetime object,  center time of the assimilation window
    window_width : [hours] Width of the assimilation window
    infile_list  : list of input files to be thinned
    pathout      : output average sqlite file(s) 
    outfile_struc: structure of output file name ; will be passed to strftime
    timing       : activation of time analysis, only the first PPI in a volume scan will be averaged
    n_cpus      : number of cpu
    delta_time_thinning_min: time slices for thinning
    delta_distance_neighbours_m: minimum distance to exclude neighbors
    delta_height_vertical_m: vertical distance where horizontal thinning takes place.
    delta_distance_couple_m: maximum distance to consider couples of observations from different radars
    pathin_model: path to the model to find out the grid size
  
    output:
    ----------------

    Nothing
    Average sqlite file(s) are created with the '_thin' suffix
  
    """

    #start and stop time of assimilation window
  
    infile_combine =  f'combine_{center_time.strftime(outfile_struc)}'
    if os.path.isfile(infile_combine):
        os.remove(infile_combine)
    if not os.path.isdir(pathout):
        os.mkdir(pathout)
  
    con_infile_combine = sqlite3.connect(infile_combine)
    con_infile_combine.execute("pragma temp_store = 2;")
    schema = radvelso.qcavg.find_schema('schema')
    with open(schema) as f:
        schema = f.read()
    con_infile_combine.executescript(schema)
    for infile in infile_list:
        radvelso.qcavg.combine(infile_combine, infile)
   # create info and resume_tables in fileout
    create_info_midas_tables(infile, con_infile_combine)  
    con_infile_combine.close()
   
    window_t0 = center_time - datetime.timedelta(seconds=3600*window_width/2.)
    window_tf = center_time + datetime.timedelta(seconds=3600*window_width/2.)
    vol_scan_list = []
    while window_t0 < window_tf :
        window_t1 = window_t0 + datetime.timedelta(minutes=delta_time_thinning_min)
        vol_scan_list.append( {'file':infile_combine, 'date0':window_t0, 'date1':window_t1 } )
        window_t0 = window_t1 
    ################
    #flush fileout if it already exists
    pathfileout=f"{pathout}/{center_time.strftime(outfile_struc)}"
    
    if os.path.isfile(pathfileout):
        os.remove(pathfileout)
  
    #init large output file
    conn_pathfileout = sqlite3.connect(pathfileout)
    conn_pathfileout.execute("pragma temp_store = 2;")
    schema = radvelso.qcavg.find_schema('schema')
    with open(schema) as f:
        schema = f.read()
    conn_pathfileout.executescript(schema)
    # using maestro_archives/
    # setup projection object
    model_dat  = find_sample_entry(pathin_model, 'fst', variable='UU', prefix=None) 
    model_lats = model_dat['lat']
    model_lons = model_dat['lon']
   
    if len(vol_scan_list) == 0:
        raise RuntimeError("""List of volume scan to process is empty. 
                          Check that files are available and search criteria are correct.""")
    tc_0 = time.time()
    if timing :
        print ("Compute only one PPI ")
        thinning(pathfileout,
                 vol_scan_list[0]['file'], 
                 vol_scan_list[0]['date0'], 
                 vol_scan_list[0]['date1'], 
                 delta_distance_neighbours_m, 
                 delta_height_vertical_m, 
                 delta_distance_couple_m, 
                 model_lats, 
                 model_lons, 
                 timer=True)
        tc_1 = time.time()
    else:
        if n_cpus == 1:
            #serial execution, usefull for debugging
            print('Serial execution')
            for vscan in vol_scan_list:
                thinning(pathfileout, 
                         vscan['file'] , 
                         vscan['date0'], 
                         vscan['date1'], 
                         delta_distance_neighbours_m, 
                         delta_height_vertical_m, 
                         delta_distance_couple_m, 
                         model_lats, 
                         model_lons)
        else:
            print(f'Compute {len(vol_scan_list)} volume scans in parallel')
            with tempfile.TemporaryDirectory() as tmpdir:
                #the directory dask-worker-space/ will be in tmpdir
                with dask.distributed.Client(processes=True,
                                             threads_per_worker=1, 
                                             n_workers=n_cpus, 
                                             local_directory=tmpdir, 
                                             silence_logs=40) as client:
  
                    #delay data 
                    model_lons = client.scatter(model_lons)
                    model_lats = client.scatter(model_lats)
                    joblist = [delayed(thinning)(pathfileout, 
                                                 vscan['file'],
                                                 vscan['date0'], 
                                                 vscan['date1'], 
                                                 delta_distance_neighbours_m, 
                                                 delta_height_vertical_m, 
                                                 delta_distance_couple_m, 
                                                 model_lats, 
                                                 model_lons) for vscan in vol_scan_list]
                    dask.compute(joblist)
         
        sample_file  = vol_scan_list[0]['file']
        # create info and resume_tables in fileout
        create_info_midas_tables(sample_file, conn_pathfileout)   
        # improve searches with index tables
        radvelso.qcavg.create_index_tables_idobs_iddata(conn_pathfileout)
        # collision_test
        radvelso.qcavg.collision_test(conn_pathfileout)
        # close connection
        conn_pathfileout.close()
        tc_1 = time.time()
     
    print(f"Runtime total: {round(tc_1-tc_0,4)} s")

def arg_call():

    import argparse 

    parser = argparse.ArgumentParser()
    parser.add_argument('--center_time',  default='undefined', type=str,   help="YYYYMMDDHH center time of assimilation window")
    parser.add_argument('--window_width', default=0.,          type=float, help="[hours] width of assimilation window")
    parser.add_argument('--inputfiles', nargs="+", default='undefined',    help="input sqlite file to average")
    parser.add_argument('--pathin',       default='undefined', type=str,   help="directory where are input sqlite files")
    parser.add_argument('--infile_struc', default='/%Y%m%d%H_ra',type=str,help="structure of input file name")
    parser.add_argument('--pathout',      default=os.getcwd(), type=str,   help="where averaged sqlite files will be put")
    parser.add_argument('--outfile_struc',default='%Y%m%d%H_superobbed_dvel_ground_radars.sqlite', type=str,   help="structure of output file name")
    parser.add_argument('--timing',       action="store_true",             help="Average only one PPI for time analysis" ) 
    parser.add_argument('--n_cpus',       default=1,           type=int,   help="Number of rays for averaging" )
    parser.add_argument('--delta_time_thinning_min',   default=10,         type=float, help="window_width to average (min)" )
    parser.add_argument('--delta_distance_neighbours_m', default=30000,        type=float, help="min distance neighbours (m)" )
    parser.add_argument('--pathin_model',       default='undefined', type=str,   help="directory where are input model file")
    parser.add_argument('--delta_height_vertical_m', default=1000,         type=int, help="delta distance for vertical interval (m)" )
    parser.add_argument('--delta_distance_couple_m',   default=1000,         type=int, help="min distance for couple of different radars is considered (m)" )

    args = parser.parse_args()

    if args.inputfiles == 'undefined' and args.pathin == 'undefined':

        args.center_time = '2019062706'
        args.window_width = 6.
        #option1: explicitely specify inputfiles
        #args.inputfiles = ['/space/hall4/sitestore/eccc/cmd/a/dlo001/data/doppler_qc/doppler_qc_v0.3/sqlite_v1.0.0_qc/split_6h/USVNX/2019073100_ra',
        #                   '/space/hall4/sitestore/eccc/cmd/a/dlo001/data/doppler_qc/doppler_qc_v0.3/sqlite_v1.0.0_qc/split_6h/CASRA/2019073100_ra']
        #option2: specify pathin + infile_struc and let Python search for files
        args.pathin = '/fs/site6/eccc/cmd/a/dlo001/data/doppler_qc/doppler_qc_v0.4/sqlite_v1.0.0_qc/split_6h/'
        args.pathout = './work'
        args.timing = False
        args.plot   = False
        args.n_cpus = 80

        print(f'superobs called with no input filename(s)')
        print(f'We are running demo with:')
    for arg in vars(args):
        print(f'--{arg}  {getattr(args, arg)}')
    if args.center_time == 'undefined':
        raise ValueError('Center time of assimilation window must be provided')
    else:
        args.center_time = datetime.datetime.strptime(args.center_time, '%Y%m%d%H')

    if np.isclose(args.window_width, 0.) :
        raise ValueError('Window width must be provided')
    if args.pathin_model != 'undefined':
        #if inputfiles argument is provided, we use that
        infile_list = args.inputfiles 

    if args.inputfiles != 'undefined':
        #if inputfiles argument is provided, we use that
        infile_list = args.inputfiles 

    elif args.pathin != 'undefined': 
        #alternatively, search for files with pathin+infile_struc 
        if not os.path.isdir(args.pathin):
            raise ValueError(f'pathin: {args.pathin} does not exist.')
        search_str = args.center_time.strftime(args.infile_struc)
        infile_list = glob.glob(f'{args.pathin}/{search_str}*')
    else:
        raise ValueError('At least one of inputfiles ot pathin must be provided')

    #check infile_list
    if len(infile_list) == 0:
        raise ValueError('infile_list is empty, we stop here')
        sys.exit(1)

    else:
        for this_file in infile_list:
            if not os.path.isfile(this_file):
                raise ValueError(f'inputfiles: {this_file} does not exist.')

    if not os.path.isdir(args.pathout):
        os.mkdir(args.pathout)
    #sys.exit is used to the return status of main is catched and passed to caller
    sys.exit(compute_thinning(args.center_time,
                              args.window_width,
                              infile_list, 
                              args.pathout, 
                              args.outfile_struc, 
                              args.timing, 
                              args.n_cpus,
                              args.delta_time_thinning_min,
                              args.delta_distance_neighbours_m,
                              args.delta_height_vertical_m,
                              args.delta_distance_couple_m,
                              args.pathin_model))

if __name__ == '__main__':
    arg_call()
