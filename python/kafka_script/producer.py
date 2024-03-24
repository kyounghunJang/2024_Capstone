from confluent_kafka import Producer
import os, io, time
import cv2
import base64

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")
        print(f"Delivery took: {time.time() - msg.timestamp()[1]} seconds")

# Kafka 설정
conf = {'bootstrap.servers': '172.22.0.8:9092'}
producer = Producer(conf)

# 이미지 파일 경로
img_path = '/opt/script/'  # 이미지 파일이 있는 폴더의 경로를 지정하세요.

for filename in os.listdir(img_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # 이미지 파일만 처리
        img = cv2.imread(img_path+'/'+filename)

        # 이미지를 JPEG 형식으로 인코딩
        result, encoded_img = cv2.imencode('.jpg', img)
        binary_img = encoded_img.tobytes()
        im_b64 = base64.b64encode(binary_img)
        print(im_b64)
        producer.produce('test',value=im_b64, callback=delivery_report)
producer.flush()