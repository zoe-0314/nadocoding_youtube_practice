# Project) 웹 스크래핑을 이용하여 나만의 비서를 만드시오

#[조건]
# 1. 네이버에서 오늘 서울의 날씨정보를 가져온다
# 2. 헤드라인 뉴스 3건을 가져온다
# 3. IT 뉴스 3건을 가져온다
# 4. 해커스 어학원 홈페이지에서 오늘의 영어 회화 지문을 가져온다.

# [출력 예시]

# [오늘의 날씨]
# 흐림, 어제보다 00º 높아요
# 현재 00℃ (최저 00º / 최고 00º)
# 오전 강수확률 00% / 오후 강수확률 00%

# 미세먼지 00㎍/㎡좋음
# 초미세먼지 00㎍/㎡좋음

# [헤드라인 뉴스]
# 1. 무슨 무슨 일이...
# (링크 : http://...)
# 2. 무슨 무슨 일이...
# (링크 : http://...)
# 3. 무슨 무슨 일이...
# (링크 : http://...)

# [IT 뉴스]
# 1. 무슨 무슨 일이...
# (링크 : http://...)
# 2. 무슨 무슨 일이...
# (링크 : http://...)
# 3. 무슨 무슨 일이...
# (링크 : http://...)

# [오늘의 영어 회화]
# (영어 지문)
# Jason : How do you think bla bla..
# Kim : Well, I think...

# (한글 지문)
# Jason :  어쩌구 저쩌구 어떻게 생각하세요?
# Kim : 글쎄요, 저는 어쩌구 저쩌구...


import requests
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


#---------- 오늘의 날씨 ----------
def today_weather():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    browser = webdriver.Chrome(options=option)
    browser.maximize_window()
    url = "https://www.naver.com/"
    browser.get(url)

    # '서울 날씨' 검색
    browser.find_element(By.ID,"query").send_keys("서울 날씨")
    browser.find_element(By.ID,"search_btn").click()

    soup = BeautifulSoup(browser.page_source,"lxml")
    weather = soup.find("span",attrs={"class":"weather before_slash"}).get_text()



    current_weather_info = soup.find_all("div",attrs={"class":"_today"})
    for temp in current_weather_info:
        current_temperature = temp.find("div","temperature_text")
        current_temperature.find("span",attrs={"class":"blind"}).decompose()
        current_temperature = current_temperature.text

        temperature_diff = temp.find("p",attrs={"class":"summary"})
        temperature_diff.find("span",attrs={"class":"weather before_slash"}).decompose()
        temperature_diff = temperature_diff.text

    weekly_weather_info = soup.find("div","list_box _weekly_weather")
    today_lowest_highest_temperature = weekly_weather_info.find("li","week_item today").find("div","cell_temperature").get_text()
    today_rainfall_rate_am = weekly_weather_info.find("li","week_item today").find_all("span","weather_inner")[0].find("span","weather_left").find("span","rainfall").get_text()
    today_rainfall_rate_pm = weekly_weather_info.find("li","week_item today").find_all("span","weather_inner")[1].find("span","weather_left").find("span","rainfall").get_text()

    current_weather_report = soup.find("h3",string="오늘의 날씨").find_parent()
    #print(type(current_weather_report))
    today_particulate_matter = current_weather_report.find("ul","today_chart_list").find_all("li")[0].get_text()
    today_fine_particulate_matter = current_weather_report.find("ul","today_chart_list").find_all("li")[1].get_text()
    #print(type(today_particulate_matter), type(today_fine_particulate_matter))

    print("[오늘의 날씨]")
    print(weather, temperature_diff)
    print("현재",current_temperature,"(",today_lowest_highest_temperature.strip(),")")
    print("오전 강수확률 ",today_rainfall_rate_am.strip(), " / 오후 강수확률 ",today_rainfall_rate_pm.strip())
    print(today_particulate_matter.strip())
    print(today_fine_particulate_matter.strip())


#---------- 헤드라인 뉴스 ----------
#경제 페이지의 헤드라인 뉴스 스크래핑
#https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101

def news():
    url_news = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101"

    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    browser = webdriver.Chrome(options=option)
    browser.maximize_window()
    browser.get(url_news)

    soup = BeautifulSoup(browser.page_source,"lxml")
    news = soup.find("div","_persist").find("div","cluster").find_all("div","cluster_group _cluster_content",limit=3)
    number = 0
    print("[헤드라인 뉴스]")
    for temp in news:
        number +=1
        headline_title = temp.find("h2","cluster_head_topic").get_text().strip()
        headline_url = "https://news.naver.com"+temp.find("h2","cluster_head_topic").find("a")["href"]
        print(number,". ",headline_title)
        print("( 링크 : ",headline_url,")")
    

#---------- IT 뉴스 ----------
#IT/과학 뉴스 페이지의 헤드라인 뉴스 스크래핑
#https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105

def it_news():
    url_itnews = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    browser.get(url_itnews)

    soup = BeautifulSoup(browser.page_source,"lxml")
    it_news = soup.find("div",id="main_content").find("div","list_body section_index").find("div","_persist").find_all("div","cluster_group _cluster_content",limit=3)
    it_number = 0
    print("[IT/과학 뉴스]")
    for it_temp in it_news:
        it_number +=1
        it_headline_title = it_temp.find("h2","cluster_head_topic").get_text().strip()
        it_headline_url = "https://news.naver.com" + it_temp.find("h2","cluster_head_topic").find("a")["href"]
        print(it_number,". ",it_headline_title)
        print("( 링크 : ",it_headline_url,")")



#---------- 오늘의 영어 회화 ----------
# https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english

def today_english():
    today_english_url="https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english"
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    browser = webdriver.Chrome(options=option)
    browser.maximize_window()
    browser.get(today_english_url)
    time.sleep(2)

    try:
        if browser.find_element_by_class_name("closing_banner"):
            browser.find_element(By.XPATH,"//*[@class='closing_banner']//a[@class='close']").click()
    except:
        pass

    soup = BeautifulSoup(browser.page_source,"lxml")
    korean_text = soup.find_all("div","conv_in")[0].find_all("div",attrs={"id":re.compile("^conv_kor_t")})
    english_text = soup.find_all("div","conv_in")[1].find_all("div",attrs={"id":re.compile("^conv_kor_t")})

    print("[오늘의 영어 회화]\n")
    print("(영어 지문)")
    for text in korean_text:
        print(text.get_text().strip())
    print("\n(한글 지문)")
    for text in english_text:
        print(text.get_text().strip())


today_weather()
news()
it_news()
today_english()