import requests as rq
import pandas as pd
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
# import MySQLdb


def naver_crw(code_list):

    # requests header
    headers = {'User-agent':
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    df = pd.DataFrame()

    # 100 페이지를 크롤링 할 때, 페이지가 100페이지보다 부족하면 그 상태로 return
    try:
        # 크롤링할 페이지 지정 -> range(시작페이지, 끝페이지+1)
        for i in range(1, 3):

            # 크롤링할 url.
            # {}부분에 종목코드 대입, i = 페이지number
            url = 'https://finance.naver.com/item/sise_day.nhn?code={0}&page='.format(
                code_list) + str(i)
            # pd.read_html 로 html 의 table 을 읽고 df 로 변환
            table = pd.read_html(
                rq.get(url, headers=headers).text, encoding="cp949")
            # 웹페이지 상의 구분선을 포함한 테이블을 가져온다.
            df_temp = table[0]
            df = df.append(df_temp)
        # 구분선 제거
        stock = df.dropna()
        return stock
    except:
        return stock


# KRX 한국 거래소 데이터에서 종목코드 가져오기
listed_comp_df = pd.read_html(
    'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

df = pd.DataFrame(listed_comp_df, columns=['종목코드'])

# df 에서 종목코드를 target 으로 지정
target = df['종목코드']

# 종목코드를 담아 둘 빈 리스트 생성
chart_list = []
# 종목코드의 6자리 숫자를 맞추기 위해 format 함수를 활용
for i in target:
    a = format(i, '06') # 06 = 230의 숫자가 나오면 앞에 000을 채워
    chart_list.append(a)

df = pd.DataFrame()

#engine connect(mysq)
#username : mysql 계정
#passwd : 비밀번호
#localhost : 로컬호스트 주소(워크밴치 메인페이지에서 확인 가능)
#port : 포트번호(워크밴치 메인페이지에서 확인 가능)
#skima_name : 스키마 이름
#new_table_name : 생성할 테이블 이름


engine = create_engine("mysql+mysqldb://{username}:{passwd}@{localhost}:{port}/{skima_name}", encoding='utf-8')
conn = engine.connect()
# print(len(chart_list)) #종목코드 개수 확인

#종목코드 별 크롤링
for i in chart_list[0:3]:
    df = naver_crw(i)
    # 크롤링된 df 형 데이터를 db에 append
    df.to_sql(name='{new_table_name}', con=engine, if_exists='append', index=False)

conn.close()