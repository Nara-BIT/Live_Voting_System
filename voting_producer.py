import json
import random
import time
from confluent_kafka import Producer

producer = Producer({'bootstrap.servers': 'localhost:9092'})

def delivery_report(err, msg):
    if err is not None: print(f"❌ Error: {err}")
    else: print(f"🗳️ Vote Cast: {msg.value().decode('utf-8')}")

print("🗳️ Starting Election Voting...")

while True:
    vote_data = {
        "voter_id": f"voter_{random.randint(1000, 9999)}",
        "candidate_id": random.choice(['1', '2', '3']), # Voting for one of our 3 candidates
        "voting_time": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    producer.produce('votes_topic', value=json.dumps(vote_data), callback=delivery_report)
    producer.poll(0)
    time.sleep(0.5) # 2 votes per second