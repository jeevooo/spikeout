import os, glob
import csv
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from pandas import datetime, DataFrame
from datetime import timedelta
import psycopg2
import pandas as pd
import datetime as dt
import io
import requests

def data_collection():
    url = 'https://analytics.usa.gov/data/live/all-pages-realtime.csv'
    username = 'postgres'
    password = '*********'
    host     = 'localhost'
    port     = '5432'            # default port that postgres listens on
    db_name = 'govtraffic'

    #dowload webtraffic data
    csv = requests.get(url).content #download desired .csv from site.
    datetimestamp = str(dt.datetime.now()) #get date time stamp of download.
    data = pd.read_csv(io.StringIO(csv.decode('utf-8'))) #convert downloaded url (python string) to a dataframe.

    #Maniuplate Data
    data = data[data.page.isin(['weather.gov/', 'ssa.gov/', 'usps.com/', 'irs.gov/', 'usajobs.gov/', 'medicare.gov/', 'nasa.gov/', 'va.gov/', 'defense.gov/', 'cdc.gov/'])]
    data = data.set_index('page').T #transpose so dataframe forms time series.
    data['Time'] = datetimestamp
    data = data.drop('page_title')
    col = data.columns.tolist()
    col = col[-1:] + col[:-1]
    data = data[col]

    #Convert Data types for querying
    data['Time'] = pd.to_datetime(data['Time'], errors = 'coerce')
    data['usps.com/'] = pd.to_numeric(data['usps.com/'], errors = 'coerce')
    data['weather.gov/'] = pd.to_numeric(data['weather.gov/'], errors = 'coerce')
    data['irs.gov/'] = pd.to_numeric(data['irs.gov/'], errors = 'coerce')
    data['ssa.gov/'] = pd.to_numeric(data['ssa.gov/'], errors = 'coerce')
    data['usajobs.gov/'] = pd.to_numeric(data['usajobs.gov/'], errors = 'coerce')
    data['va.gov/'] = pd.to_numeric(data['va.gov/'], errors = 'coerce')
    data['defense.gov/'] = pd.to_numeric(data['defense.gov/'], errors = 'coerce')
    data['nasa.gov/'] = pd.to_numeric(data['nasa.gov/'], errors = 'coerce')
    data['medicare.gov/'] = pd.to_numeric(data['medicare.gov/'], errors = 'coerce')
    data['cdc.gov/'] = pd.to_numeric(data['cdc.gov/'], errors = 'coerce')
    
    #Adjust time offset
    data['Time'] = data['Time'] - pd.DateOffset(hours = 4)

    #Adjust the time value
    data["Time"] = data["Time"].astype("datetime64[ns]")
    data['Time'] =  pd.to_datetime(data['Time'], format = '%Y-%m-%d %H:%M:S.%f')
    data['Time'] = data['Time'].values.astype('<M8[m]')    

    #Export Data
    #data.to_csv('govtraffic' + datetimestamp + '.csv')
    
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(username, password, host, port, db_name))
    print(engine.url)
    
    ## create a database (if it doesn't exist)
    if not database_exists(engine.url):
        create_database(engine.url)
    print(database_exists(engine.url))
    
    ## insert data into database from Python (proof of concept - this won't be useful for big data, of course)
    data.to_sql('traffic', engine, if_exists = 'append')

data_collection()

