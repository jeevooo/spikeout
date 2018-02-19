import os, glob
import io
import csv
import requests
import datetime as dt
from pandas import datetime, DataFrame
from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import math

con = None
con = psycopg2.connect(database = dbname, user = username)
sql_query = """
SELECT * FROM spikeout;
"""

def get_data(sql_query, con):
    concatenated_df = pd.read_sql_query(sql_query,con)
    concatenated_df = concatenated_df.drop(['Unnamed: 0'], axis=1) #remove unecessary column
    
    # Remove seconds and limit timestamp to minutes. 
    concatenated_df["Time"] = concatenated_df["Time"].astype("datetime64[ns]")
    concatenated_df['Time'] =  pd.to_datetime(concatenated_df['Time'], format = '%Y-%m-%d %H:%M:S.%f')
    concatenated_df['Time'] = concatenated_df['Time'].values.astype('<M8[m]')
    
    # adjust time values for server offset; specific to my sampling
    t = '2018-01-19'
    t_df = pd.to_datetime (t)
    concatenated_df['Time'] = np.where(concatenated_df['Time'] >= t_df, concatenated_df['Time'] - pd.DateOffset(hours = 5), concatenated_df['Time'])
    
    return concatenated_df