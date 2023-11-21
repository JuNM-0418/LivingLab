# Living Lab Data Upload Automation
import gspread
import time
import pandas as pd
import datetime

json_file_path = "token.json"
gc = gspread.service_account(json_file_path)
spreadsheet_url = None
doc = gc.open_by_url(spreadsheet_url)

worksheet = doc.worksheet("1-1. 전력량 (15min)")

file_list = {"309.csv": 2, "310.csv": 3, "313.csv": 4,
             "314.csv": 5, "315.csv": 6, "316.csv": 7}
# file_list = {"314.csv": 5, "315.csv": 6, "316.csv": 7}
day_step = 1
start_day = datetime.datetime.now() - datetime.timedelta(days=day_step)

for file in file_list:

    df = pd.read_csv(file, encoding='cp949')

    start_index = 0
    end_index = 0

    for i in range(1, len(df)-1, 1):
        day = datetime.datetime.strptime(df.loc[i][1][:-9], "%Y-%m-%d")
        if (start_day.day == day.day):
            start_index = i
            break

    for i in range(start_index, len(df)-1, 1):
        day = datetime.datetime.strptime(df.loc[i][1][:-9], "%Y-%m-%d")
        if (start_day.day != day.day):
            end_index = i
            break

    data = []
    if (file == "309.csv"):
        for i in range(start_index, end_index, 1):
            data.append(df.loc[i][1])
        for i in range(0, len(data), 1):
            worksheet.update_cell(i+2, 1, data[i])
            time.sleep(1)
    data = []
    for i in range(start_index, end_index, 1):
        data.append(df.loc[i][12])
    for i in range(0, len(data), 1):
        worksheet.update_cell(i+2, file_list[file], data[i])
        time.sleep(1)
