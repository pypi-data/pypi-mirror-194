
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
from datetime import  timedelta
import domutils.radar_tools as radar_tools
import domutils.geo_tools as geo_tools
from scipy.interpolate import LinearNDInterpolator
from radvelso.unravel import find_reference
from radvelso.unravel.core import Dealias as DealiasBase
import xarray as xr
import pickle 
import scipy.spatial
import cartopy.crs as ccrs
import warnings
import joblib
import domcmc.fst_tools as fst_tools

class Dealias(DealiasBase):
    
    """
    Dealiasing class.
    """

    def __init__(
        self, ppi_ranges, ppi_azimuths, ppi_elevation, ppi_velocity, nyquist, alpha=0.6):
       
        """
        Constructor.

        arg:
        ----------
        ppi_ranges: array[bins]
            PPI's bins range in meters.
        ppi_azimuths: array[rays]
            PPI's rays angle in degrees.
        ppi_elevation: float
            PPI elevation angle in degrees.
        ppi_velocity: array[rays, bins]
            Doppler velocity.
        nyquist: float
            PPI nyquist velocity.
        alpha: float
            Coefficient for which the nyquist velocity periodicity range is
            considered valid.
        """

        super().__init__(
            ppi_ranges,
            ppi_azimuths,
            ppi_elevation,
            ppi_velocity.copy(),
            nyquist,
            alpha=alpha,
        )
        self._initialized = False

    def initialize(
        self, model_dop_velocity, beta=0.25, missing=-9999.0, undetect=-3333.0):
     
        """
        Initialize the dealiasing finding the radials of reference.

        1. Consider as "reference velocities" dealiased velocities close to the model's doppler velocity.
           This step is an initial dealiasing that helps the sbsequent dealiasing steps.
        2. Find reference radials (section 3.a.2, Leuf et al, 2020).

        Notes
        -----
        Louf, V., Protat, A., Jackson, R. C., Collis, S. M., & Helmus, J. (2020).
        UNRAVEL: A Robust Modular Velocity Dealiasing Technique for Doppler Radar,
        Journal of Atmospheric and Oceanic Technology, 37(5), 741-758. Retrieved Mar 2, 2022.
        https://journals.ametsoc.org/view/journals/atot/37/5/jtech-d-19-0020.1.xml
        """

        model_dop_velocity = model_dop_velocity.copy()

        # Prepare the data
        invalid = (self.velocity == missing) | (self.velocity == undetect)
        valid = ~invalid
        self.velocity[invalid] = np.nan
        self.dealias_vel = self.velocity.copy()

        #####################################
        # Initial dealiasing using model data
        #print (invalid)
        model_dop_velocity[invalid] = missing
        self.velocity[invalid] = missing

        # Find reference velocities close to the model_velocity (reference)
        # 1. Generate velocity candidates at +/- 2*Ny*i intervals.
        vel_candidates = []
        for i in range(-3, 4):
            vel_candidates.append(self.velocity + 2 * i * self.nyquist)
        vel_candidates = np.stack(vel_candidates, axis=-1)

        # 2. Keep the closest one to the model_velocity (reference)
        sorting_idx = np.argsort(
            np.abs(vel_candidates - model_dop_velocity[:, :, None]), axis=2
        )[:, :, 0].squeeze()
        xi, yi = np.meshgrid(
            range(sorting_idx.shape[0]), range(sorting_idx.shape[1]), indexing="ij"
        )
        vel_candidate = vel_candidates[xi, yi, sorting_idx]

        # 3. Check if the candidate is |Vcand-Vobs|< beta*Vny
        #    If True, accept that that candidate.

        # Check is the candidate is equal to the original velocity.
        # not_modified = np.abs(vel_candidate - self.velocity) < 0.0001
        vel_diff = np.abs(vel_candidate - model_dop_velocity)
        accepted_candidates = vel_diff < beta * self.nyquist  # & (~not_modified)
        
        # not_modified = not_modified & valid
        model_valid = (model_dop_velocity != missing) & (model_dop_velocity != undetect)
        accepted_candidates = accepted_candidates & valid & model_valid

        if np.count_nonzero(accepted_candidates.size > 0):

            self.dealias_vel[accepted_candidates] = vel_candidate[accepted_candidates]
            self.flag[accepted_candidates] = 2  # Dealiased
            # self.flag[not_modified] = 0  # Consider as unprocessed.

            # NOTE: Once a velocity has been flagged 1 or 2, it is not modified anymore by
            # subsequent steps.
        self.dealias_vel[invalid] = np.nan
        self.flag[invalid] = -1

        ########################
        # Find reference radials
        start_beam, end_beam = find_reference.find_reference_radials(
            self.azimuth, self.dealias_vel)

        azi_start_pos = np.argmin(np.abs(self.azimuth - start_beam))
        azi_end_pos = np.argmin(np.abs(self.azimuth - end_beam))

        self.azi_start_pos = azi_start_pos
        self.azi_end_pos = azi_end_pos

        self._initialized = True

    def dealiase(self):

        """
        Dealise the doppler velocity.

        Dealiasing flags:
        -3: Missing values
        0: Unprocessed. This velocity could not be dealiased.
        1: Processed and unchanged value
        2: Processed and dealiased value.
        """

        if not self._initialized:
            raise RuntimeError(
                "The dealiasing object was not initialized.\n"
                "Run the initialize(*args,**kwargs) method first.")

        for window in [6, 12, 24]:
            self.correct_range(window)
            self.correct_clock(window)
            if self.check_completed():
                break

        if not self.check_completed():
            for window in [(5, 5), (10, 10), (20, 20), (40, 40)]:
                self.correct_box(window)
                if self.check_completed():
                    break

        self.correct_closest()
        self.flag[self.flag > 2] = 2

def find_schema(schema):

    """find schema file contained in the Python package
  
    args:
    ----------------
    
    schema: the schema we are looking for
  
    output:
    ----------------

    full path of schema file that was found
    
    """
  
    #full path of radvelso module
    radvelso_dir = os.path.dirname(radvelso.__file__)
    #root path of radvelso package (one dir up from radvelso module)
    package_dir = os.path.dirname(radvelso_dir)
    #full path of schema we are looking for
    schema_file = f'{package_dir}/radvelso/schema/{schema}'
  
    if not os.path.isfile(schema_file):
        raise ValueError(f'schema_file: {schema_file} does not exist')
  
    return schema_file


def make_input_ppi_db(filein, 
                      stn, 
                      this_time, 
                      nominal_ppi_elevation, 
                      min_range_in_ppi, 
                      max_range_in_ppi,
                      obs_nyquist):

    """make a separate db for one PPI
  
    This db is saved in memory and allows quich search of averaging boxes
  
    args: 
    ---------------

    filein                 : input sqlite file containing many radars and times
    stn                    : radar for this one volume scan
    this_time              : end time of this one volume san
    nominal_ppi_elevation  : nominal elevation
    min_range_in_ppi       : min range in PPI
    max_range_in_ppi       : max range in PPI
    obs_nyquist            : Nyquist for QC
     
    output: 
    ---------------

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
  
    schema = find_schema('schema')
    with open(schema) as f:
        schema = f.read()
    conn_ppi_db.executescript(schema)
    # improve searches with index tables
    create_index_tables_elevation_azimuth(conn_ppi_db)
    create_index_tables_idobs_iddata(conn_ppi_db)
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
                      and time = ? 
                      and round(nominal_ppi_elevation, 1) = ? 
                      and nyquist >= ?
                      ;"""
    conn_ppi_db.execute(order_sql, (stn, this_time, round(nominal_ppi_elevation,1), obs_nyquist))
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
    query = (  f'select count(*) from data;') #ORDER BY RANDOM()  ;')
    c=  conn_ppi_db.cursor()
    avg1  = c.execute(query)
    result = c.fetchone()
    
    return conn_ppi_db,  result[0]

def num_obs_in_ppi(conn_ppi_db, 
                   min_range_in_ppi, 
                   max_range_in_ppi):
 
    """count total number of observations in PPI
    
    args:
    ----------------
      
    conn_ppi_db      : connexion to sqlite db for this PPI
    min_range_in_ppi : min range in PPI
    max_range_in_ppi : max range in PPI
  
    output:
    ----------------

    number of observations in PPI
    
    """
  
    order_sql= """ SELECT
                     count(*)
                   FROM
                     data 
                   WHERE
                     range >= ? 
                     and range <= ?
                      """
    
    conn_ppi_db.row_factory =sqlite3.Row
    cursor = conn_ppi_db.cursor()
    cursor.execute( order_sql,(min_range_in_ppi, max_range_in_ppi))
    result = cursor.fetchone()
    number_obs_ppi   = result[0]
   
    return number_obs_ppi
    
def average_boxes(conn_filememory,
                  id_obs,
                  id_data,
                  azimuth,
                  half_delta_range_box,
                  range_bin_centers, 
                  half_delta_azimuth_box,
                  obs_percentage):
 
    """ Average input data found in range and azimuth "box"
       
    args:
    ----------------

    conn_filememory        : connexcion to output file (and attached ppi_db)
    id_obs                 : id_obs for this ray
    id_data                : id_data for this averaging box
    azimuth                : center azimuth of averaging box
    half_delta_range_box   : half of the delta_range for this averaging box
    range_bin_centers      : range center for this averaging box 
    half_delta_azimuth_box : half of azimuthal span of averaging box
  
    output:
    ----------------

    number of observations used in this average
    """
  
    # bounds of the box
    right_azimuth   = azimuth+half_delta_azimuth_box
    left_azimuth    = azimuth-half_delta_azimuth_box
    range_box_start = range_bin_centers-half_delta_range_box
    range_box_end   = range_bin_centers+half_delta_range_box
  
    # Condition changes for azimuth centered at zero 
    condition="and"
    if (left_azimuth<0): 
        left_azimuth=360.-half_delta_azimuth_box  
        condition="or"
    
    order_sql = """ SELECT 
                      count(*),
                      half_delta_azimuth,
                      half_delta_range,
                      sum(center_elevation)
                    FROM
                      db_ppi.data natural join db_ppi.header 
                    WHERE
                      range >= ? 
                      and range < ?
                      and id_obs in(
                        SELECT 
                          id_obs 
                        FROM 
                          db_ppi.header 
                        WHERE 
                          center_azimuth >= ? 
                          """ + condition + """ center_azimuth < ?
                      ) """
  
    cursor = conn_filememory.execute(order_sql, (range_box_start, range_box_end, left_azimuth, right_azimuth))
    result = cursor.fetchone()
    # get Num observation for thos box
    number_obs_box = result[0]
    half_delta_azimuth = result[1]
    half_delta_range = result[2]
    # get sum elevation for this box
    sum_elevation = result[3]
    number_obs_percentage = 0.
    if number_obs_box == 0: 
        # no observations in averaging box, we exit here  
        return 0., 0., 0.
  
    else:
        if (half_delta_azimuth==0):
            half_delta_azimuth=0.5
        if (half_delta_range==0):
            half_delta_range = 125
        number_obs_max = (half_delta_azimuth_box/half_delta_azimuth)*(half_delta_range_box/half_delta_range)
        if ((100*number_obs_box/number_obs_max)>=obs_percentage):
          
            # Write the found values of avg (obsvalue) (among others) in the box
            order_sql = """INSERT into data(
                           id_obs, 
                           range, 
                           obsvalue, 
                           half_delta_azimuth, 
                           half_delta_range, 
                           id_data, 
                           quality_index,
                           number_obs
                           ) 
                         SELECT
                           ?, ?,
                           avg(obsvalue), 
                           ?, ?, ?,
                           avg(quality_index), ?
                         FROM
                           db_ppi.data 
                         WHERE
                           range >= ? 
                           and range < ? 
                           and id_obs in(
                             SELECT 
                               id_obs 
                             FROM 
                               db_ppi.header 
                             WHERE 
                               center_azimuth >= ? """+condition+""" center_azimuth < ?
                           )"""
          
            conn_filememory.execute(order_sql, (id_obs,
                                                range_bin_centers, 
                                                half_delta_azimuth_box,
                                                half_delta_range_box,
                                                id_data,
                                                number_obs_box,
                                                range_box_start,
                                                range_box_end, 
                                                left_azimuth,
                                                right_azimuth,))
            number_obs_percentage = number_obs_box
  
    return number_obs_box, sum_elevation, number_obs_percentage


def create_header(conn_filememory, 
                  ray,        
                  avg_elevation,
                  id_obs):

    """ Create header entry
  
    A header is created matching a bunch of entries in data table
  
    args:
    ----------------

    conn_filememory  : connextion to  file in memory
    sample_header    : dictionary entry containing info from first header in ppi
    ray              : data structure of averaging ray        
    avg_elevation    : average elevation envountered along averaging ray 
    id_obs           : id_obs of radar beam
    
    output:
    ----------------

    Nothing
    header entry is written in output sqlite file
  
    """
  
    #get first header in PPI
    order_sql =  """ SELECT * FROM db_ppi.header """  
    conn_filememory.row_factory = sqlite3.Row 
    cursor = conn_filememory.cursor()
    cursor.execute( order_sql)
    sample_header = cursor.fetchone()
  
    #variables from the first header encountered
    #those will not change for a given PPI
    id_stn                = sample_header['id_stn']
    location              = sample_header['location']
    lat                   = sample_header['lat']
    lon                   = sample_header['lon']
    date                  = sample_header['date']
    time                  = sample_header['time']
    codtyp                = sample_header['codtyp']
    antenna_altitude      = sample_header['antenna_altitude']
    nyquist               = sample_header['nyquist']
    nominal_ppi_elevation = sample_header['nominal_ppi_elevation']
    time_start            = sample_header['time_start']
    time_end              = sample_header['time_end']
       
    #variables that depend on averaging parameters for this ray
    azimuth     = ray['azimuth']
    range_start = ray['min_range_in_ppi']
    range_end   = ray['max_range_in_ppi']
  
    #variables that depend on the data that was averaged for this ray
    # avg_elevation
    # time_start
    # time_end 
  
    order_sql ="""INSERT  into  header(
                    id_obs,id_stn, location, lat, lon, date, time, codtyp, 
                    antenna_altitude, nyquist, nominal_ppi_elevation,
                    center_azimuth, range_start, range_end,
                    center_elevation, time_start, time_end) 
                  VALUES
                     ( ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """
  
    conn_filememory.execute( order_sql,(id_obs, id_stn, location, lat, lon, date, time, codtyp,
                                        antenna_altitude, nyquist, nominal_ppi_elevation, azimuth,
                                        range_start, range_end, avg_elevation, time_start, time_end))
  
def create_index_tables_elevation_azimuth(conn):
   
    """ Create index tables
    For elevation and azimuth  

    args:
    ----------------

    conn          : connextion to sqlite file
    
    output:
    ----------------

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

def create_index_tables_idobs_iddata(conn):

    """ Create index tables
    For id_obs and id_data

    args:
    ----------------

    conn          : connextion to sqlite file
    
    output:
    ----------------

    Nothing
      index tables i sqlite file
  
    """
    
    order_sql = """ CREATE INDEX
                      idx1
                    ON header(id_obs);"""
    conn.execute(order_sql)
    
    order_sql = """CREATE INDEX
                     idx2 
                   ON data(id_obs);"""
    conn.execute(order_sql)
  
    order_sql = """CREATE INDEX
                     idx3 
                   ON data(id_data);"""
    conn.execute(order_sql)
  
def create_info_midas_tables(filein,
                              conn_pathfileout, 
                              n_rays,        
                              delta_range,
                              ops_run_name,
                              obs_percentage, 
                              obs_nyquist):
   
    """ Create header entry
  
    A header is created matching a bunch of entries in data table
  
    args:
    ----------------
     
    filein        : input sqlite file with raw data
    conn_pathfileout  : connextion to output file
    n_rays        : number of rays 
    delta_range   : delta range of the boxes
    ops_run_name  : name of operational run
    obs_percentage: min percentage of obs per box to calculated avegare 
    obs_nyquist   : min nyquist in ppi to calculated avegare 
    
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
  
    order_sql =""" INSERT  into  info (
                     NAME, DESCRIPTION, UNIT) values
                   (?,?,?)"""
    conn_pathfileout.execute( order_sql, ('Maximun nyquist', 'Maximum Nyquist permitted', obs_nyquist,))
   
  
    order_sql =""" INSERT  into  info (
                     NAME, DESCRIPTION, UNIT) values
                   (?,?,?)"""
    conn_pathfileout.execute( order_sql, ('Minus percentage of observation in the box', 'percentage of observation in the box to average', obs_percentage,))
  
  
    order_sql =""" UPDATE  info SET DESCRIPTION = REPLACE(DESCRIPTION,'OFF','ON') where name = 'SUPEROBBING';"""
    conn_pathfileout.execute( order_sql)
    order_sql =""" UPDATE  info SET DESCRIPTION = ? where name = 'SUPEROBBING_NUMBER_RAYS' ;"""
    conn_pathfileout.execute( order_sql, ( n_rays, ))
    order_sql =""" UPDATE  info SET DESCRIPTION = ? where name = 'SUPEROBBING_DELTA_RANGE' ;"""
    conn_pathfileout.execute( order_sql, (delta_range, ))
  
    # Resume table 
    order_sql ="""CREATE TABLE resume(date integer , time integer , run varchar(9));"""
    conn_pathfileout.execute( order_sql)
    YYYYMMDD = os.path.basename(filein)[:8]
    HH = os.path.basename(filein)[8:10]
    order_sql = """INSERT into resume values(?,?,?);"""
    conn_pathfileout.execute( order_sql, (YYYYMMDD, HH, ops_run_name,))
    
    # rdb4_schema table
    order_sql ="""CREATE TABLE rdb4_schema( schema  varchar(9) );"""
    conn_pathfileout.execute( order_sql)
    order_sql ="""INSERT into rdb4_schema values('radvel');"""
    conn_pathfileout.execute( order_sql)
  
    # commint and detach database
    conn_pathfileout.commit()
    conn_pathfileout.execute("DETACH DATABASE db_all")


def superobs(filein, 
             stn,
             this_datetime, 
             pathfileout,
             ops_run_name, 
             obs_percentage,
             obs_nyquist, 
             pathoutpkl,
             model_files_list, 
             model_valid_date_list,
             assim_T0,
             assim_window_width,
             model_data_dir,
             timer=False):
             
    """ Average  a volume scan
    
    This function takes in raw measurements in an sqlite file and 
    creates an average volume scan based on the content of the 
    provided averaging structure. 
  
    args:
    ----------------

    filein        : input sqlite file with raw data
    stn           : name of radar that generated the volume scan being processed
    this_datetime : valid date time of radar observation 
    pathfileout   : output averaging  sqlite file 
    ray_list      : averaging template containing info for how to average PPIs
    ops_run_name  : name of operational run 
    obs_nyquist   : min nyquist in ppi to calculated avegare 
    obs_percentage: min percentage of obs per box to calculated avegare 
    model_data_dir:  str
    pathout       : path to pickle files
       Directory where the model data is stored in fst format.
    timer         : activation of time analysis, only the first PPI in a volume scan will be averaged
   
    output:
    ----------------

    This function outputs nothing
      However, the averaged data is put in a sqlite file with the same name
      as the original but with the suffix "_superobs" 
  
    """

    hhmiss_pad =  this_datetime.strftime('%H%M%S') 
    #no zeros on left but still 0 if 000000
    hhmiss_nopad = str(int(hhmiss_pad))
  
    #figure out minimum and maximum ranges in averaged PPI
    file = open(f"{pathoutpkl}/averaging_template.pkl",'rb')
    ray_list = pickle.load(file)
    file.close()
    n_rays = len(ray_list)
    min_range_in_ppi = 1.e9
    max_range_in_ppi  = 0. 
    for this_ray in ray_list:
        min_range_in_ppi = np.amin([this_ray['min_range_in_ppi'], min_range_in_ppi])
        max_range_in_ppi = np.amax([this_ray['max_range_in_ppi'], max_range_in_ppi])
  
  
    #Prepare file in memory
    filememory=f'file:{os.path.basename(filein)}_{hhmiss_pad}_{stn}?mode=memory&cache=shared'
    print(filememory)
    conn_filememory = sqlite3.connect(filememory, uri=True, check_same_thread=False)
    # off the journal
    conn_filememory.execute("""PRAGMA journal_mode=OFF;""")
    # SQLite continues without syncing as soon as it has handed data off to the operating system
    conn_filememory.execute("""PRAGMA synchronous=OFF;""")
  
    schema = find_schema('schema')
    with open(schema) as f:
        schema = f.read( )
    conn_filememory.executescript(schema)
    # improve searches with index tables
    create_index_tables_idobs_iddata(conn_filememory)
    # Construct a new Generator with the default BitGenerator (PCG64).
    rng = np.random.default_rng()
    maxsize = sys.maxsize
    # maxsize = 9223372036854775807 from python -c 'import sys; print(sys.maxsize)'
    ids     = rng.integers(maxsize, size=2)
    id_data = ids[0].tolist()
    id_obs  = ids[1].tolist()
    #list of elevations in file for this radar at this time
    conn_elevation = sqlite3.connect(filein)
    order_sql = """ SELECT 
                      distinct nominal_ppi_elevation 
                    FROM
                      header 
                    WHERE
                      id_stn = ?
                      and time = ? 
                      and nyquist >= ?
                    ORDER BY 
                      1;"""
                         
    nominal_ppi_elevations = [ np.round(elev[0],4) for elev in conn_elevation.execute(order_sql, (stn, hhmiss_nopad,obs_nyquist )).fetchall() ]
    conn_elevation.close()
  
    if timer : 
        nominal_ppi_elevations = nominal_ppi_elevations[0:1]
    for nominal_ppi_elevation in nominal_ppi_elevations:
  
        conn_ppi_db, nobs = make_input_ppi_db(filein, 
                                              stn, 
                                              hhmiss_nopad, 
                                              nominal_ppi_elevation, 
                                              min_range_in_ppi, 
                                              max_range_in_ppi,
                                              obs_nyquist)
  
        if os.path.exists(model_data_dir):

            # open model information for the radar

            #TODO
            #Use commented code below to find pickle file just before and just after
            # the PPI tim we are interested in

            ##make a list of available pickle files and their validity dates
            #search_pattern = os.path.join(pathoutpkl,f'{stn}*.pkl'))
            #pickle_files_list = sorted(glob.glob(search_pattern))
            #if len(model_files_list) == 0:
            #    raise RuntimeError(f'No pickle files found for criterion: {search_pattern}')
            #pickle_valid_date_list = [ get_date_from_filename(this_file,'pickles') for this_file in model_files_list ] 
            #
            #model_filenames, dt_model_time = surrounding_model_files(this_datetime, 
            #                                                         pickle_files_list, 
            #                                                         pickle_valid_date_list)
            #         

            make_dealias(this_datetime,
                         model_files_list, 
                         model_valid_date_list,
                         assim_T0,
                         assim_window_width,
                         conn_ppi_db,
                         filein,
                         stn,
                         model_data_dir,
                         nominal_ppi_elevation,
                         pathoutpkl)
  
  
        #temporarily attach ppi db to output file
        conn_filememory.execute('ATTACH DATABASE "file::memory:?cache=shared" AS db_ppi') 
  
        #iterate over rays of the averaged PPI
        number_obs_ppi = 0
        for ray in ray_list:    
  
            #variables that do not change for a given ray
            azimuth          = ray['azimuth']
            half_delta_range = ray['half_delta_range']
  
            # average boxes and write result in data table of filememory db (Memory)
            sum_elev_ray   = 0.
            number_obs_ray = 0.
            number_obs_ray_percentage = 0.
            for range_bin_center, half_delta_azimuth in zip(ray['range_bin_centers'], 
                                                            ray['half_delta_azimuth']):
                   
                number_obs_box, sum_elev_box, number_obs_percentage = average_boxes(conn_filememory,
                                                                                    id_obs,
                                                                                    id_data,
                                                                                    azimuth, 
                                                                                    half_delta_range,
                                                                                    range_bin_center,
                                                                                    half_delta_azimuth,
                                                                                    obs_percentage)
                if number_obs_box > 0:
                    number_obs_ray += number_obs_box
  
                if number_obs_percentage>0:
                    sum_elev_ray   += sum_elev_box
                    id_data = (rng.integers(maxsize, size=1))[0].tolist()
                    number_obs_percentage +=number_obs_percentage 
                    number_obs_ray_percentage += number_obs_box
            
            #   if any data was found in ray, create header entry matching average bins
            # already entered in data table
            if number_obs_ray_percentage > 0:
  
                avg_elevation = sum_elev_ray / number_obs_ray_percentage
  
                create_header(conn_filememory, 
                              ray, 
                              avg_elevation,
                              id_obs)
                id_obs  = (rng.integers(maxsize, size=1))[0].tolist()
            
            #keep track of how many obs have been averagd in ppi
            number_obs_ppi += number_obs_ray
  
        # Test number of observations in source PPI vs num observation used in averaging boxes
        number_obs_in_source_ppi = num_obs_in_ppi(conn_ppi_db, 
                                                  min_range_in_ppi, 
                                                  max_range_in_ppi)
  
        if (number_obs_ppi != number_obs_in_source_ppi): 
            raise RuntimeError("""Error: number of observations in source ppi is different from number of obs used in average""")
  
        conn_filememory.commit()
        conn_filememory.execute("DETACH DATABASE db_ppi")
        conn_ppi_db.close()
  
    # Update flag, varno and vcoord_type
    conn_filememory.execute("UPDATE data SET flag=0, varno=21014, vcoord_type=7007")
    conn_filememory.commit()
    # Copy in a single sqlite file from memory (parallel)
    try:
        combine(pathfileout, filememory)
    except sqlite3.Error as error:
        print("Error while creating a single sqlite file:  {os.path.basename(filememory)}", error)
    # close connection 
    conn_filememory.close()
 

def combine(pathfileout, filememory):

    """ Creating a single sqlite file from multiple sqlite files
 
    args:
    ----------------

     pathfileout   : output averaging  sqlite file 
     filememory    : name of the sqlite file in memory to copy
   
    output:
    ----------------

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
                    FROM  this_avg_db.header;"""
    conn_pathfileout.execute(order_sql) 
    order_sql = """ INSERT into data
                    SELECT
                      *
                    FROM  this_avg_db.data;"""
    conn_pathfileout.execute(order_sql)

    conn_pathfileout.commit()
    conn_pathfileout.execute(""" DETACH DATABASE this_avg_db """)

def surrounding_model_files(scan_datetime, 
                            model_files_list, 
                            model_valid_date_list,
                            assim_T0 = None, 
                            assim_window_width = None):
  
    """
    Return the model files just before and just after a volume scan
    Time difference between each file and volume scan time is alto returned

    Args:
    ----------------
    scan_datetime: time of volume scan to bracket
    model_file_list: list of model filed to choose from
    model_valid_date_list: validity date for each file in model_file_list 

    output:
    ----------------
    [file_before, file_after], [dt_file_before, dt_file_after]
    """

    if assim_T0 is not None and assim_window_width is not None:
        assim_window_start = assim_T0 - datetime.timedelta(seconds=int(assim_window_width/2.*3600.))
        assim_window_end   = assim_T0 + datetime.timedelta(seconds=int(assim_window_width/2.*3600.))
    else:
        # no limits on time
        assim_window_start = datetime.datetime(0,   0,0,0,0)
        assim_window_end   = datetime.datetime(3000,0,0,0,0)

    for ii, this_model_vdate in enumerate(model_valid_date_list):

        if ii+1 == len(model_valid_date_list):
            raise ValueError('model files do not bracket vol scan time')

        if (this_model_vdate >= assim_window_start and 
            this_model_vdate <= assim_window_end):

            dt_before = (scan_datetime - model_valid_date_list[ii])
            dt_before_seconds = dt_before.days*24*3600 + dt_before.seconds
            dt_after  = (scan_datetime - model_valid_date_list[ii+1])
            dt_after_seconds = dt_after.days*24*3600 + dt_after.seconds

            if dt_before_seconds >= 0. and dt_after_seconds <= 0. :
                break

    file_before = model_files_list[ii]
    file_after  = model_files_list[ii+1]

    return [file_before, file_after], [dt_before_seconds, dt_after_seconds]

def collision_test(conn_pathfileout):
   
    """Check the collisiona and that the id_obs from the header have an associated properly to id_data.
 
    args:
    ----------------
   
    conn_pathfileout: connection of  output averaging  sqlite file 
    
    output:
    ----------------

    Nothing

    """

    # distinct id_obs from header
    # count id_obs from header
    order_sql = """select 
                     count(distinct id_obs)
                   from header;"""
    cursor   = conn_pathfileout.cursor()
    cursor.execute(order_sql)
    result   = cursor.fetchone()
    distinct_id_obs_from_header = result[0]
    order_sql = """select 
                    count(id_obs)
                  from header;"""
    cursor   = conn_pathfileout.cursor()
    cursor.execute(order_sql)
    result   = cursor.fetchone()
    count_id_obs_from_header = result[0]
   
    # distinct id_obs from data
    # distinct id_data from data
    # count id_data from data
    order_sql = """select 
                     count(distinct id_obs)
                   from data;"""
    cursor   = conn_pathfileout.cursor()
    cursor.execute(order_sql)
    result   = cursor.fetchone()
    distinct_id_obs_from_data = result[0]
    order_sql = """select 
                     count(distinct id_data)
                   from data;"""
    cursor   = conn_pathfileout.cursor()
    cursor.execute(order_sql)
    result   = cursor.fetchone()
 
    distinct_id_data_from_data = result[0]
    order_sql = """select 
                    count(id_data)
                  from data;"""
    cursor   = conn_pathfileout.cursor()
    cursor.execute(order_sql)
    result   = cursor.fetchone()
    count_id_data_from_data = result[0]

    if (distinct_id_obs_from_header !=  distinct_id_obs_from_data): 
       raise RuntimeError("""Error: id_obs is not associated properly""")
    if (distinct_id_obs_from_header !=  count_id_obs_from_header): 
       raise RuntimeError("""Error: id_obs is in collision""")
    if (distinct_id_data_from_data  !=  count_id_data_from_data): 
       raise RuntimeError("""Error: id_data is in collision""")

      
def extract_winds_from_fst(fst_file, valid_time):
  
    """
    Extract the rotated winds from an standard file. 

    args:
    ----------------

    fst_file: str
        Standard file containing a model output for a single time.
    valid_time: datetime object
        validity date of data to read

    output:
    ----------------

    Dictionary with the winds, latitudes, longitudes and heights. 
    """
    
    # read std file
    wind_dict = fst_tools.get_data(file_name=fst_file,
                                   var_name="wind_vectors",
                                   datev=valid_time, 
                                   latlon=True)

    # wind
    model_latitudes = wind_dict["lat"]
    model_longitudes = wind_dict["lon"]
    model_uuwe = wind_dict["uuwe"]  # west-east   component of wind
    model_vvsn = wind_dict["vvsn"]  # south-north component of wind
    ip1_momentum = wind_dict["ip1_list"]  # list of momentum vertical levels

    # Get rid of diagnostic surface level
    # (this step should not be necessary for newer GEM outputs without diagnostic wind)
    model_uuwe = model_uuwe[:, :, 1:]
    model_vvsn = model_vvsn[:, :, 1:]
    ip1_momentum = ip1_momentum[1:]

    # altitude of gridpoints
    gz_dict = fst_tools.get_data(file_name=fst_file, 
                                 var_name="GZ", 
                                 ip1=ip1_momentum,
                                 datev=valid_time)
    model_heights = gz_dict["values"] * 10  # decameter to meters
    model_heights_average = model_heights.mean(axis=(0,1))

    ## We cap the model top at ~20000 m height to avoid saving unnecessary data.
    max_z_index = np.where (model_heights_average > 20000)[0][0]
    model_heights = model_heights[:, :, 0:max_z_index]
    model_uuwe    =    model_uuwe[:, :, 0:max_z_index]
    model_vvsn    =    model_vvsn[:, :, 0:max_z_index]

    model_longitudes = ((model_longitudes + 180) % 360) - 180

    model_dict= {'model_latitudes' : model_latitudes, 
                 'model_longitudes': model_longitudes, 
                 'model_uuwe'      : model_uuwe, 
                 'model_vvsn'      : model_vvsn,
                 'model_heights'   : model_heights} 

    return  model_dict

def index_from_latlon(grid_lats, grid_lons, lats , lons):
   
    """ Given the arrays of lat and lon calculates the nearest i,j
 
    args:
    ----------------
    
    grid_lats: array[n,m]
       Model latitudes grid
    grid_lons:array[n,m]
       Model longitudes gris
    lats: array of latitudes 
    lons: array of longitudes
    
    outpout:
    ----------------

    nearest_i: the nearest i from (lat,lon)
    nearest_j: the nearest j from (lat,lon)
 
    """
 
    radar_lats = np.array([lats])
    radar_lons = np.array([lons])
    grid_shape = grid_lats.shape
    #from latlon to xyz coords 
    proj_ll = ccrs.Geodetic()
    geo_cent = proj_ll.as_geocentric()
 
    grid_xyz = geo_cent.transform_points(proj_ll,
                                         grid_lons.flatten(),
                                         grid_lats.flatten())
 
    radar_xyz = geo_cent.transform_points(proj_ll,
                                          radar_lons.flatten(),
                                          radar_lats.flatten())
 
    #build kdtree from model grid
    kdtree = scipy.spatial.cKDTree(grid_xyz, balanced_tree=False)
 
    #search nearest neighbor using the tree
    _, indices = kdtree.query(radar_xyz, k=1)
    for ii, index in enumerate(indices):
        (nearest_i, nearest_j) = np.unravel_index(index, grid_shape)
        #print(f'radar lat/,on: {radar_lats[ii]:.3f},{radar_lons[ii]:.3f} --  nearest i,j: {nearest_i},{nearest_j}')
 
        return  nearest_i, nearest_j

def dict_constans():

    """ Dictionary with the constants used in radvelso
    args:
    ----------------
    Nothing 
    
    outpout:
    ----------------
    dictconstans: dictionary with the constants used in radvelso


    """

    dictconstans = {'approximate_radius_of_earth' : 6371007.1809}
    return dictconstans

def distance_between_two_points(lat1, lon1, lat2, lon2):
    
    """Distance between two point giving latitude longitude of the couple

    args:  
    ----------------

    lat1: latitude of the first observation
    lon1: longitude of the second observation
    lat2: latitude of the second observation
    lon2: longitude of the second observation
     
    output:
    ----------------
    
    distance2point: distance between two point giving latitude longitude of the couple     
    """

    # approximate radius of earth in km
    
    radius_of_earth = radvelso.qcavg.dict_constans()['approximate_radius_of_earth']

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance2point = radius_of_earth * c

    return distance2point

def clip_outputs_near_radar(model_dict, model_filename, i_radar, j_radar, model_resolution):

    """ Clip a large grid of model outputs to keep only datapoints 
        that are within a certain distance of a given radar

    args:
    ----------------

    model_dict: dictionary with all the information of the model 
    model_filename: model file name
    i_radar: i pixels the radar
    j_radar: j pixels the radar
    model_resolution: Estimation of model resolution
     
    output:
    ----------------
    
    model_radar: dictionary with model information around radar (~290 km)


    """
    
    model_latitudes  = model_dict['model_latitudes']
    model_longitudes = model_dict['model_longitudes']
    model_uuwe       = model_dict['model_uuwe'] 
    model_vvsn       = model_dict['model_vvsn']
    model_heights    = model_dict['model_heights']
    
    # estimation of delta ij 290000 an estimated value of maximum range considered
    delta = int(290000/model_resolution)

    #clip horizontally
    clipped_heights    =    model_heights[i_radar-delta:i_radar+delta, j_radar-delta:j_radar+delta, : ]
    clipped_uuwe       =       model_uuwe[i_radar-delta:i_radar+delta, j_radar-delta:j_radar+delta, : ]
    clipped_vvsn       =       model_vvsn[i_radar-delta:i_radar+delta, j_radar-delta:j_radar+delta, : ]
    clipped_latitudes  =  model_latitudes[i_radar-delta:i_radar+delta, j_radar-delta:j_radar+delta]
    clipped_longitudes = model_longitudes[i_radar-delta:i_radar+delta, j_radar-delta:j_radar+delta]

    clipped_dict = {'model_heights'   : clipped_heights,
                   'model_uuwe'       : clipped_uuwe,
                   'model_vvsn'       : clipped_vvsn,
                   'model_latitudes'  : clipped_latitudes,
                   'model_longitudes' : clipped_longitudes}

    return clipped_dict

def model2ppi_linear( model_latitudes,
                      model_longitudes,
                      model_heights,
                      ppi_latitudes,
                      ppi_longitudes,
                      ppi_heights,
                      model_vars=None,
                      valid_mask=None):
    """
    Interpolate the model output into the PPI scan using bilinear interpolation.

    (Based on Dominik Jacques interpolation routine)

    Args:
    ----------------

    model_latitudes: array[lon,lat]
        Model latitudes in degrees.
    model_longitudes: array[lon,lat]
        Model longitudes in degrees.
    model_heights: array[lon,lat, level]
        Model height in meters ASL.
    ppi_latitudes: array[rays,bins]
        Radar bin latitudes in degrees.
    ppi_longitudes: array[rays,bins]
        Radar bin longitude in degrees.
    ppi_heights: array[rays,bins]
        Radar bin heights in meters ASL.
    model_vars: array[lon, lat, level] or list of arrays
        List of model data to interpolate. 
        Each element of the list corresponds to a different variable.
    invalid_mask: array[rays,bins]
        Mask indicating the invalid values in the PPI.
    
    output:
    ----------------
    model_vars_at_ppi: array[rays,bins]
        model data interpolated for ppi


    """

    if model_vars is None:
        raise ValueError("The list of model variables to interpolate cannot be emtpy.")

    if not isinstance(model_vars, (tuple, list)):
        model_vars = [model_vars]
    # IMPORTANT! Only locations with valid values are interpolated
    nrays, nbins = ppi_latitudes.shape
    nz = model_heights.shape[2]
    if valid_mask is None:
        valid = np.ones_like(ppi_latitudes, dtype=bool)
    else:
        valid = ~valid_mask

    # Define grids
    ppi_grid = np.stack((ppi_longitudes[valid], ppi_latitudes[valid]), axis=1)
    n_valid_ppi_points = ppi_grid.shape[0]
    model_grid = np.stack((model_longitudes.ravel(), model_latitudes.ravel()), axis=1)

    # 1. The model-> PPI interpolation is done by first interpolating each model level at the radar bins lats/lons (the PPI grid).
    # Then, we interpolate along the vertical at the bins hights.
    # This approach is faster than a 3D interpolation.

    def interpolate2D(data_values, input_grid):
        """Interpolate model data into the ppi grid."""
        interpolator = LinearNDInterpolator(input_grid, data_values.ravel())
        res = interpolator(ppi_grid)
        return res, interpolator.tri

    # [n_valid_ppi_points, nz]
    model_height_at_ppi = np.zeros((n_valid_ppi_points, nz)).copy()
    model_vars_at_ppi3D = [model_height_at_ppi.copy() for _ in model_vars]

    # Iterate over vertical levels and interpolate along the horizontal
    tri = model_grid
    for z in range(model_vars[0].shape[2]):
        model_height_at_ppi[:, z], tri = interpolate2D(model_heights[:, :, z], tri)
        for var_idx, var in enumerate(model_vars):
            model_vars_at_ppi3D[var_idx][:, z], tri = interpolate2D(
                var[:, :, z].ravel(), tri)

    # 2. Interpolate the data in the vertical
    z_diff = model_height_at_ppi - ppi_heights[valid][:, None]

    # Variables dimensions:
    # z_diff: [n_valid_ppi_points, nz]
    # model_height_at_ppi: [n_valid_ppi_points, nz]
    nan_diff = np.where(z_diff < 0.0, np.nan, z_diff)
    within_bounds = np.isfinite(nan_diff).any(axis=1)
    outside_bounds = ~within_bounds

    outside_bounds_2d_mask = np.zeros_like(valid)

    idx = np.arange(valid.size)
    idx = idx[valid.ravel()][outside_bounds]
    if len(idx) > 0:
        outside_bounds_2d_mask_flat = outside_bounds_2d_mask.reshape(-1)
        outside_bounds_2d_mask_flat[idx] = True

    nan_diff[outside_bounds] = 0

    k_just_above = np.nanargmin(nan_diff, axis=1)
    k_just_below = k_just_above - 1
    k_just_above[outside_bounds] = nz - 1
    k_just_below[outside_bounds] = nz - 2

    # points below model level
    too_low_inds = np.asarray(k_just_below < 0).nonzero()
    if len(too_low_inds[0]) >= 0:
        k_just_above[too_low_inds] = 1
        k_just_below[too_low_inds] = 0

    # k_just_below: [n_valid_ppi_points,]
    ii = np.arange(n_valid_ppi_points)

    vert_interp_weights = z_diff[ii, k_just_above] / (
        model_height_at_ppi[ii, k_just_above] - model_height_at_ppi[ii, k_just_below])

    def interp_vertically(data_in_3d):
        data_1d_interpolated = (
            vert_interp_weights * data_in_3d[ii, k_just_below]
            + (1.0 - vert_interp_weights) * data_in_3d[ii, k_just_above])

        data2d = np.zeros((nrays, nbins))
        data2d[valid] = data_1d_interpolated
        data2d[outside_bounds_2d_mask] = np.nan
        return data2d

    # Interpolate variables
    model_vars_at_ppi = tuple(interp_vertically(var) for var in model_vars_at_ppi3D)

    if len(model_vars_at_ppi) == 1:
        return model_vars_at_ppi[0]

    return model_vars_at_ppi

    
def model2ppi_interpolation(model_radar, ppi_radar, elevation):

    """  calculation of the doppler velocity operator obtained from the interpolation of
         the ppi and the model
    
    args:
    ----------------
    
    model_radar: dictionary with model information about the radar model
    ppi_radar: dictionary with radar ppi information

    output:
    ----------------

    model_velocity: velocity model  from the ppi-related model


    """

    data_mask   = np.logical_not(ppi_radar['ppi_velocity']!=-9999.)

    # ppi&model
    model_uuvv = model2ppi_linear(model_radar['model_latitudes'],
                                  model_radar['model_longitudes'],
                                  model_radar['model_heights'],
                                  ppi_radar['ppi_latitudes'],
                                  ppi_radar['ppi_longitudes'],
                                  ppi_radar['ppi_heights'],
                                  model_vars= [model_radar['model_uuwe'], model_radar['model_vvsn']],
                                  valid_mask= data_mask )
                                               


    model_uuInterpolate = model_uuvv[0]
    model_vvInterpolate = model_uuvv[1]
    dim1 = len(ppi_radar['ppi_heights'])
    dim2 = len(ppi_radar['ppi_heights'][0])
    ppi_azimuths = np.broadcast_to(ppi_radar['ppi_azimuths'][:,np.newaxis], (dim1,dim2))  
    # Doppler velocity is the projection of wind along direction of radar beam
    # Positive values indicates velocities "away" from the radar
    model_velocity = (model_uuInterpolate*np.sin(np.radians(ppi_azimuths)) +
                          model_vvInterpolate*np.cos(np.radians(ppi_azimuths)))*np.cos(np.radians(elevation))
    return  model_velocity

def get_model_velocity_interpolated(this_vol_scan_time,
                                    nameradar,
                                    model_files_list, 
                                    model_valid_date_list,
                                    assim_T0,
                                    assim_window_width,
                                    ppi_radar,
                                    pathoutpkl,
                                    elevation):
  
    """ given a floor model and a ceil model, linear interpolation for a time between them

    args:
    ----------------
    model_filenames: str of floor and ceil velocity model
    dt_model_time: time from observation to model time
    ppi_radar: dictionary with ppi information 
    model_radar: dictionary with model information about the radar model

    output:
    ----------------

    model_velocity_interpolated: velocity model interpolated from floor and ceil velocity model

    """
    files_before_after, dt_before_after = surrounding_model_files(this_vol_scan_time, 
                                                                  model_files_list, 
                                                                  model_valid_date_list,                                                   assim_T0,
                                                                  assim_window_width)
    
    file = open(f"{pathoutpkl}/wind_dict_{nameradar}_{os.path.basename(files_before_after[0])}.pkl",'rb')
    model_radar_floor = pickle.load(file)
    file.close()
    file = open(f"{pathoutpkl}/wind_dict_{nameradar}_{os.path.basename(files_before_after[1])}.pkl",'rb')
    model_radar_ceil = pickle.load(file)
    file.close()

    model_velocity_floor  = model2ppi_interpolation(model_radar_floor, ppi_radar,elevation)
    model_velocity_ceil   = model2ppi_interpolation(model_radar_ceil, ppi_radar,elevation)

    t_floor = 0.
    t_ceil = 900 #second
    Diff = model_velocity_ceil - model_velocity_floor
    dt =  dt_before_after[0]
    model_velocity_interpolated = model_velocity_floor+ Diff * ((dt) / (t_ceil -  t_floor))
    # convert nan value to zero
    nodata_mask = np.where(ppi_radar['ppi_velocity']==-9999.)

    model_velocity_interpolated[nodata_mask] = -9999.
    return model_velocity_interpolated

def get_ppi(conn_filememory):

    """ dictionary ppi infromation
    
    args:
    ----------------

    conn_filememory: connection of memory  with ppi infromation

    output:
    ----------------
    
    ppi_radar: dictionary with radar ppi information


    """

    c = conn_filememory.cursor()
    c.row_factory = sqlite3.Row
    
    # all information that remains the same for this one PPI
    order_sql = '''select  
                     center_elevation, 
                     lat,
                     lon,
                     antenna_altitude,
                     nyquist,
                     half_delta_range,
                     range_start,
                     range_end
                    
                   from
                     header
                     natural join data;'''

    result_header = c.execute(order_sql).fetchone()
    elevation = result_header[0] 
    radar_lat = result_header[1]
    radar_lon = result_header[2]
    hrad      = result_header[3]
    nyquist   = result_header[4]


    half_delta_range = result_header[5]
    range_start      = result_header[6]
    range_end        = result_header[7]

    order_sql = '''select 
                     range,
                     obsvalue,
                     center_azimuth,
                     id_data,
                     quality_index
                   from
                     data
                     natural join header ;'''
    result_data = c.execute(order_sql).fetchall()

    ranges    = np.array([row[0] for row in result_data])
    obsvalues = np.array([row[1] for row in result_data])
    azimuths  = np.array([row[2] for row in result_data])
    id_datas  = np.array([row[3] for row in result_data])
    q_index   = np.array([row[4] for row in result_data])

    no_data = -9999.
    delta_azimuth = .5
    azimuth_arr = np.arange(0., 360., delta_azimuth)+delta_azimuth/2.
    n_azimuths = azimuth_arr.size

    delta_r =  int(2*half_delta_range)
    min_range = range_start 
    max_range = range_end

    range_bounds_arr = np.arange(min_range, max_range+delta_r, delta_r)
    range_bin_arr = range_bounds_arr[0:-1] + (range_bounds_arr[1:] - range_bounds_arr[0:-1])/2
    n_range_bins = range_bin_arr.size

    ppi_velocity   = np.full((n_azimuths, n_range_bins),no_data)
    ppi_heights    = np.full((n_azimuths, n_range_bins),no_data)
    ppi_latitudes  = np.full((n_azimuths, n_range_bins),no_data)
    ppi_longitudes = np.full((n_azimuths, n_range_bins),no_data)
    ppi_q_index    = np.full((n_azimuths, n_range_bins),no_data)
    ppi_id_data    = np.full((n_azimuths, n_range_bins),no_data)
    ppi_ranges     = np.full((n_range_bins),no_data)
    ppi_azimuths   = np.full((n_azimuths),no_data)

    ppi_elevation  = np.full((n_azimuths, n_range_bins),no_data)
    ppi_qc = np.full((n_azimuths, n_range_bins),1)
    

    dist_earth = radar_tools.model_43(elev=elevation, dist_beam=ranges/1e3, hrad=hrad/1e3, want='dist_earth')
    obsvalue_longitudes, obsvalue_latitudes  = geo_tools.lat_lon_range_az(radar_lon ,radar_lat, dist_earth, azimuths)
    obsvalue_heights = radar_tools.model_43(elev=elevation, dist_beam=ranges/1e3, hrad=hrad/1e3, want='height')
    # zip is needed to join sqlite + obsvalue_heights +  obsvalue_longitudes in the loop
    zip_to_loop = zip(ranges, azimuths, obsvalues, obsvalue_heights, obsvalue_longitudes, obsvalue_latitudes, id_datas, q_index)

    for rnge, azimuth, obsvalue, heights, obsvalue_longitude, obsvalue_latitude, id_data, q_ind in  zip_to_loop:
        ind_range   = (np.abs(range_bin_arr - rnge)).argmin()
        ind_azimuth = (np.abs(azimuth_arr - azimuth)).argmin()

        
        ppi_velocity[ind_azimuth, ind_range]   = obsvalue
        ppi_heights[ind_azimuth, ind_range]    = heights 
        ppi_longitudes[ind_azimuth, ind_range] = obsvalue_longitude
        ppi_latitudes[ind_azimuth, ind_range]  = obsvalue_latitude 
        ppi_q_index[ind_azimuth, ind_range]    = q_ind
        ppi_id_data[ind_azimuth, ind_range]    = id_data
        ppi_ranges[ ind_range]                 = rnge
        ppi_azimuths[ind_azimuth]              = azimuth  
        ppi_elevation[ind_azimuth, ind_range]  = round(elevation,2)

    ppi_radar = {'ppi_azimuths'   : ppi_azimuths, 
                 'ppi_velocity'   : ppi_velocity,
                 'ppi_heights'    : ppi_heights,
                 'ppi_longitudes' : ppi_longitudes,
                 'ppi_latitudes'  : ppi_latitudes,
                 'ppi_azimuths'   : ppi_azimuths,
                 'ppi_ranges'     : ppi_ranges,
                 'ppi_elevation'  : ppi_elevation,
                 'radar_lat'      : radar_lat,
                 'radar_lon'      : radar_lon,
                 'nyquist'        : nyquist,
                 'ppi_qc'         : ppi_q_index,
                 'ppi_id_data'    : ppi_id_data
                 }
    return ppi_radar


def make_process_dealisaing( ppi_radar, 
                             model_velocity_interpolated,
                             elevation, infile, this_datetime, stn,
                             kernel_az=3,
                             kernel_r=3, 
                             filter_threshold = 10):
 
    """ calculate the dealias velocity

    args:
    ----------------

    ppi_radar: dictionary with radar ppi information
    model_velocity_interpolated: velocity model interpolated from floor and ceil velocity model
   
    output:
    ----------------

    ppi_obsvalue_dealisaing: dealias velocity


    """
  
    # Delias
    _dealias = Dealias(ppi_radar['ppi_ranges'],
                       ppi_radar['ppi_azimuths'],
                       ppi_radar['ppi_elevation'], 
                       ppi_radar['ppi_velocity'].copy(),
                       ppi_radar['nyquist'])
    _dealias.initialize(model_velocity_interpolated , beta=0.25)
    _dealias.dealiase()


    nodata_mask   = np.where(ppi_radar['ppi_velocity'] == -9999.)

    
    ppi_radar['ppi_qc'][ nodata_mask ] = 0.4

    OmP =_dealias.dealias_vel - model_velocity_interpolated
    OmP[nodata_mask] = np.nan
    da = xr.DataArray(data=OmP, dims=("rays", "bins"))
    min_valid_bins = int(round(0.65 * kernel_az * (kernel_r + 2)))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)

        OmP_std = (
             da.rolling(
                          rays=kernel_az,
                          bins=kernel_r + 2,
                          center=True,
                          min_periods=min_valid_bins,
                         )
                         .std(skipna=True)
                         .values
                        )

    OmP_std[np.isnan(OmP_std)] = 0
    OmP_std[np.isnan(OmP)] = 0

    ppi_radar['ppi_qc'][(OmP_std > filter_threshold) & (ppi_radar['ppi_qc'] >0.4)] = 0.5

    mask_qc   = np.where(ppi_radar['ppi_qc']<0.6)

    ppi_obsvalue_dealias = ppi_radar['ppi_velocity'].copy()
    ppi_obsvalue_dealias[mask_qc] =-9999.
    ppi_obsvalue_dealias[np.isnan(ppi_obsvalue_dealias)] = -9999.

    return ppi_obsvalue_dealias

def flag_for_dealisaing(conn_filememory, id_data):

    """ delete observation from memory due to dealias
    
    args:
    ----------------

    conn_filememory: connection of memory  with ppi infromation
    id_data: id_data of observation

    output:
    ----------------

    Nothing, observation deleted from memory to calcula averaged

    """
    order_sql = """delete from data where ID_DATA = ?;"""
    conn_filememory.execute(order_sql,(int(id_data),)) 

def make_dealias(this_datetime,
                 model_files_list, 
                 model_valid_date_list,
                 assim_T0,
                 assim_window_width,
                 conn_ppi_db,
                 infile,
                 stn,
                 model_data_dir,
                 elevation,
                 pathoutpkl) :

    """ Determine observations that will not be taken into account in the average according to dealias
     
    args:
    ---------------
    
       -
    
    this_datetime: date of ppi
    conn_filememory: connection of memory  with ppi infromation
    filein: str of the sqlite file in
    stn: name of radar
    model_data_dir: str
       Directory where the model data is stored in fst format.
    model_radar: dictionary with model information about the radar model
    elevation: elevation of ppi

    output:
    ----------------

    Nothing: Determine observations as not assimilable

    """

    
    ppi_radar = get_ppi( conn_ppi_db)

    model_velocity_interpolated = get_model_velocity_interpolated(this_datetime,
                                                                  stn,
                                                                  model_files_list, 
                                                                  model_valid_date_list,
                                                                  assim_T0,
                                                                  assim_window_width,
                                                                  ppi_radar,
                                                                  pathoutpkl,
                                                                  elevation)


    ppi_obsvalue_dealisaing = make_process_dealisaing(ppi_radar,
                                                      model_velocity_interpolated, 
                                                      elevation, infile, this_datetime, stn)

    flag_index = np.where(ppi_obsvalue_dealisaing!=  ppi_radar['ppi_velocity'])
    # print (len(ppi_radar['ppi_id_data'][flag_index]), elevation)
    if np.any(flag_index):
        for obs in ppi_radar['ppi_id_data'][flag_index]:
            # remove obs in memory
            flag_for_dealisaing(conn_ppi_db, obs)
        conn_ppi_db.commit()

def get_model_resolution(wind_dict, latitude, longitude):

    """given a standard model file estimation of the resolution at a point defined by lat and lon

    args:
    ----------------
 
    model_latitudes:Array[n,m] of lotitudes from model
    model_longitudes:Array[n,m] of latitudes from model
    latitude: value of latitude
    longitude: value of longitude 


    output:
    ----------------
   
    model_resolution
    i_model_for_radar: i of model grid
    j_model_for_radar: j of model grid
    
    """
    model_latitudes  = wind_dict['model_latitudes']
    model_longitudes = wind_dict['model_longitudes']
    i_model_for_radar, j_model_for_radar = index_from_latlon(model_latitudes, 
                                                             model_longitudes,
                                                             latitude, 
                                                             longitude)
    model_resolution = distance_between_two_points(model_latitudes[i_model_for_radar,  j_model_for_radar], 
                                                   model_longitudes[i_model_for_radar, j_model_for_radar], 
                                                   model_latitudes[i_model_for_radar,  j_model_for_radar+1], 
                                                   model_longitudes[i_model_for_radar, j_model_for_radar+1])
   
    return model_resolution, i_model_for_radar, j_model_for_radar                                    
 


def save_pkl (name, tosave): 
 
    """ save a dictionary in a pickle file

    args:
    ----------------
    name: name of file to save
    tosave: Array to save

    output:
    ----------------
    nothing one file information to save

    """

    if os.path.exists(name):
        os.remove(name)
    f = open(name,"wb")
    # write the python object (dict) to pickle file
    pickle.dump( tosave, f)
    # close file
    f.close()

def get_date_from_filename(this_file, 
                           kind):
    """Compute validity date from a filename

    args:
    ----------------
    this_file: name of file to parse
    kind:      what kind of file ar we dealing with
    """
    file_bname = os.path.basename(this_file)
    if kind == 'G1':
        fcst_T0_date = datetime.datetime.strptime(file_bname[0:10], '%Y%m%d%H')
        minutes = int(file_bname[11:14])
        valid_date = fcst_T0_date + datetime.timedelta(seconds=minutes*60)

    elif kind == 'pickles':
       #write code here to get date from pickle name
       pass

    else:
        raise ValueError(f'Dont know what to do with kind={kind}')

    return valid_date


def savepkl_for_radardomain(nameradar, 
                            vol_scan_datetime_list,
                            this_radar_lat, 
                            this_radar_lon,
                            model_files_list,
                            model_valid_date_list,
                            assim_T0,
                            assim_window_width,
                            ops_run_name,
                            pathoutpickle):
    """ save a dictionary with models winds to interpolate for the radar in a pickle file

    args:
    ----------------
    nameradar: radar name
    vol_scan_datetime_list: list of datetimes of each volume scan
    this_radar_lat: latitude radar
    this_radar_lon: longitude radar
    model_outputs_for_dealiasing: path to models winds
    assim_T0: central time of assimilation window
    assim_window_width: width of assimilation window
    ops_run_name: name of operational run
    pathout: path to work
    output:
    ----------------
    nothing one pickle file for radar with models winds 

    """

    # Initialization wind dictionary with the full domain
    
    
    #make a list of available model files and their validity dates
    #trial_T0 = assim_T0 - datetime.timedelta(seconds=assim_window_width*3600)
    #search_pattern = os.path.join(model_outputs_for_dealiasing,trial_T0.strftime(model_files_search_pattern))
   # model_files_list = sorted(glob.glob(search_pattern))
    #if len(model_files_list) == 0:
    #     raise RuntimeError(f'No model files found for criterion: {search_pattern}')
    #model_valid_date_list = [ get_date_from_filename(this_file,ops_run_name) for this_file in model_files_list ] 

    # Extract winds around the radar and save it to pickle files
    print (nameradar)
    model_resolution = None
    for this_vol_scan_time in vol_scan_datetime_list:

        files_before_after, dt_before_after = surrounding_model_files(this_vol_scan_time, 
                                                                      model_files_list, 
                                                                      model_valid_date_list,
                                                                      assim_T0,
                                                                      assim_window_width)

        for this_model_file in files_before_after:
            
            if os.path.exists(f"{pathoutpickle}/wind_dict_{nameradar}_{os.path.basename(this_model_file)}.pkl"):
                 continue
            else:
     
                 model_filename = os.path.basename(this_model_file)
                 valid_time = model_valid_date_list[model_files_list.index(this_model_file)]
                 file = open(f"{pathoutpickle}/wind_dict_fulldomain_{model_filename}.pkl",'rb')
                 wind_dict_fulldomain = pickle.load(file)
                 file.close()

                 if model_resolution is None:
                     (model_resolution, 
                     i_model_for_radar, 
                     j_model_for_radar) = get_model_resolution(wind_dict_fulldomain,  
                                                               this_radar_lat,
                                                               this_radar_lon)


                 wind_dict_radardomain = clip_outputs_near_radar(wind_dict_fulldomain,
                                                                 model_filename,
                                                                 i_model_for_radar,
                                                                 j_model_for_radar,
                                                                 model_resolution)

                 save_pkl(f"{pathoutpickle}/wind_dict_{nameradar}_{os.path.basename(this_model_file)}.pkl", wind_dict_radardomain)

def savepkl_for_fulldomain(this_model_file,
                       model_files_list, 
                       model_valid_date_list,
                       pathoutpickle,
                       nameradar=None):
   
    """ save a dictionary with models winds to interpolate for the radar in a pickle file

    args:
    ----------------
    
    
    output:
    ---nameradar-------------

    """

    print (f"Extract model file: {os.path.basename(this_model_file)}")
    valid_time = model_valid_date_list[model_files_list.index(this_model_file)]
    wind_to_save = extract_winds_from_fst(this_model_file, valid_time)
    save_pkl(f"{pathoutpickle}/wind_dict_fulldomain_{os.path.basename(this_model_file)}.pkl", wind_to_save )

def get_model_valid_date_list(assim_T0, 
                              assim_window_width,
                              ops_run_name, 
                              model_files_search_pattern,
                              model_outputs_for_dealiasing):
    
    """ make a list of available model files and their validity dates

    args:
    ----------------
    
    
    output:
    ----------------

    """

    trial_T0 = assim_T0 - datetime.timedelta(seconds=assim_window_width*3600)
    search_pattern = os.path.join(model_outputs_for_dealiasing,trial_T0.strftime(model_files_search_pattern))
    model_files_list = sorted(glob.glob(search_pattern))
    if len(model_files_list) == 0:
        raise RuntimeError(f'No model files found for criterion: {search_pattern}')
    model_valid_date_list = [ get_date_from_filename(this_file,ops_run_name) for this_file in model_files_list ] 

    return model_files_list, model_valid_date_list



def compute_qcavg(assim_T0,
                  assim_window_width,
                  desired_radar_list,
                  infile_list, 
                  pathout, 
                  outfile_struc, 
                  ops_run_name, 
                  n_rays, 
                  delta_range,
                  n_cpus,
                  obs_percentage,
                  obs_nyquist,
                  model_outputs_for_dealiasing,
                  model_files_search_pattern):
    
    """launch computation of average volums scans, possibly in parallel
  
    args:
    ----------------

    assim_T0     : datetime object,  center time of the assimilation window
    assim_window_width : [hours] Width of the assimilation window
    desired_radar_list : list of radars to process
    infile_list  : list of input files to be superobbed
    pathout      : output average sqlite file(s) 
    outfile_struc: structure of output file name ; will be passed to strftime
    ops_run_name : name of operational run 
    n_rays       : number of rays
    delta_range  : delta range of the boxes
    n_cpus       : number of cpus for parallel execution, with n_cpus=1 joba are launched sequentially and dask is not invoked 
    obs_percentage : percentage of observation in the box to average
    obs_nyquist    : mac nyquist for processing AVG+dealias
    model_outputs_for_dealiasing : a path containing fst files with model with model winds. Setting this path will trigger dealiasing.
    model_files_search_pattern   : search pattern for model files
  
    output:
    ----------------

    Nothing
     Average sqlite file(s) are created with the '_thin' suffix
  
    """

    #flush fileout if it already exists
    pathfileout=f"{pathout}/{assim_T0.strftime(outfile_struc)}"
    if os.path.isfile(pathfileout):
        os.remove(pathfileout)
    if not os.path.isdir(pathout):
        os.mkdir(pathout)

    #flush fileout if it already exists for pickle files
    # TODO not sure we want to do this and/or do this here
    pathoutpickle= f'{pathout}/pickle_files'
    if os.path.isfile(pathoutpickle):
        os.remove(pathoutpickle)
    if not os.path.isdir(pathoutpickle):
        os.mkdir(pathoutpickle)
    
    #init large output file
    conn_pathfileout = sqlite3.connect(pathfileout)
    conn_pathfileout.execute("pragma temp_store = 2;")
    schema = find_schema('schema')
    with open(schema) as f:
        schema = f.read()
    conn_pathfileout.executescript(schema)
  
    print('Making a dict containing all volume scans present in the sqlite files.')
    vol_scan_dict = {}
    # vol_scan_dict[radar_name] = {'antenna_lat':45, 
    #                              'antenna_lon':-180, 
    #                              'datetime_list':[date1, date2, ..., date n]}
    vol_scan_list = []
    # vol_scan_list is a list of all volume scans that will that will be processed in parallel
    for this_sqlite_file in infile_list:
        with sqlite3.connect(this_sqlite_file) as conn_loops:
            for [radar_name, antenna_lat, antenna_lon] in conn_loops.execute("select distinct ID_STN, lat, lon  from header order by 1;").fetchall():
                
                if 'all' in  desired_radar_list:
                    pass
                elif radar_name not  in  desired_radar_list:
                    continue
                if radar_name not in vol_scan_dict.keys():
                    
                    vol_scan_dict[radar_name] = {}
                    vol_scan_dict[radar_name]['antenna_lat'] = antenna_lat
                    vol_scan_dict[radar_name]['antenna_lon'] = antenna_lon

                    # In Sqlite, the date associated with each "ray" of radar measurements 
                    # is the date at the end of the associated volume scan
                    order_sql = f"select distinct DATE, printf('%06d', TIME) from header where ID_STN = '{radar_name}';"
                    result = conn_loops.execute(order_sql).fetchall()
                    datetime_list  = sorted([datetime.datetime.strptime( f'{date_time[0]}{date_time[1]}', '%Y%m%d%H%M%S') for date_time in result])

                    vol_scan_dict[radar_name]['datetime_list'] = datetime_list

                    # Append this volume scan to vol_scan_list
                    for this_datetime in vol_scan_dict[radar_name]['datetime_list']:
                        vol_scan_list.append({ 'sqlite_src_file': this_sqlite_file, 
                                               'radar_name': radar_name,
                                               'this_datetime': this_datetime, 
                                             })

                           
    if len(vol_scan_list) == 0:
        raise RuntimeError("""List of volume scan to process is empty. 
                              Check that files are available and search criteria are correct.""")
    
    print ("len(vol_scan_list)",len(vol_scan_list))
    
    # Dealias Doppler velocities if a path was provided
    if model_outputs_for_dealiasing is not None:

        model_files_list, model_valid_date_list = get_model_valid_date_list(assim_T0, 
                                                          assim_window_width,
                                                          ops_run_name, 
                                                          model_files_search_pattern,
                                                          model_outputs_for_dealiasing)
    

 
        tc_0 = time.time()



        joblib.Parallel(n_jobs = 20)(joblib.delayed(savepkl_for_fulldomain) (this_model_file,
                                                                       model_files_list,
                                                                       model_valid_date_list,
                                                                       pathoutpickle) for this_model_file in model_files_list)

                                                                       
                                                                           
      
        tc_1 = time.time()
        print(f"Runtime wind dictionary: {round(tc_1-tc_0,4)} s")
        print(' Preparing pickle files of model data for dealiasing')
        # TODO use number of jobs from node ressources
        joblib.Parallel(n_jobs = 20)(joblib.delayed(savepkl_for_radardomain)(radar_name,
                                                                          vol_scan_dict[radar_name]['datetime_list'],
                                                                          vol_scan_dict[radar_name]['antenna_lat'],
                                                                          vol_scan_dict[radar_name]['antenna_lon'],
                                                                          model_files_list,
                                                                          model_valid_date_list,
                                                                          assim_T0,
                                                                          assim_window_width,
                                                                          ops_run_name,
                                                                          pathoutpickle) for radar_name in vol_scan_dict.keys())

        tc_1 = time.time()
        print(f"Runtime wind dictionary: {round(tc_1-tc_0,4)} s")
        #exit(0)


    print(' Make averaging template')
    #initialize template that will be used for averaging every PPIs
    min_range_in_ppi =  delta_range
    max_range_in_ppi = 240000.
    averaging_template = radvelso.fill_ray.fill_ray_dict(n_rays=n_rays,
                                                         min_range_in_ppi = min_range_in_ppi,
                                                         max_range_in_ppi = max_range_in_ppi,
                                                         delta_range= delta_range)
    
    save_pkl(f'{pathoutpickle}/averaging_template.pkl', averaging_template)
    tc_0 = time.time()
   # n_cpus = 1
    if n_cpus == 1:
        #serial execution, usefull for debugging
        print('Serial execution')
        for vscan in vol_scan_list:
            superobs(vscan['sqlite_src_file'],
                     vscan['radar_name'],
                     vscan['this_datetime'],
                     pathfileout, 
                     ops_run_name,
                     obs_percentage,
                     obs_nyquist,
                     pathoutpickle,
                     model_files_list, 
                     model_valid_date_list,
                     assim_T0,
                     assim_window_width,
                     model_outputs_for_dealiasing)
    else:

        print(f'Compute {len(vol_scan_list)} volume scans in parallel')
        joblib.Parallel(n_jobs = 40 )(joblib.delayed(superobs)(vscan['sqlite_src_file'],
                                                                 vscan['radar_name'],
                                                                 vscan['this_datetime'],
                                                                 pathfileout, 
                                                                 ops_run_name,
                                                                 obs_percentage,
                                                                 obs_nyquist,
                                                                 pathoutpickle,
                                                                 model_files_list, 
                                                                 model_valid_date_list,
                                                                 assim_T0,
                                                                 assim_window_width,
                                                                 model_outputs_for_dealiasing) for vscan in vol_scan_list)
    
    sample_file  = vol_scan_list[0]['sqlite_src_file']
    # create info and resume_tables in fileout
    create_info_midas_tables(sample_file, 
                             conn_pathfileout,
                             n_rays, 
                             delta_range,
                             ops_run_name,
                             obs_percentage,
                             obs_nyquist)   
    # improve searches with index tables
    create_index_tables_idobs_iddata(conn_pathfileout)
    # collision_test
    collision_test(conn_pathfileout)
    # close connection
    conn_pathfileout.close()
    tc_1 = time.time()
    print(f"Runtime total: {round(tc_1-tc_0,4)} s")

def arg_call():
    import argparse 

    parser = argparse.ArgumentParser()
    parser.add_argument('--assim_T0',  default='undefined', type=str,   help="YYYYMMDDHH center time of assimilation window")
    parser.add_argument('--assim_window_width', default=0.,          type=float, help="[hours] width of assimilation window")
    parser.add_argument('--desired_radar_list', nargs="+", default='all',          help="List of radars to process")
    parser.add_argument('--inputfiles', nargs="+", default='undefined',    help="input sqlite file to average")
    parser.add_argument('--pathin',       default='undefined', type=str,   help="directory where are input sqlite files")
    parser.add_argument('--infile_struc', default='*/%Y%m%d%H_ra',type=str,help="structure of input file name")
    parser.add_argument('--pathout',      default=os.getcwd(), type=str,   help="where averaged sqlite files will be put")
    parser.add_argument('--outfile_struc',default='%Y%m%d%H_superobbed_dvel_ground_radars.sqlite', type=str,   help="structure of output file name")
    parser.add_argument('--ops_run_name', default='undefined', type=str,   help="Name of operational run (will show up in rdb4_schema)" ) 
    parser.add_argument('--n_rays',       default=20,          type=int,   help="Number of rays for averaging" )
    parser.add_argument('--delta_range',  default=5000.,       type=float, help="Delta_range  for averaging" )
    parser.add_argument('--n_cpus',       default=1,           type=int,   help="Number of rays for averaging" )
    parser.add_argument('--obs_percentage',default=50,         type=float, help="Percentage of observation in the box to average" )
    parser.add_argument('--obs_nyquist'   ,default=100,        type=float, help="Nyquist for QC" )
    parser.add_argument('--model_outputs_for_dealiasing',default='undefined', type=str, help="Path of model outputs used for dealiasing" )
    parser.add_argument('--model_files_search_pattern',  default='undefined', type=str, help="search pattern for model files" )

    args = parser.parse_args()

    for arg in vars(args):
        print(f'--{arg}  {getattr(args, arg)}')


    #argument checking
    if args.assim_T0 == 'undefined':
        raise ValueError('Center time of assimilation window must be provided')
    else:
        args.assim_T0 = datetime.datetime.strptime(args.assim_T0, '%Y%m%d%H')

    if np.isclose(args.assim_window_width, 0.) :
        raise ValueError('Window width must be provided')

    if args.inputfiles != 'undefined':
        #if inputfiles argument is provided, we use that
        infile_list = args.inputfiles 

    elif args.pathin != 'undefined': 
        #alternatively, search for files with pathin+infile_struc 
        if not os.path.isdir(args.pathin):
            raise ValueError(f'pathin: {args.pathin} does not exist.')
        search_str = args.assim_T0.strftime(args.infile_struc)
        infile_list = glob.glob(f'{args.pathin}/{search_str}')

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

    if args.model_outputs_for_dealiasing == 'undefined':
        warning.warn("Model outputs for dealiasing are not specified, NO DEALIASING of Doppler velocities will be performed.")
        args.model_outputs_for_dealiasing = None
    else:
        if not os.path.isdir(args.model_outputs_for_dealiasing):
            raise ValueError('The provided path: "model_outputs_for_dealiasing" does not exist!')

    if args.model_files_search_pattern == 'undefined':
        raise ValueError('You mush specify a model_files_search_pattern')

   
    #sys.exit is used to the return status of main is catched and passed to caller
    sys.exit(compute_qcavg(args.assim_T0,
                           args.assim_window_width,
                           args.desired_radar_list,
                           infile_list, 
                           args.pathout, 
                           args.outfile_struc, 
                           args.ops_run_name, 
                           args.n_rays, 
                           args.delta_range, 
                           args.n_cpus,
                           args.obs_percentage,
                           args.obs_nyquist,
                           args.model_outputs_for_dealiasing, 
                           args.model_files_search_pattern))



if __name__ == '__main__':
    arg_call()
