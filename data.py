from dotenv import load_dotenv
from datetime import datetime
import requests
import pandas as pd
import os
import pytz

load_dotenv()
auth_token = os.getenv('OANDA_API_KEY')

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {auth_token}'
    }

url = "https://api-fxtrade.oanda.com/v3/instruments/XAU_USD/candles"
params = {
    'count': 1,
    'price': 'M',
    'granularity': 'H1'
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

candles = data['candles']

def UTC_10(time_str):
    utc_time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")
    utc_time = utc_time.replace(tzinfo=pytz.UTC)
    utc_plus_10 = utc_time.astimezone(pytz.timezone('Australia/Sydney'))
    return utc_plus_10.strftime("%Y-%m-%d %H:%M")

# Create a DataFrame
df_candles = pd.DataFrame([{
'time': UTC_10(candle['time'][:16]),
'open': float(candle['mid']['o']),
'high': float(candle['mid']['h']),
'low': float(candle['mid']['l']),
'close': float(candle['mid']['c']),
'volume': candle['volume']
} for candle in candles])

print(df_candles)