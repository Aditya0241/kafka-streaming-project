import pandas as pd
from kafka import KafkaProducer
from time import sleep
from json import dumps

BROKER = "localhost:9092"
TOPIC = "demo_test"
CSV_PATH = "/home/ec2-user/data/indexProcessed.csv"

producer = KafkaProducer(
    bootstrap_servers=[BROKER],
    value_serializer=lambda x: dumps(x).encode("utf-8"),
)

df = pd.read_csv(CSV_PATH)

print(f"Loaded {len(df)} rows from {CSV_PATH}")
print(f"Sending to Kafka topic: {TOPIC} on {BROKER}")

while True:
    msg = df.sample(1).to_dict(orient="records")[0]
    producer.send(TOPIC, value=msg)
    producer.flush()
    print("sent one message")
    sleep(1)
