import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import os
from ultralytics import YOLO

service = Service(executable_path=r"/Users/jang-gyeonghun/2024_Capstone/crawling_bs4/crawling.py" )
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 브라우저를 화면에 표시하지 않음
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

model = YOLO("/Users/jang-gyeonghun/2024_Capstone/crawling_bs4/naver_crawling/best.pt")


driver = webdriver.Chrome(service=service, options=options)
# 네이버 이미지 검색 URL
search_query = ["장미", "튤립", "백합", "히아신스", "카네이션", "수국", "벚꽃", "아마리릴리스", "나팔꽃", "프리지아", "데이지", "카라", "매화", "섬마을초", "샤스핀", "라벤더", "마리골드", "수선화", "블루벨"] # 크롤링할 이미지의 검색어를 입력하세요
class_num = 0
for name in search_query:
    url = f"https://search.naver.com/search.naver?where=image&query={name}"

    if not os.path.exists("data/"+name):
        os.makedirs("data/"+name)

    driver.get(url)
    time.sleep(2)  # 페이지가 완전히 로드될 때까지 대기
    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    page_source = driver.page_source

    # BeautifulSoup으로 파싱
    soup = BeautifulSoup(page_source, 'html.parser')

    image_urls = []
    for img_tag in soup.find_all('img',class_= "_fe_image_tab_content_thumbnail_image"):
        image_urls.append(img_tag.get('src'))
    i=0
    for url in image_urls:
        try:
            if 'data:image' in url:
                continue
            response = requests.get(url)
            with open(f'data/{name}/image_{i}.jpg', 'wb') as f:
                f.write(response.content)
        
            result=model.predict(f'data/{name}/image_{i}.jpg')
            if 'no detection' in str(result):
                raise ValueError('No detection found in result')
            with open(f'data/{name}/image_{i}.txt', 'w') as f:
                if result and len(result) > 0:
                    if hasattr(result[0][0], 'boxes') and hasattr(result[0][0].boxes, 'cls'):
                        if 1.0 in result[0][0].boxes.cls or 2.0 in result[0][0].boxes.cls:
                            f.write(f"{class_num} {result[0][0].boxes.xywh[0][0]} {result[0][0].boxes.xywh[0][1]} {result[0][0].boxes.xywh[0][2]} {result[0][0].boxes.xywh[0][3]}")
            i+=1
        except Exception as e:
            print(f"Error occurred: {e}")
            if os.path.exists(f'data/{name}/image_{i}.jpg'):
                os.remove(f'data/{name}/image_{i}.jpg')
            if os.path.exists(f'data/{name}/image_{i}.txt'):
                os.remove(f'data/{name}/image_{i}.txt')
            
    class_num+=1

driver.quit()
print("이미지 다운로드 완료")
