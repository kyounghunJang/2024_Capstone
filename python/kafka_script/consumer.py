from confluent_kafka import Consumer, KafkaError

# Kafka Consumer 설정
conf = {
    'bootstrap.servers': '172.22.0.8:9092',  # Kafka 서버 주소\ 
    # Consumer Group ID
    'auto.offset.reset': 'earliest',  # 가장 처음부터 메시지를 받기 시작
}
# Kafka Consumer 생성
consumer = Consumer(conf)

# 토픽 설정
consumer.subscribe(['test'])  # 여기에 사용할 토픽 이름을 입력하세요.

# 메시지를 계속 받기
while True:
    message = consumer.poll(1.0)

    if message is None:
        continue
    if message.error():
        if message.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(message.error())
            break

    print('Received message: {}'.format(message.value()))

consumer.close()