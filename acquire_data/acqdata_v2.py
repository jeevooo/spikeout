import io
import csv
import requests
import datetime as dt
from pandas import datetime, DataFrame
from datetime import timedelta
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

#url = 'http://analytics.usa.gov/data/live/all-pages-realtime.csv' # url to download from analytics.usa.gov
#weblist = ['weather.gov/', 'ssa.gov/', 'usps.com/', 'irs.gov/', 'usajobs.gov/', 'medicare.gov/', 'nasa.gov/', 'va.gov/', 'defense.gov/', 'cdc.gov/']
#user = [ENTER USERNAME AS STRING]


def acqdata(url, weblist, user):
    
    """ This function is designed to acquire web traffic data from analytics.usa.gov and exports a data file with the selected weblist and associated active users at specific download time. 
    
    The data is returned as a dataframe""""
    
    #download webtraffic
    csv = requests.get(url).content #download desired .csv from site.
    datetimestamp = str(dt.datetime.now()) #get date time stamp of download.
    data = pd.read_csv(io.StringIO(csv.decode('utf-8'))) #convert downloaded url (python string) to a .csv.
    #data.to_sql('traffic_data_table', engine, if_exists='replace')
    
    #Maniuplate Data
    data[data.page.isin(weblist)]
    data = data.set_index('page').T
    data['Time'] = datetimestamp
    data = data.drop('page_title')
    col = data.columns.tolist()
    col = col[-1:] + col[:-1]
    data = data[col]
    
    #Export Data
    data.to_csv('govtraffic' + datetimestamp + '.csv')

    # Use Sqlalchemy to connect to database
    dbname = 'spikeout'
    username = user
    engine = create_engine('postgres://%s@localhost/%s'%(username,dbname))
    #print(engine.url)

    # insert data into database from Python
    data.to_sql('spikeout', engine, if_exists='append')
    
    return data