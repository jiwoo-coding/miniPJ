'''
Naver를 이용한 데이터 크롤링(API KEY 필요)

필수 import 설치 요구
    from bs4 import BeautifulSoup   # pip install bs4
    import urllib.request           # pip install urllib.request
    import pandas as pd             # pip install pandas
    import requests                 # pip install requests

# api_key setting
    dataload.My_naver_api_ID = 'API_key_ID 값 입력(string)'           >> default="희주 API ID Key"
    dataload.My_naver_api_Secret = 'API_key_secret 값 입력(string)'   >> default="희주 API Secret Key"

# function
    dataload.api_naver_TL(*location)    >> 검색 위치와 검색 키워드로 타이틀과 링크를 csv 파일로 저장 및 data 호출
    dataload.make_bodytext(*try_url, **location)  >> URL과 검색 위치에 따라서 TEXT(string) data로 반환
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
        *location='blog', 'cafe' 등 검색 위치 입력(string)
        
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

# 동적 elements의 HTML을 가져오기 위해 blog URL 재설정
def final_url_blog(try_url):
    try:
        url=try_url
        html_result=requests.get(url)
        soup_temp=BeautifulSoup(html_result.text, 'html.parser')
        area_temp=soup_temp.find(id='screenFrame')   # id가 screenFrame을 찾는다.
        url_2=area_temp.get('src')                   # 이에 따른 소스를 집어 넣음
        html_result=requests.get(url_2)               
        soup_temp=BeautifulSoup(html_result.text, 'html.parser')
        area_temp=soup_temp.find(id='mainFrame')     # id가 mainFrame을 찾는다.
        url_3=area_temp.get('src')
        print(url_3)
        url_4='https://blog.naver.com'+url_3         # 
        return url_4
    except:
        try:
            area_temp = soup_temp.find(id='mainFrame')
            url_3=area_temp.get('src')
            url_4='https://blog.naver.com'+url_3
            return url_4
        except:
            print(f'{try_url} renew error')
            return None

# 새롭게 만든 URL을 이용해서 TEXT data 추출
def make_bodytext(try_url, location):
    '''
    make_bodytext(*try_url, **location)
    > url을 가져와서 검색위치에 따라 본문의 TEXT data 반환 
    > 검색위치에 따라서 동적, 정적 elements가 나뉨
    
    argument:
        *try_url= Link값 (string)
        **location='blog', 'cafe' 등 검색 위치 입력(string)
        
    return:
        text data(string)       >> 문자열 형태로 본문 text 추출 
    '''
    if location=='blog':  #'blog' 에서만 적용
        try:
            url=final_url_blog(try_url)   # URL 재생성
            res=urllib.request.urlopen(url)
            soup=BeautifulSoup(res, 'html.parser')
            title = soup.findAll("div",{"class":'se-main-container'})     #블로그마다 동일하게 HTML 중 div에서 se-main-container의 본문을 가져옴
            for a in title:
                text=a.get_text()    # 가져온 본문 중 text만 가져옴
            text_data=text.replace("\n","").replace("\u200b","")                # \n 과 \u200b 문자는 HTML 이므로 제거
            return text_data
        except:
            print(f"{try_url}({location}) error")
    else:
        print("location is not allowed")
        return 0
