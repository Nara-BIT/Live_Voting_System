# 🗳️ Real-Time Election Voting Pipeline

A complete end-to-end data engineering pipeline that simulates live election voting, processes the votes in real-time, and displays the results on a live updating dashboard.

## 🏗️ Architecture & Tech Stack
graph LR
    %% Custom Styling
    classDef python fill:#4B8BBE,stroke:#306998,stroke-width:2px,color:white;
    classDef kafka fill:#231F20,stroke:#FFF,stroke-width:2px,color:white;
    classDef spark fill:#E25A1C,stroke:#FFF,stroke-width:2px,color:white;
    classDef db fill:#336791,stroke:#FFF,stroke-width:2px,color:white;
    classDef ui fill:#FF4B4B,stroke:#FFF,stroke-width:2px,color:white;

    %% Components
    P[🐍 Python Producer<br/>voting_producer.py]:::python
    
    subgraph Docker Infrastructure
        direction LR
        K[Apache Kafka<br/>KRaft Broker]:::kafka
        S[⚡ Apache Spark<br/>Streaming Processor]:::spark
        DB[(🐘 PostgreSQL<br/>voting_db)]:::db
    end
    
    ST[📊 Streamlit Dashboard<br/>app.py]:::ui

    %% Data Flow
    P -- "Publishes Votes (JSON)" --> K
    K -- "Streams Topic (votes_topic)" --> S
    S -- "Writes Aggregations (JDBC)" --> DB
    DB -- "Queries Live Data (SQL)" --> ST
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

