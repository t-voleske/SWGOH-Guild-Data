import gspread
from read_data import read_players_data, read_tickets_weekly, read_tickets_monthly
import pandas as pd
import os
import json
from dotenv import load_dotenv
load_dotenv()

filepath = os.getenv("FILEPATH_CREDENTIALS")

def floatify(x):
    if x == '':
        return '-'
    return float(x)
gc = gspread.service_account(filename=filepath) # type: ignore

def convert_to_readible(x):
    if x == '':
        return '-'
    return format(int(x), ',')
    #return str(format(int(x), ',')).replace(',', '.')

sh = gc.open("SON_Guild_Data")
ws = sh.sheet1
main = sh.worksheet("Main")
weekly = sh.worksheet("Tickets_weekly")
monthly = sh.worksheet("Tickets_monthly")

#Prepare data for Main sheet
df = pd.DataFrame(read_players_data(), columns=['nickname', 'last_activity', 'total_gp', 'raid_score', 'average_percent', 'zeffo_ready', 'tickets_lost_week', 'days_tickets_lost'])
df = df.fillna('')
df['average_percent'] = df['average_percent'].map(floatify)
df['total_gp'] = df['total_gp'].map(floatify)
df['raid_score'] = df['raid_score'].map(floatify)
print(df)

#Prepare data for weekly ticket sheet
df_weekly = pd.DataFrame(read_tickets_weekly(), columns=['nickname', 'tickets_lost', 'days_tickets_lost', 'full_days_lost'])
df_weekly = df_weekly.fillna('')

#Prepare data for monthly ticket sheet
df_monthly = pd.DataFrame(read_tickets_monthly(), columns=['nickname', 'tickets_lost', 'days_tickets_lost', 'full_days_lost'])
df_monthly = df_monthly.fillna('')

#Batch clear Main and then update
main.batch_clear(["A2:H51"])
main.update(range_name='A2:H51', values=df.values.tolist())

#Batch clear weekly/monthly and then update
weekly.batch_clear(["A2:D50"])
weekly.update(range_name='A2:D50', values=df_weekly.values.tolist())
monthly.batch_clear(["A2:D100"])
monthly.update(range_name='A2:D100', values=df_monthly.values.tolist())


#listified = df.values.tolist()
#print(listified)