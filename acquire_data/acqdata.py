url = 'http://analytics.usa.gov/data/live/all-pages-realtime.csv' # url to download from analytics.usa.gov
weblist = ['weather.gov/', 'ssa.gov/', 'usps.com/', 'irs.gov/', 'usajobs.gov/', 'medicare.gov/', 'nasa.gov/', 'va.gov/', 'defense.gov/', 'cdc.gov/']


def acqdata(url, weblist):
    
    """ This function is designed to acquire web traffic data from analytics.usa.gov """"
    
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
    
    return data