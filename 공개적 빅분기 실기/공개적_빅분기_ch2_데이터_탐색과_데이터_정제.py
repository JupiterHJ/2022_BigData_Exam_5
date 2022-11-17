# -*- coding: utf-8 -*-
"""공개적 빅분기 CH2. 데이터 탐색과 데이터 정제.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1akq1ijo7btgiQkTcrvX3DP87F3GU55Yo
"""

data['sex'] = data['sex'].replace([1,2], ['Male', 'Female']) 
data['sex'].value_counts().plot(kind='pie')   #원그래프
data['sex'].value_counts().plot(kind='bar')   #막대그래프
data.hist(bins=100, figsize=(10,5))  #히스토그램
data.boxplot(column='salary', return_type='both')  #박스플롯
plt.scatter(data['sex'], data['salary'], alpha=1)  #스캐터

<이상값 제거>
Q1_salary = data['salary'].quantile(q=0.25)
Q3_salary = data['salary'].quantile(q=0.75)
IQR_salary = Q3_salary-Q1_salary
data_IQR = data[(data['salary']<Q3_salary+IQR_salary*1.5)&(data['salary']>Q1_salary-IQR_salary*1.5)]

<변환>
data['log_salary'] = np.log(data['salary'])
data['sqrt_salary'] = np.sqrt(data['salary'])

<결측값>
data.isnull()   
data.notnull()
data.isnull().sum()
data['salary'].isnull().sum()    #'salary'의 결측 개수 합
data.notnull().sum(1)          #각각 행별로 결측 개수 합

<결측값 제거>
data_del_row = data.dropna(axis=0)   #행(가로)
data_del_col = data.dropna(axis=1)  #열(세로)
data[['salary']].dropna()   #행,열

<결측값 대체>
data_0 = data.fillna(0)   #0으로 대체
data_ffill = data.fillna(method='ffill')   #앞의 값으로 대체
data_bfill = data.fillna(method='bfill')   #뒤의 값으로 대체
data_mean = data.fillna(data.mean())   #평균으로 대체
data_mean = data.fillna(data.median())   #중간값으로 대체
data2['sales_new'] = np.where(pd.notnull(data2['sales'])==True, data2['sales'], data2['salary'])

#최종
import numpy as np
import pandas as pd

data = pd.read_csv('house_raw.csv')

new_data = data[(data['bedrooms']<0.4) & (data['households']<6) & (data['rooms']<10)]
new_data.hist(bins=10, figsize=(15,10))
#data_rooms = data[data['rooms']<20]
#data_rooms['rooms'].hist(bins=50, figsize=(10,5))
#print(data['rooms'].value_counts().sum())
#print(data_rooms2['rooms'].value_counts().sum())

X = new_data[new_data.columns[0:5]]
y = new_data[["house_value"]]

#라이브러리 불러오기
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=42)

#데이터 정규화
from sklearn.preprocessing import MinMaxScaler  
scaler_minmax = MinMaxScaler()
scaler_minmax.fit(X_train)
X_scaled_minmax_train = scaler_minmax.transform(X_train)
X_scaled_minmax_test = scaler_minmax.transform(X_test)

#선형모델을 적용
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_scaled_minmax_train, y_train)

#훈련데이터 정확도 확인: 55%
pred_train = model.predict(X_scaled_minmax_train)
print("훈련 데이터 정확도", model.score(X_scaled_minmax_train, y_train))

#훈련데이터 정확도 확인: 55%
pred_test = model.predict(X_scaled_minmax_test)
print("테스트데이터 정확도", model.score(X_scaled_minmax_test, y_test))

new_data.to_csv('housing_price.csv', index=False)

"""#1. 단변량 데이터 검색

1) 범주형 자료
"""

import pandas as pd
data = pd.read_csv('EX_CE0Salary.csv', encoding='utf-8')  #한글깨짐방지
data.info()                        #정보

data.head()

data['sex'] = data['sex'].replace([1,2], ['Male', 'Female'])  #숫자일때 문자로 대체
data['sex'].value_counts()         #범주별 빈도

import matplotlib.pyplot as plt
data['sex'].value_counts().plot(kind='pie')   #원그래프

data['sex'].value_counts().plot(kind='bar')   #막대그래프

"""2) 연속형 자료"""

data.describe()    #변수별 요약통계량

data.skew()    #왜도 : 양의값. 우측꼬리분포. 0이면 정규분포와 비슷, 2면 한쪽으로 치우쳐있음.

data.kurt  #첨도

#기술통계량: count(NA 제외한 값의 수를 반환)
#min, max, argmin(최소 갖고 있는 색인의 위치), argmax, idxmin(최소 갖고 있는 색인의 값), idxmax
#quantile(0~1분위수), sum, mean, median, var(분산), mad(절대평균편차), std(표준편차), skew(왜도), kurt(첨도)
#cumsum(누적합), cummin(누적 최소값), cummax, cumprod(누적곱), diff(1차 산술차), pct_change(퍼센트 변화율)
#corr(상관관계), cov(공분산)

import matplotlib.pyplot as plt
#data.hist(bins=50, figsize(20,15))   #bins구간너비, figsize도표크기
data['salary'].hist(bins=100, figsize=(10,5), color='y')

"""#2. 이변량 데이터 검색"""

data.corr()        #지정안하면 pearson피어슨 방법
data.corr(method="spearman")   #spearman
data.corr(method="kendall")    #켄달

import matplotlib.pyplot as plt
plt.scatter(data['sex'], data['salary'], alpha=1)
plt.show()

data.groupby('sex')[['salary']].describe()

"""#3. 이상치 처리"""

data.boxplot(column='salary', return_type='both')
#data.boxplot(column='salary', return_type='axes')
#data.boxplot(column='salary', return_type='dict')

Q1_salary = data['salary'].quantile(q=0.25)
Q3_salary = data['salary'].quantile(q=0.75)
IQR_salary = Q3_salary-Q1_salary
IQR_salary

data_IQR = data[(data['salary']<Q3_salary+IQR_salary*1.5)&(data['salary']>Q1_salary-IQR_salary*1.5)]
data_IQR['salary'].hist(bins=10, figsize=(10,5))

data_IQR.corr()

plt.scatter(data_IQR['sex'], data_IQR['salary'], alpha=0.5)
plt.show()

"""#4. 변수 변환
- log 변환, 제곱근 변환
"""

#로그 변환
import numpy as np
data['log_salary'] = np.log(data['salary'])
data.hist(bins=50, figsize=(10,5))

#제곱근 변환
data['sqrt_salary'] = np.sqrt(data['salary'])
data.hist(bins=50, figsize=(15,10))

"""#5. 결측치 처리

1) 결측치 개수
"""

#NaN의 결측값
data.isnull()    #결측이면 True, 아니면 False

data.notnull()    #결측이면 False, 아니면 True

data.isnull().sum()    #결측 개수
data['salary'].isnull().sum()    #결측 개수

data.notnull().sum()    #결측 개수
data['salary'].notnull().sum()    #결측 개수

data.notnull().sum(1)  #1행의 결측값 아닌거 개수
data['valid']=data.notnull().sum(1)
data

"""2) 결측값 제거: dropna()
- 결측값이 있는 행 제거, 결측값이 있는 열 제거, 결측값이 있는 특정 행 또는 열 제거

가) 결측값이 있는 행(가로) 제거
"""

data_del_row = data.dropna(axis=0)

"""나) 결측값이 있는 열(세로) 제거"""

data_del_col = data.dropna(axis=1)

"""다) 결측값 있는 특정 행/열 제거"""

data[['salary']].dropna()

"""3) 결측값 대체: fillna()

가) 결측값을 특정 값으로 대체
"""

data_0 = data.fillna(0)   #0으로 대체
data_ffill = data.fillna(method='ffill')   #앞의 값으로 대체
data_bfill = data.fillna(method='bfill')   #뒤의 값으로 대체

"""나) 결측값을 변수별 평균으로 대체"""

data_mean = data.fillna(data.mean())   #평균으로 대체
data_mean = data.fillna(data.median())   #중간값으로 대체

"""다) 결측값을 다른 변수의 값으로 대체"""

data2 = data.copy()
data2['sales_new'] = np.where(pd.notnull(data2['sales'])==True, data2['sales'], data2['salary'])

#where함수 이용해, sales가 결측 아니면 원래값, 결측이면 salary의 값으로.

#data.groupby('salary').mean()

fill_mean_func = lambda g : g.fillna(g.mean())
data_group_mean = data.groupby('salary').apply(fill_mean_func)
data_group_mean

fill_values = {1:1000, 2:2000}
fill_func = lambda d : d.fillna(fill_values[d.name])
data_group_value = data.groupby('sex').apply(fill_func)
data_group_value

"""#6. 실전 과제"""

import pandas as pd
data = pd.read_csv('house_raw.csv')
data.head()

data.hist(bins=50, figsize=(10,5))

X = data[data.columns[0:5]]
y = data[["house_value"]]

#학습용,테스트용 데이터 구분을 위해 라이브러리 불러와서 7:3 비율 할당
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

#훈련,테스트데이터 독립변수 단위 동일하게 함
from sklearn.preprocessing import MinMaxScaler  
scaler_minmax = MinMaxScaler()
scaler_minmax.fit(X_train)
X_scaled_minmax_train = scaler_minmax.transform(X_train)
X_scaled_minmax_test = scaler_minmax.transform(X_test)

#선형모델을 적용
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_scaled_minmax_train, y_train)

#정확도 확인: 55%
pred_train = model.predict(X_scaled_minmax_train)
model.score(X_scaled_minmax_train, y_train)

#정확도: 음수 = 이유: 이상치 제거
pred_test = model.predict(X_scaled_minmax_test)
model.score(X_scaled_minmax_test, y_test)

#bedroom: 0.6 이상 제거. 0.6보다 큰 데이터 확인하니 14개.
data_bedroom = data[data['bedrooms']<0.6]
data_bedroom2 = data[data['bedrooms']>=0.6]
data_bedroom['bedrooms'].hist(bins=50, figsize=(10,5))
print(data_bedroom2['bedrooms'].value_counts().sum())

#households: 10 이상 제거. 
data_households = data[data['households']<10]
data_households2 = data[data['households']>=10]
data_households['households'].hist(bins=50, figsize=(10,5))
print(data_households2['households'].value_counts().sum())

#rooms: 20 이상 제거. 
print(data['rooms'].value_counts().sum())
data_rooms = data[data['rooms']<20]
data_rooms2 = data[data['rooms']>=20]
data_rooms['rooms'].hist(bins=50, figsize=(10,5))
print(data_rooms2['rooms'].value_counts().sum())

new_data = data[(data['bedrooms']<0.5) & (data['households']<7) & (data['rooms']<12)]
new_data.hist(bins=50, figsize=(10,5))

#특정데이터셋, 레이블데이터셋 나누기
X = new_data[new_data.columns[0:5]]
y = new_data[["house_value"]]

#라이브러리 불러오기
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=42)

#데이터 정규화
from sklearn.preprocessing import MinMaxScaler  
scaler_minmax = MinMaxScaler()
scaler_minmax.fit(X_train)
X_scaled_minmax_train = scaler_minmax.transform(X_train)
X_scaled_minmax_test = scaler_minmax.transform(X_test)

#선형모델을 적용
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_scaled_minmax_train, y_train)

#훈련데이터 정확도 확인: 55%
pred_train = model.predict(X_scaled_minmax_train)
print("훈련 데이터 정확도", model.score(X_scaled_minmax_train, y_train))

#훈련데이터 정확도 확인: 55%
pred_test = model.predict(X_scaled_minmax_test)
print("테스트데이터 정확도", model.score(X_scaled_minmax_test, y_test))

new_data.to_csv('housing_price.csv', index=False)

#최종

import numpy as np
import pandas as pd

data = pd.read_csv('house_raw.csv')

new_data = data[(data['bedrooms']<0.4) & (data['households']<6) & (data['rooms']<10)]
new_data.hist(bins=10, figsize=(15,10))
#data_rooms = data[data['rooms']<20]
#data_rooms['rooms'].hist(bins=50, figsize=(10,5))
#print(data['rooms'].value_counts().sum())
#print(data_rooms2['rooms'].value_counts().sum())

X = new_data[new_data.columns[0:5]]
y = new_data[["house_value"]]

#라이브러리 불러오기
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=42)

#데이터 정규화
from sklearn.preprocessing import MinMaxScaler  
scaler_minmax = MinMaxScaler()
scaler_minmax.fit(X_train)
X_scaled_minmax_train = scaler_minmax.transform(X_train)
X_scaled_minmax_test = scaler_minmax.transform(X_test)

#선형모델을 적용
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_scaled_minmax_train, y_train)

#훈련데이터 정확도 확인: 55%
pred_train = model.predict(X_scaled_minmax_train)
print("훈련 데이터 정확도", model.score(X_scaled_minmax_train, y_train))

#훈련데이터 정확도 확인: 55%
pred_test = model.predict(X_scaled_minmax_test)
print("테스트데이터 정확도", model.score(X_scaled_minmax_test, y_test))

new_data.to_csv('housing_price.csv', index=False)