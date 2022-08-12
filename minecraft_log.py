# ! pip install gspread gspread-dataframe oauth2client gspread-formatting
from email import message
from venv import create
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials as sac
from  gspread_formatting import CellFormat
import re
import pandas as pd
import numpy as np
from datetime import date
import gzip

today = str(date.today())
def connect_google():
    # Set api key
    auth_json = 'minecraft-357407-fbea91beb3ee.json'
    # Set scopes
    gs_scopes = ['https://spreadsheets.google.com/feeds']
    # 以金鑰及操作範圍設定憑證資料
    cr = sac.from_json_keyfile_name(auth_json, gs_scopes)
    # 取得操作憑證
    gc = gspread.authorize(cr)
    # 以 url 開啟試算表
    gsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1rCPCPSuPYjyDg4jfGbMVZmh-cOli4xoPIca5nwfvam4/edit#gid=0')
    # 創建工作表
    try:
        worksheet = gsheet.add_worksheet(title=f"{today}", rows="100", cols="20")
    except:
        pass
    # 選擇工作表1
    wks = gsheet.worksheet(f"{today}")
    return wks

# def un_gz_rt_gs(file_name):
#     f_name = file_name.replace(".gz", "")
#     g_file = gzip.GzipFile(file_name)
#     open(f_name, "wb+").write(g_file.read())
#     g_file.close()
#     return f_name

def log(f_name):
    wks = connect_google()
    result = []
    # Open File
    row = []
    with open(f_name,"r",encoding='utf-8') as file:
        log = file.readlines()
    for logdata in log:
        if 'was slain by' in logdata and 'message' not in logdata:
            time = "".join(re.findall(r'\[\d+:\d+:\d+\]',logdata))
            time = [today+" "+time[1:-1]]
            person = list(re.findall(r"([^: ][\/*\.*\ *\&*\w]*) was slain by (.*)",logdata)[0])
            data = time + [person[1]] + [person[0]]
            row.append(data)
        else:
            continue
    df = pd.DataFrame(row,columns=['time','win','loss'])
    monsterlist = ['Fisherman','Shepherd','Villager','Blaze', 'Creeper', 'Drowned', 'Elder Guardian', 'Endermite', 'Evoker', 'Ghast', 'Guardian', 'Hoglin', 'Husk', 'Magma Cube', 'Phantom', 'Piglin Brute', 'Pillager', 'Ravager', 'Shulker', 'Silverfish', 'Skeleton', 'Slime', 'Stray', 'Vex', 'Vindicator', 'Warden', 'Witch', 'Wither Skeleton', 'Zoglin', 'Zombie', 'Zombie Villager', 'Enderman', 'Piglin', 'Spider', 'Cave Spider', 'Zombified Piglin', 'Ender Dragon', 'Wither','Iron Golem']
    for i in range(1,3):
        df.iloc[:,i] = df.iloc[:,i].replace(monsterlist,np.nan)
    df.dropna(inplace=True)
    loss = df["loss"].value_counts().to_dict()
    win = df["win"].value_counts().to_dict()
    df2 = pd.DataFrame.from_dict(win,orient='index',columns=['win_count']).reset_index().rename(columns={'index': 'Id'})
    df3 = pd.DataFrame.from_dict(loss,orient='index',columns=['loss_count']).reset_index().rename(columns={'index': 'Id'})
    df4 = pd.merge(df2,df3,how='outer',on=["Id","Id"]).fillna(0)
    df4['win_count'] = df4['win_count'].astype('int64')
    df4['loss_count'] = df4['loss_count'].astype('int64')

    # uses DEFAULT_FORMATTER
    fmt = CellFormat(horizontalAlignment='CENTER')
    format_cell_range(wks, 'A:Z', fmt)

    # 寫入 Google Sheet
    set_with_dataframe(wks, df)
    set_with_dataframe(wks, df4,row = 1,col=6)
log('latest.log')