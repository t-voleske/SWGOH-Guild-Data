import gspread
from read_data import read_players_data
import pandas as pd
import os
import json
from dotenv import load_dotenv
load_dotenv()

filepath = os.getenv("FILEPATH_CREDENTIALS")

def floatify(x):
    if x == '':
        return ''
    return float(x)
gc = gspread.service_account(filename=filepath) # type: ignore

sh = gc.open("SON_Guild_Data")
ws = sh.sheet1
main = sh.worksheet("Main")

print(sh.sheet1.get('A1'))

df = pd.DataFrame(read_players_data(), columns=['nickname', 'last_activity', 'total_gp', 'raid_score', 'average_percent', 'zeffo_ready', 'tickets_lost_week', 'days_tickets_lost'])
df = df.fillna('')
df['average_percent'] = df['average_percent'].map(floatify)
df['total_gp'] = df['total_gp'].map(floatify)
df['raid_score'] = df['raid_score'].map(floatify)
print(df)

main.batch_clear(["A2:H51"])
main.update(range_name='A2:H51', values=df.values.tolist())


#listified = df.values.tolist()
#print(listified)