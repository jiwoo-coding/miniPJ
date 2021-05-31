'''
api를 이용하여 데이터 수집
필수 import 설치 값
    from bs4 import BeautifulSoup
    import urllib.request
    import pandas as pd
    import requests

dataload.My_naver_api_ID = 'API_key_ID 값 입력(str)'
dataload.My_naver_api_Secret = 'API_key_secret 값 입력(str)'
dataload.keyword = '검색 키워드 문자열 입력(str)'
api_naver_TL(location)   # naver api key를 이용해서 검색 위치에 따른 키워드 값을 타이틀과 링크로 csv 파일로 저장, return 값은 DataFrame
'''

# 입력값
My_naver_api_ID='NtViEQEhhin_KXWOLExO'
My_naver_api_Secret='bNHhcXBeWr'
keyword='깨무는 강아지'

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import requests

# naver api key를 이용해서 검색을 통한 키워드 추출
def api_naver_TL(location):
    '''
    parameter(1) : 'blog', 'cafe' 등 검색 위치 값(str)
    return DataFrame (반환)
    '''
    headers =  {   # Api key 입력
      'X-Naver-Client-Id': My_naver_api_ID,
      'X-Naver-Client-Secret': My_naver_api_Secret
    }
    dic_payload = {'query': keyword, 'display': '100',}
    data=pd.DataFrame(columns=['Title','Link'])
    for j in range(1,1000,100):
        dic_payload['start'] = j
        url = 'https://openapi.naver.com/v1/search/'+str(location)+'.json'
        res = requests.get(url, headers=headers, params=dic_payload)
        dic={}
        for i in range(100):
            try:
                temp=BeautifulSoup(res.json()['items'][i]['title'], 'html.parser')
                temp=temp.get_text()  # HTML 파싱 한것 중 text만 가져옴
                dic[temp]=res.json()['items'][i]['link']
            except:
                print(res.json())
        temp_df=pd.DataFrame(dic.items(), columns=['Title','Link'])
        data=pd.concat([data,temp_df], axis=0)  # dataframe 복사
    data.reset_index(drop=True, inplace=True) # 인덱스 정렬

    # 지정한 파일병으로 데이터 저장
    name=keyword+'('+location+')'
    data.to_csv(name+'.csv', encoding='utf-8-sig', index=False)
    return data
      
      
