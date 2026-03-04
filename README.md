# 🗳️ Real-Time Election Voting Pipeline

A complete end-to-end data engineering pipeline that simulates live election voting, processes the votes in real-time, and displays the results on a live updating dashboard.

## 🏗️ Architecture & Tech Stack
This project uses a modern streaming architecture built entirely in Docker:
* **Python (Producer):** Generates continuous live JSON vote payloads.
* **Apache Kafka (KRaft Mode):** The ingestion engine, running completely without Zookeeper.
* **Apache Spark Streaming:** The processing brain. Catches the Kafka stream, aggregates the votes, and pushes them out.
* **PostgreSQL:** The analytical storage layer holding the aggregated results.
* **Streamlit:** A live, auto-refreshing UI that visualizes the final output in real-time.

## ⚙️ Prerequisites
* Docker & Docker Compose
* Python 3.9+

## 🚀 How to Run the Pipeline

**1. Spin up the Infrastructure**
Start Postgres, Kafka, and the Spark Cluster:
```bash
docker compose up -d
