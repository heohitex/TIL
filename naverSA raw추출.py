from datetime import datetime
from datetime import timedelta
import pandas as pd
from google.colab import drive   ## 구글드라이버 연동 코드
#저장할 시트 위치 지정
sheet_id = "1GwjlE_LE0B-bHFKWH9yj22CE3IuxrsGHC30P0kjIsmA"
worksheet_name = "pandas"



#날짜 입력
start_date = "2024-02-23"
end_date= "2024-02-24"
report_date =pd.date_range(start_date,end_date)


drive.mount('/content/drive')
campaign_ids=campaign_ids=[] # 캠페인 ID 입력
import time
import random
import requests
import sys
sys.path.append('/content/drive/Shareddrives/마케팅 그룹/(아카이브)DT팀/HWG/사이드프로젝트/리포트 자동화')
import signaturehelper
def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}

BASE_URL = 'https://api.naver.com'
API_KEY = ''
SECRET_KEY = ''
CUSTOMER_ID = ''

uri = '/stats' #SAMPLE API를 작성하신분이 uri라는 변수에 API 서비스를 입력해놓았고요, 아래 보시면 BASE_URL + uri과 uri변수를 합쳐서
# 요청에 사용되는 주소를 만들도록 하였습니다.
method = 'GET' #method='get'

from google.colab import auth
import gspread
from google.auth import default
#autenticating to google
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)




import pandas as pd

df=pd.DataFrame()
df_data={}
for campaign_id in campaign_ids:
    for x in report_date:
        day_ymd=x.strftime('%Y-%m-%d')
        day_input='"'+day_ymd+'"'

        r = requests.get(BASE_URL + uri, params={'ids': campaign_id,
                                                 'fields': '["salesAmt"]',
                                                 'timeRange': '{'+'"since":'+"{}".format(day_input)+','+'"until" :' +'{}'.format(day_input)+'}'},
                         headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

        # time.sleep(1)

        #딕셔너리로 넣기
        data=r.json()
        df_data['date']=day_ymd
        df_data['id']=campaign_id

        if data['data']!=[]:
            df_data['총비용']=data['data'][0]['salesAmt']

        else :
            df_data['총비용']=0


        df_data=pd.DataFrame(df_data,index=[0])
        df=pd.concat([df,df_data])
    #     'timeRange': '{"since":"2020-08-01","until":"2020-10-02"}'


df.sort_values('date',inplace=True)

uri = '/ncc/campaigns'
method = 'GET'
r= requests.get(BASE_URL + uri+'?ids={}'.format(campaign_ids[0]), headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
# nccCampaignId와 name을 추출하여 캠페인ID와 캠페인 이름을 매칭시킬 수 있음
r.json()
data=r.json()
#빈 딕셔너리에 키와 값 추가하기
#예제
empty_dict={}
empty_dict['key']='value'
empty_dict

cam_name={}
for x in campaign_ids:
    uri = '/ncc/campaigns'
    method = 'GET'
    r= requests.get(BASE_URL + uri+'?ids={}'.format(x), headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

    data=r.json()
    cam_name[data[0]['nccCampaignId']]=data[0]['name']

    # time.sleep(1)


camp_list=[]
for x in df['id']:
    for y in cam_name:
        if x==y:
            camp_list.append(cam_name[y])


df['캠페인']=camp_list

result_df=df

result_df=result_df[['date', '캠페인', '총비용']]

result_df["비용"]=result_df["총비용"]/1.1




sh = gc.open_by_key(sheet_id)
worksheet = sh.worksheet(worksheet_name)

# DataFrame에서 열 이름을 가져옵니다.
column_names = result_df.columns.values.tolist()

# 데이터의 각 행을 반복하고 각 행을 워크시트에 추가합니다.
for row in result_df.values.tolist():
    worksheet.append_row(row)
