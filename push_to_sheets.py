import gspread
from read_data import read_players_data, read_tickets_weekly, read_tickets_monthly, read_member_points
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

#get filepath for configuration.json for Google Spreadsheet API from .env file 
filepath = os.getenv("FILEPATH_CREDENTIALS")

#Helper function to cast to float and handle missing values
def floatify(x):
    if x == '':
        return '-'
    return float(x)

# Create gspread object to interact with spreadsheet API
gc = gspread.service_account(filename=filepath) # type: ignore

sh = gc.open("SON_Guild_Data") # open spreadsheet in gspread
main = sh.worksheet("Main") # gspread object for Main worksheet
weekly = sh.worksheet("Tickets_weekly") # gspread object for Tickets_weekly worksheet
monthly = sh.worksheet("Tickets_monthly") # gspread object for Tickets_monthly worksheet
points_weekly = sh.worksheet("Points_weekly") # gspread object for Points_weekly worksheet

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

#Prepare data for weekly points sheet
df_weekly_points = pd.DataFrame(read_member_points(), columns=['player_id', 'nickname', 'last_activity_p', 'average_percent_p', 'zero_raid_score', 'zeffo_ready', 'tickets_weekly', 'total_points'])
df_weekly_points = df_weekly_points.iloc[:, 1:]

#Batch clear Main and then update
main.batch_clear(["A2:H51"])
main.update(range_name='A2:H51', values=df.values.tolist())

#Batch clear weekly/monthly and then update
weekly.batch_clear(["A2:D52"])
weekly.update(range_name='A2:D52', values=df_weekly.values.tolist())
monthly.batch_clear(["A2:D52"])
monthly.update(range_name='A2:D52', values=df_monthly.values.tolist())

# Batch clear Points_weekly, then update
points_weekly.batch_clear(["A2:G52"])
points_weekly.update(range_name='A2:G52', values=df_weekly_points.values.tolist())


#listified = df.values.tolist()
#print(listified)