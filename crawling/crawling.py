import time
import requests
from selenium import webdriver
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pyflink.common import WatermarkStrategy
from pyflink.common.serialization import SimpleStringSchema,DeserializationSchema   
from pyflink.datastream.connectors.kafka import KafkaSource
from pyflink.datastream.stream_execution_environment import StreamExecutionEnvironment

from torchvision import transforms
from PIL import Image
from io import BytesIO
import cv2
import base64


def preprocessing(image_bytes):
    # PyTorch의 DataLoader를 사용하여 전처리를 수행합니다.
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    if(image_bytes is None):
        return None
    im_bytes = base64.b64decode(image_bytes) 
    im_file = BytesIO(im_bytes) 
    img = Image.open(im_file)
    return transform(img)


class Crawler:

    def __init__(self):
        download_dir = r"/usr/crawling/data" 
        prefs = {"download.default_directory": download_dir}
        service = Service(executable_path='/usr/bin/chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # 브라우저를 화면에 표시하지 않음
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        self.driver = webdriver.Chrome(service=service,options=options)
        self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        self.driver.execute("send_command", params)

    def crawling_url(self, url):
        self.driver.get(url)
        self.driver.find_element(By.ID, 'video_download').click()
        time.sleep(1)
        self.driver.find_element(By.ID, 'image_download').click()
        time.sleep(1)

class FlinkProcessing:

    def __init__(self):
        self.env=StreamExecutionEnvironment.get_execution_environment()
        self.env.add_jars("file:///usr/crawling/Driver/flink-sql-connector-kafka-3.0.2-1.18.jar")


    def flink_processing(self):
        source= KafkaSource.builder()\
        .set_bootstrap_servers('172.22.0.8:9092')\
        .set_topics('test')\
        .set_value_only_deserializer(SimpleStringSchema())\
        .build()

        self.env.from_source(source, WatermarkStrategy.no_watermarks(), "Kafka Source")\
            .map(preprocessing)\
            .print()
        self.env.execute()


if __name__ == "__main__":
    crawler = Crawler()  # Crawler 클래스의 인스턴스 생성
    test= FlinkProcessing()
    test.flink_processing()

