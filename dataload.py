'''
api를 이용하여 데이터 수집
필수 import 설치 요구
    from bs4 import BeautifulSoup   # pip install bs4
    import urllib.request           # pip install urllib.request
    import pandas as pd             # pip install pandas
    import requests                 # pip install requests

*api_key setting
    dataload.My_naver_api_ID = 'API_key_ID 값 입력(str)'           >> default="희주 API ID Key"
    dataload.My_naver_api_Secret = 'API_key_secret 값 입력(str)'   >> default="희주 API Secret Key"

*function
    dataload.api_naver_TL(*location)  >> 검색 위치와 검색 키워드로 타이틀과 링크를 csv 파일로 저장 및 data 호출
'''
try:
    from bs4 import BeautifulSoup
    import urllib.request
    import pandas as pd
    import requests

    # 입력값
    My_naver_api_ID='NtViEQEhhin_KXWOLExO'
    My_naver_api_Secret='bNHhcXBeWr'
except:
    print("필수 import 설치 요구 (dataload? 참고)")
    key='error'
        
# naver api key를 이용해서 검색을 통한 키워드 추출
def api_naver_TL(location):
    '''
    api_naver_TL(*location)
    > naver api key를 이용한 후 검색사이트 지정 및 검색키워드에 따른 Title과 Link data 수집 및 저장
    > 1000 data searching
    
    argument:
        *location='blog', 'cafe' 등 검색 위치 입력(str)
        
    return:
    (총 2개)
        Dataframe       >> dataframe 형태로 data 추출 
        검색키워드(검색위치).csv 파일로 directory 자동 저장
    '''
    keyword=input("검색어를 입력해 주세요: ")
    
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
      

    
