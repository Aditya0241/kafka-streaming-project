from kafka import KafkaConsumer
from json import loads
import json
from s3fs import S3FileSystem

BROKER = "localhost:9092"
TOPIC = "demo_test"

BUCKET = "aditya-kafka-streaming-2025-12-28"
PREFIX = "kafka/"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[BROKER],
    value_deserializer=lambda x: loads(x.decode("utf-8")),
    auto_offset_reset="latest",
    enable_auto_commit=True,
)

s3 = S3FileSystem()

count = 0
for msg in consumer:
    key = f"s3://{BUCKET}/{PREFIX}stock_market_{count}.json"
    with s3.open(key, "w") as f:
        json.dump(msg.value, f)
    print("wrote:", key)
    count += 1
