# hdstreetview   
   
## 패키지 설치   
```
pip install git+https://github.com/arawatki97/hdstreetview
```
   
## 패키지 업데이트   
```
pip install --upgrade git+https://github.com/arawatki97/hdstreetview
```
   
## 패키지 설명서   
0.1버전 기준   
   
구조   
hdstreetview   
  ├─ csv2naver   
  └─ svnaver   
   
사용방법   
1. hdstreetview 패키지에서 csv2naver 모듈을 불러온다.   
```python
from hdstreetview import csv2naver
```
   
2. csv2naver 모듈 내의 csv2naver 함수를 사용한다.   
```python
# VARIABLES
csv2naver.csv2naver(csv, path, column, year=None)

# csv    : 경위도 좌표가 있는 CSV 파일의 경로.
# path   : 파노라마 사진을 저장하고 싶은 경로. 끝 부분에 /(슬래시)를 반드시 포함해야 한다.
# column : 경위도 좌표에 해당하는 두 개의 컬럼. [위도, 경도] 순서의 리스트로 구성해야 한다.
# year   : 비교할 연도 쌍. [연도, 연도] 형태의 리스트로 구성해야 한다.
           연도 비교를 하고 싶지 않다면 입력하지 않아야 한다!!


# EXAMPLE 1
# 함수에 그대로 집어넣는 방법
csv2naver.csv2naver("../data/roadxy.csv", "../result/", ["ycoord","xcoord"], year=[2010, 2020])

# EXAMPLE 2
# 함수에 변수를 집어넣는 방법
# 연도 비교를 하지 않을 때
csv = "../data/roadxy.csv"
path = "../result/"
column = ["ycoord","xcoord"]
csv2naver.csv2naver(csv, path, column)
```
   

