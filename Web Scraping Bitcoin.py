import pandas as pd
import requests
import datetime
import os

# set the directory to our repository
cd = os.getcwd()
os.chdir(cd)

# initalisation of parameters
end_date = datetime.date.today()   # <-- today's date
days_back = 10   # <-- lookback window

# list of dates from the last 10 days
date_list = pd.date_range(end=end_date, periods=days_back) \
    .strftime("%d-%m-%Y").tolist()   # format dates as required by the API

# create a directory where to store all the files that we're going to generate
if not os.path.exists('data/btc'):
    os.makedirs('data/btc')

# loop through the list of dates and, at each cycle: 
# - make an HTTP request to the CoinGecko API 
# - retrieve the information we need in JSON format
# - save the data to a temporary DataFrame named "tmp_df"
# - add the current cycle's date to a new column name "date" in the DataFrame
# - save the temporary DataFrame to a .csv file in your local folder
for dt in date_list: 
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/history?date=' + dt
    r = requests.get(url)
    print('...loading '+str(dt)+' data | status code: '+str(r.status_code))
    tmp_df = pd.DataFrame.from_dict(r.json()['market_data']).reset_index()
    tmp_df['date'] = dt
    tmp_df.to_csv('data/btc/btc_'+str(dt)+'.csv', index=False)

os.listdir('data/btc')

# create a list object containing all the csv files we need
files = os.listdir('data/btc')

# cycle through all the elements in the directory and, at each cycle, load 
# them to a temporary DataFrame 'tmp_df' and append them to an empty 
# DataFrame 'df' 
df = pd.DataFrame([])
for file in files: 
    if file.endswith('.csv'):
        tmp_df = pd.read_csv('data/btc/' + file)
        df = pd.concat([df, tmp_df])
#save the df as a .csv
df.to_csv('data/dataframe.csv', index=False)
# remove all csv files from the 'btc' directory
for file in os.listdir('data/btc'): 
    os.remove('data/btc/' + file)