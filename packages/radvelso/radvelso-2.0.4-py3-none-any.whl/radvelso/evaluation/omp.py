#/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import math 
import ast 
import sqlite3
import sys
import math 
import numpy as np
from itertools import chain
import os
import glob

def omp(path):
  """"
     Makes images of the BIAS and STDDEV as a function of range or heighthe from a sqlite file(s) after being used in MIDAS. 

     path  :  path to sqlite file(s)
    
    ====================================
  """
  distance_radar = 250000.                                                             # [meters] Distance from the radar to the farthest point taken into account
  delta_range    = 500.                                                              # [meters] Delta range where BIAS and STDDEV are calculated
  radius         = 6371007.2                                                           # Earth Radius
  range_array    = np.arange(250,distance_radar+ delta_range, delta_range, dtype=float)  # Delta range array  where BIAS and STDDEV are calculated
 
 
 
  #######################################################
  # create one sqlite in memory from sqlite files  
  #######################################################
  conn2 = sqlite3.connect("file::memory:?cache=shared",uri=True)
  with open('schema') as f:
                schema = f.read()
  conn2.executescript(schema)
  directory = os.fsencode(path)
  pwd=os.getcwd()
  os.chdir(pwd)
  for file in glob.glob(path+"*_ra"):
      print (file)
      attachDatabaseSQL        = "ATTACH DATABASE ? AS db_all"
      dbfile  = (file,)
      conn2.execute(attachDatabaseSQL,dbfile )
      
      order_sql = """ insert into header 
                  select 
                    * 
                  from
                    db_all.header 
                  where 
                      
                     id_stn='casbv' """

      conn2.execute( order_sql) 
  #select associated data entries

      order_sql =""" insert into data  
                    select
                      *
                    from
                      db_all.data
                    where
                      id_obs in ( select 
                                    id_obs
                                  from header) and  NUMBER_OBS >=? """
      number_min_obs =1
      conn2.execute(order_sql,(number_min_obs,))
      conn2.commit()



      
     # order_sql = "INSERT into DATA( ID_DATA , ID_OBS, VCOORD, VARNO, VCOORD_TYPE, OBSVALUE, FLAG, OMP, OMA, OBS_ERROR, FG_ERROR, DELTA_AZM, DELTA_RANGE) SELECT ID_DATA+maxiddata, ID_OBS+MAXIDOBS, VCOORD, VARNO, VCOORD_TYPE, OBSVALUE, FLAG, OMP, OMA, OBS_ERROR,FG_ERROR, DELTA_AZM, DELTA_RANGE FROM  db1.DATA, lastiddata, lastidobs;"

      detachDatabaseSQL   = "DETACH DATABASE db_all"
      conn2.execute(detachDatabaseSQL)

  conn2.create_aggregate("stdev", 1, StdevFunc)
  # conn2.execute("CREATE INDEX idobs on data (id_obs)")
  id_stn ='casbv'

  reles = conn2.execute("select distinct NOMINAL_PPI_ELEVATION from header where id_stn =? order by 1 ;", ( id_stn,)).fetchall()
  reles = np.array(ast.literal_eval(','.join(map(str,chain.from_iterable(reles)))),dtype=float)
  ranges = conn2.execute("select distinct range from data natual join header where id_stn = 'casbv'order by 1 ;").fetchall()
  ranges  = np.array(ast.literal_eval(','.join(map(str,chain.from_iterable(ranges)))),dtype=float)

  print (ranges)
  id_stns = conn2.execute("select distinct id_stn from header order by 1 ;").fetchall()
  ########################################
  # radar station loop 
  #######################################
  id_stns =['casbv']
  for id_stn in id_stns:
     print ("id_stn", id_stn)
 
     order_sql =  " select lat,lon, NOMINAL_PPI_ELEVATION, id_stn from header  where id_stn = ? limit 1  "  
     conn2.row_factory = sqlite3.Row 
     cursor = conn2.cursor()
     cursor.execute( order_sql , ( id_stn,))
     result = cursor.fetchone()
     lat    = result['lat']
     lon    = result['lon']
     id_stn = result['id_stn']
     elev   = result['NOMINAL_PPI_ELEVATION']
     stn=id_stn[0]
     ########################################
     # elevation loop 
     ########################################
     for rele in reles:
  
        avgvcoord = np.zeros((len(range_array)))
        avgomp    = np.zeros((len(range_array)))
        stdevomp  = np.zeros((len(range_array)))
        count_obs = np.zeros((len(range_array)))
        avgvh     = np.zeros((len(range_array)))
        ########################################
        # range loop
        ########################################
        for range_step in ranges:
           i = np.where(range_array==range_step)
           cursor = conn2.cursor()
           ###############################################
           # look for values 
           # a = avg(range) ==> avg(height)
           # b = avg(omp)
           # c = stdev(omp)
           # d = count_obs
           ###############################################
           order_sql = "select round(avg(vcoord/1000),3),round(avg(omp),3),round(stdev(omp),3),count(*),range  from header natural join data where  abs(NOMINAL_PPI_ELEVATION-?) < .1 and abs(range-?)<0.1   and id_stn = ? ;"  # and abs(omp) < 10. ;"
           for  a,b,c,d,e in cursor.execute( order_sql ,(float(rele) ,range_step,id_stn, )):
              parameter  =[a,b,c,d, rele]
              print (a,b,c,d, rele,e)
              if (a!=None):
                 avgvcoord[i] = a 
                 avgvh[i]        = np.sqrt( a**2.+(radius+elev)**2.+(2.*a*(radius+elev)*np.sin(math.radians(rele)))) -(radius+elev)
              if (b!=None):
                 avgomp[i]    = b 
              if (c!=None):   
                 stdevomp[i]  = c
              if (d!=None):
                 count_obs[i]  = d 
             
   

        index_l   = np.where(avgomp==0)
        avgomp    = (np.delete(avgomp,index_l))
        avgvcoord = (np.delete(avgvcoord,index_l))
        stdevomp  = (np.delete(stdevomp,index_l))
        count_obs = (np.delete(count_obs,index_l))
        avgvh     = (np.delete(avgvh,index_l))
        print (avgomp)
        print (stdevomp)
        ################################################
        # Configuration of the imagen
        ################################################
        fig = plt.figure(figsize=(10,10))
        left=0.1
        width=.7
        ax1 = plt.axes([left, 0.15, width, 0.75])
        plt.title(id_stn)
        plt.xlabel('ELEVATION : '+str(round(rele,1)))
        plt.ylabel('RANGE [km]')
        ax1.grid(True)
        print (stdevomp,  avgvcoord )
        plt.plot( avgomp,    avgvcoord  , color='b',linestyle='--', marker='',ms=4)
        plt.plot( stdevomp,  avgvcoord  , color='r',linestyle='-' , marker='',ms=4)
        datapt=[]
        xlim=ax1.get_xlim()
        for y in  range(0,len(avgvcoord) ):
           datapt.append(( xlim[1]  , avgvcoord[y] ) )
        data_to_display = ax1.transData.transform
        display_to_ax = ax1.transAxes.inverted().transform
        if ( len(datapt) > 0):
           ax_pts = display_to_ax(data_to_display(datapt))
        for y in  range(0,len(avgvcoord) ):
           ix,iy=ax_pts[y]
           ax1.text(ix+.01,iy ,int(count_obs[y]) , fontsize =6,color='b' ,transform=ax1.transAxes )
        legendlist=['BIAS','STDDEV']
        l1=plt.legend(legendlist  ,columnspacing=1, fancybox=True,ncol=2,shadow = False,loc = (0.60, -0.10),prop={'size':12})
        ax1.set_xlim(-12,12)
        # ax1.set_ylim(0,300)
        plt.savefig('profile_range_'+str(stn)+'_'+str(round(rele,1))+'_.png',format='png')

        fig = plt.figure(figsize=(10,10))
        left=0.1
        width=.7
        ax1 = plt.axes([left, 0.15, width, 0.75])
        plt.title(id_stn)
        plt.xlabel('ELEVATION : '+str(round(rele,1)))
        plt.ylabel('HEIGHT [km]')
        ax1.grid(True)
        plt.plot( avgomp,   avgvh, color='b', linestyle='--', marker='o', ms=4)
        plt.plot( stdevomp, avgvh, color='r', linestyle='-' , marker='o', ms=4)
        datapt=[]
        xlim=ax1.get_xlim()
        for y in  range(0,len(avgvh) ):
           datapt.append(( xlim[1]  , avgvh[y] ) )
        data_to_display = ax1.transData.transform
        display_to_ax = ax1.transAxes.inverted().transform
        if ( len(datapt) > 0):
           ax_pts = display_to_ax(data_to_display(datapt))
        for y in  range(0,len(avgvcoord) ):
           ix,iy=ax_pts[y]
           ax1.text(ix+.01,iy  ,int(count_obs[y]) , fontsize =6,color='b' ,transform=ax1.transAxes )
       
        legendlist=['BIAS','STDDEV']
        l1=plt.legend(legendlist  ,columnspacing=1, fancybox=True,ncol=2,shadow = False,loc = (0.60, -0.10),prop={'size':12})

        ax1.set_xlim(-12,12)
        # ax1.set_ylim(0,70)
        plt.savefig('profile_height_'+str(stn)+'_'+str(round(rele,1))+'_.png',format='png')
        plt.close() 
  # close sqlite
  conn2.close()          


# Sqlite3 needs this class to calculate stddev
class StdevFunc:
    def __init__(self):
        self.M = 0.0
        self.S = 0.0
        self.k = 1

    def step(self, value):
        if value is None:
            return
        tM = self.M
        self.M += (value - tM) / self.k
        self.S += (value - tM) * (value - self.M)
        self.k += 1

    def finalize(self):
        if self.k < 3:
            return None
        return math.sqrt(self.S / (self.k-2))

def main(path):
   omp(path) 

if __name__ == '__main__':
     import argparse 
     print("Executing ")
     parser = argparse.ArgumentParser()
     parser.add_argument('-path',  action="store", dest="path",
        required=True, help=" sql file" , default="None")
     args = parser.parse_args()      
     main(args.path)
   

