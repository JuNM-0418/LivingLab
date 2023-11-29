# Living Lab Data Upload Automation
import gspread
import pandas as pd
import datetime

json_file_path = "token.json"
gc = gspread.service_account(json_file_path)
spreadsheet_url = ""
doc = gc.open_by_url(spreadsheet_url)

# 데이터를 입력할 구글 시트 시트이름
worksheet = doc.worksheet("1-1. 전력량 (15min)")

# 불러올 파일 딕셔너리
file_list = {"309.csv": 2, "310.csv": 3, "313.csv": 4,
             "314.csv": 5, "315.csv": 6, "316.csv": 7}


start_day = 28


tmp_data = [[], [], [], [], [], [], []]

# 데이터를 로드하여 필요한 부분만 추출하는 부분
for file in file_list:
    df = pd.read_csv(file, encoding='cp949')
    start_index = 0
    end_index = 0

# 원하는 데이터의 시작 인덱스 넘버를 저장
    for i in range(1, len(df)-1, 1):
        if (df.loc[i][1][:-9] == None or df.loc[i][1][:-9] == '' or df.loc[i][1][:-9] == ' '):
            start_index = i
            break

        # if (file == "309.csv" or file == "314.csv" or file == "316.csv"):
        #     target_day = datetime.datetime.strptime(
        #         df.loc[i][1][:-6], "%Y-%m-%d %H:%M:%S")
        # else:
        #     target_day = datetime.datetime.strptime(
        #         df.loc[i][1][:-9], "%Y-%m-%d")

        if (len(df.loc[i][1]) == 19):
            target_day = datetime.datetime.strptime(
                df.loc[i][1][:-9], "%Y-%m-%d")
        elif (len(df.loc[i][1]) == 16):
            target_day = datetime.datetime.strptime(
                df.loc[i][1][:-6], "%Y-%m-%d")
        else:
            target_day = datetime.datetime.strptime(
                df.loc[i][1][:-5], "%Y-%m-%d")

        if (start_day == target_day.day):
            start_index = i
            break

# 원하는 데이터의 끝 인덱스 넘버를 저장
    for i in range(start_index, len(df)-1, 1):
        if (df.loc[i][1][:-9] == None or df.loc[i][1][:-9] == '' or df.loc[i][1][:-9] == ' '):
            end_index = i
            break
        # if (file == "309.csv" or file == "314.csv" or file == "316.csv"):
        #     target_day = datetime.datetime.strptime(
        #         df.loc[i][1][:-6], "%Y-%m-%d")
        # else:
        #     target_day = datetime.datetime.strptime(
        #         df.loc[i][1][:-9], "%Y-%m-%d")

        if (len(df.loc[i][1]) == 19):
            target_day = datetime.datetime.strptime(
                df.loc[i][1][:-9], "%Y-%m-%d")
        elif (len(df.loc[i][1]) == 16):
            target_day = datetime.datetime.strptime(
                df.loc[i][1][:-6], "%Y-%m-%d")
        else:
            target_day = datetime.datetime.strptime(
                df.loc[i][1][:-5], "%Y-%m-%d")
        if (start_day != target_day.day):
            end_index = i
            break

# 시작 인덱스와 끝 인덱스를 가지고 데이터를 추출하여 임시 2차원 배열에 저장
    if (file == "309.csv"):
        for i in range(start_index, end_index, 1):
            tmp_data[0].append(df.loc[i][1])

    for i in range(start_index, end_index, 1):
        tmp_data[file_list[file]-1].append(df.loc[i][12])


# 데이터의 길이가 다른 경우를 위한 처리
data_length = len(tmp_data[0])
for data in tmp_data:
    if len(data) > data_length:
        for i in range(len(data) - data_length, 0, -1):
            data.pop(-1)
    elif len(data) < data_length:
        for i in range(data_length - len(data), 0, -1):
            data.append(0)

# 임시 2차원 배열을 pandas Dataframe으로 변경
wattage_data = pd.DataFrame({'저장시간': tmp_data[0],
                             '전력량 (309호)': tmp_data[1],
                             '전력량 (310호)': tmp_data[2],
                             '전력량 (313호)': tmp_data[3],
                             '전력량 (314호)': tmp_data[4],
                             '전력량 (315호)': tmp_data[5],
                             '전력량 (316호)': tmp_data[6]})


# 데이터 타입 변경
wattage_data = wattage_data.astype({'전력량 (309호)': 'float'})
wattage_data = wattage_data.astype({'전력량 (310호)': 'float'})
wattage_data = wattage_data.astype({'전력량 (313호)': 'float'})
wattage_data = wattage_data.astype({'전력량 (314호)': 'float'})
wattage_data = wattage_data.astype({'전력량 (315호)': 'float'})
wattage_data = wattage_data.astype({'전력량 (316호)': 'float'})
wattage_data = wattage_data.astype({'저장시간': 'str'})

# 데이터 업로드
worksheet.update([wattage_data.columns.values.tolist()] +
                 wattage_data.values.tolist())
