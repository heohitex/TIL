#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


plt.rc('font', family="Malgun Gothic")
plt.rc('axes', unicode_minus=False)
from IPython.display import set_matplotlib_formats

set_matplotlib_formats('retina')


# In[3]:


raw = pd.read_csv("Dataset/final/funda_train.csv") #상점 신용카드 매출 예측 경진대회


# In[4]:


raw["region"] = raw["region"].fillna("기타 기타")
raw["type_of_business"] = raw["type_of_business"].fillna("기타")
raw["city"] = raw["region"].str.split(' ').str[0]
raw["gu"] = raw["region"].str.split(' ').str[1]


# In[5]:


raw['transacted_date'] = pd.to_datetime(raw['transacted_date'])


# In[6]:


raw["year"] = raw['transacted_date'].dt.year
raw["month"] = raw['transacted_date'].dt.month
raw["day"] = raw['transacted_date'].dt.day
raw["hour"] = raw["transacted_time"].str.split(":").str[0]
raw["year_month"] = raw['transacted_date'].dt.strftime('%Y-%m')


# In[7]:


raw["type_of_business"] = raw["type_of_business"].str.replace("기타 기타","기타")


# In[10]:


raw_a = raw[raw["card_company"] == "a"]
raw_b = raw[raw["card_company"] == "b"]
raw_c = raw[raw["card_company"] == "c"]
raw_d = raw[raw["card_company"] == "d"]
raw_e = raw[raw["card_company"] == "e"]
raw_f = raw[raw["card_company"] == "f"]
raw_g = raw[raw["card_company"] == "g"]
raw_h = raw[raw["card_company"] == "h"]


# In[8]:


raw.head()


# In[9]:


pd.options.display.float_format = '{:.5f}'.format


# # 카드사별 Count

# In[25]:


raw[["store_id","type_of_business", "region"]].nunique()


# In[30]:


# 카드사별 없는 업종
146 - raw.groupby(["card_company"])["type_of_business"].nunique()


# In[122]:


# d카드사에서 취급하지 않는 업종
df_business = raw.groupby(["type_of_business"])["card_company"].nunique().reset_index()
df_business[df_business["card_company"] < 8]


# In[31]:


# 카드사별 없는 가맹점 수
1967 - raw.groupby(["card_company"])["store_id"].nunique()


# In[32]:


#카드사별 없는 지역
181 - raw.groupby(["card_company"])["region"].nunique()


# In[118]:


df_region = raw.groupby(["region"])["card_company"].nunique().reset_index()
df_region[df_region["card_company"] < 8]


# In[103]:


#카드사별 최대 할부
print("a",sorted(raw_a["installment_term"].unique())[-1])
print("b",sorted(raw_b["installment_term"].unique())[-1])
print("c",sorted(raw_c["installment_term"].unique())[-1])
print("d",sorted(raw_d["installment_term"].unique())[-1])
print("e",sorted(raw_e["installment_term"].unique())[-1])
print("f",sorted(raw_f["installment_term"].unique())[-1])
print("g",sorted(raw_g["installment_term"].unique())[-1])
print("h",sorted(raw_h["installment_term"].unique())[-1])


# In[112]:


raw_f[raw_f["installment_term"] == 93]


# In[138]:


amount_top10 = raw.groupby(["type_of_business"])["amount"].sum().sort_values(ascending=False).reset_index().head(11)["type_of_business"].to_list()


# In[144]:


amount_top10


# In[153]:


#업종별 매출 Top 10 제외
raw_a_2 = raw_a[~raw_a["type_of_business"].isin(amount_top10)]
raw_b_2 = raw_b[~raw_b["type_of_business"].isin(amount_top10)]
raw_c_2 = raw_c[~raw_c["type_of_business"].isin(amount_top10)]
raw_d_2 = raw_d[~raw_d["type_of_business"].isin(amount_top10)]
raw_e_2 = raw_e[~raw_e["type_of_business"].isin(amount_top10)]
raw_f_2 = raw_f[~raw_f["type_of_business"].isin(amount_top10)]
raw_g_2 = raw_g[~raw_g["type_of_business"].isin(amount_top10)]
raw_h_2 = raw_h[~raw_h["type_of_business"].isin(amount_top10)]


# In[215]:


top10_a = raw_a_2.groupby(["type_of_business"])["amount"].sum().sort_values(ascending=False).head(10).reset_index()
top10_b = raw_b_2.groupby(["type_of_business"])["amount"].sum().sort_values(ascending=False).head(10).reset_index()
top10_c = raw_c_2.groupby(["type_of_business"])["amount"].sum().sort_values(ascending=False).head(10).reset_index()
top10_d = raw_d_2.groupby(["type_of_business"])["amount"].sum().sort_values(ascending=False).head(10).reset_index()
top10_e = raw_e_2.groupby(["type_of_business"])["amount"].sum().sort_values(ascending=False).head(10).reset_index()
top10_f = raw_f_2.groupby(["type_of_business"])["amount"].sum().sort_values(ascending=False).head(10).reset_index()
top10_g = raw_g_2.groupby(["type_of_business"])["amount"].sum().sort_values(ascending=False).head(10).reset_index()
top10_h = raw_h_2.groupby(["type_of_business"])["amount"].sum().sort_values(ascending=False).head(10).reset_index()
top10_a["card_company"] = "a"
top10_b["card_company"] = "b"
top10_c["card_company"] = "c"
top10_d["card_company"] = "d"
top10_e["card_company"] = "e"
top10_f["card_company"] = "f"
top10_g["card_company"] = "g"
top10_h["card_company"] = "h"


# In[219]:


#카드사별 업종별 매출 취합
top10_business_by_card = pd.concat([top10_a,top10_b,top10_c,top10_d,top10_e,top10_f,top10_g,top10_h])


# In[258]:


plt.figure(figsize=(10, 7))
sns.barplot(data=top10_business_by_card, x="card_company", y="amount", hue="type_of_business")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# In[299]:


plt.figure(figsize=(20, 8))
plt.xticks(rotation = 70 )
sns.barplot(data=top10_business_by_card, x="type_of_business", y="amount", hue="card_company")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# # 카드사별 업종별 특징
# 
# - 음식점 : '서양식 음식점업', '간이음식 포장 판매 전문점', '치킨 전문점', 
# - 교육 : '외국어학원', '기타 예술학원', '기타 교육지원 서비스업', '그 외 기타 분류 안된 교육기관'
# - 자동차 : '자동차 신품 타이어 및 튜브 판매업', '기타 자동차 신품 부품 및 내장품 판매업', '자동차 전문 수리업'
# - 식품 : '기타 산업용 농산물 도매업', '육류 소매업'
# - 의료 : '일반 병원', 
# - 패션/미용 : '섬유, 직물 및 의복액세서리 소매업', '화장품, 비누 및 방향제 소매업', '화장품 및 화장용품 도매업'
# - 건강 : '운동 및 경기용품 소매업', '그 외 기타 스포츠시설 운영업', '체력단련시설 운영업'
# - 기타 : '그 외 기타 분류 안된 상품 전문 소매업',  '가구 소매업', '상품 종합 도매업'

# In[305]:


top10_business_by_card["type_of_business"].nunique()


# In[319]:


result = []
for a in top10_business_by_card["type_of_business"]:
    if a in ['서양식 음식점업', '간이음식 포장 판매 전문점', '치킨 전문점']:
        a = "음식점"
    elif a in ['외국어학원', '기타 예술학원', '기타 교육지원 서비스업', '그 외 기타 분류 안된 교육기관']:
        a = "교육"
    elif a in ['자동차 신품 타이어 및 튜브 판매업', '기타 자동차 신품 부품 및 내장품 판매업', '자동차 전문 수리업']:
        a = "자동차"
    elif a in ['기타 산업용 농산물 도매업', '육류 소매업']:
        a = "식품"
    elif a in ['일반 병원']:
        a = "의료"
    elif a in ['섬유, 직물 및 의복액세서리 소매업', '화장품, 비누 및 방향제 소매업', '화장품 및 화장용품 도매업']:
        a = "패션/미용"
    elif a in ['운동 및 경기용품 소매업', '그 외 기타 스포츠시설 운영업', '체력단련시설 운영업']:
        a = "건강"
    else :
        a = "기타"
    result.append(a)

top10_business_by_card["category"] = result


# In[329]:


plt.figure(figsize=(15, 8))
sns.barplot(data=top10_business_by_card, x="card_company", y="amount", hue="category")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# ## 카드사별 주력 업종
# - A카드사 : 음식점, 교육
# - B카드사 : 패션/미용
# - C카드사 : 패션/미용
# - D카드사 : 음식점
# - E카드사 : 패션/미용, 교육
# - F카드사 : 자동차
# - G카드사 : 식료품
# - H카드사 : 의료

# In[ ]:




