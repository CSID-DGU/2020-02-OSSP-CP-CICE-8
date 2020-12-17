from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib
import requests
import pandas as pd
import xmltodict
import json
import datetime
import sqlite3
import os

DB_PATH = os.path.dirname(__file__) + '/CoronaBotDB'

today =datetime.datetime.now()

def five_days_ago(today):
    five = (today-datetime.timedelta(7)).strftime("%Y%m%d")
    return five

key = 'RI5ekmQZaQtJcWF%2BFp%2FjIPg3kaXeWQj0MfyFVPynolhE9rUNQjg%2FCdWF1GkZe0UWS63SVaRd26nbQxZMqWGfKQ%3D%3D'
url = f'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey={key}&'
queryParams = urlencode({ quote_plus('pageNo') : 1, quote_plus('numOfRows') : 10,quote_plus('startCreateDt') : today.strftime("%Y%m%d"),
                        quote_plus('endCreateDt') : today.strftime("%Y%m%d")})

url2 = url + queryParams
response = urlopen(url2)
results = response.read().decode("utf-8")

results_to_json = xmltodict.parse(results)
data = json.loads(json.dumps(results_to_json))

corona=data['response']['body']['items']['item']

# print(corona)
Date=[]
Region=[]
Local = []
Over = []
LOsum = []
# clear_cnt=[]
# care_cnt=[]
# death_cnt=[]
for i in corona:
    Date.append(i['stdDay'])
    Region.append(i['gubun'])
    Local.append(i['localOccCnt'])
    Over.append(i['overFlowCnt'])
    LOsum.append(int(i['localOccCnt']) + int(i['overFlowCnt']))

# print(Region)
# print(Date)
# print(Local)
# print(Over)
# print(LOsum)

df=pd.DataFrame([Date,Region,LOsum]).T
df.columns=['Date','Region', 'LOsum']
df=df.sort_values(by='LOsum', ascending=False)
print(df)

#
# df = df.drop(index=6)
#
# # print(df)
def create_db():
    con = sqlite3.connect(DB_PATH + '/newkorea.db')
    cursor = con.cursor()
    # Date 날짜 Region 지역 total 확진자수
    cursor.execute("CREATE TABLE region(Date text, Region text, total int)")
    con.commit()
    con.close()
#
def input_db():
    con = sqlite3.connect(DB_PATH + '/newkorea.db')
    cursor = con.cursor()
    length1 = df.shape[0]
    length2 = df.shape[1]
    for i in range(length1):
        row = []
        for j in range(length2):
            row.append(df.iloc[i, j])
        cursor.execute("INSERT INTO region VALUES(?, ?, ?)",
                       (row[0], row[1], row[2]))
    con.commit()
    con.close()
#
def refresh_db():
    con = sqlite3.connect(DB_PATH+'/newkorea.db')
    # con.execute("DROP TABLE korea")
    con.execute("DELETE FROM region").rowcount
    con.commit()
    con.close()
# create_db()
def regionupdater(): # 업데이트 함수
    refresh_db() # 디비 clean
    input_db() # 다시 7개 넣기(일주일치)

regionupdater()