from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

# 1. Initialize Spark with Kafka and Postgres Connectors
spark = (SparkSession.builder
         .appName("RealTimeVotingProcessor")
         .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.6.0")
         .config("spark.master", "spark://spark-master:7077")
         .getOrCreate())

spark.sparkContext.setLogLevel("ERROR")

# 2. Define the Schema of our Vote
vote_schema = StructType([
    StructField("voter_id", StringType(), True),
    StructField("candidate_id", StringType(), True),
    StructField("voting_time", StringType(), True)
])

# 3. Read the stream from Kafka
raw_stream = (spark.readStream
              .format("kafka")
              .option("kafka.bootstrap.servers", "kafka:29092")
              .option("subscribe", "votes_topic")
              .option("startingOffsets", "earliest")
              .load())

# 4. Convert JSON bytes to Columns
votes_df = raw_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), vote_schema).alias("data")) \
    .select("data.*")

# 5. Aggregate Votes (The Real-Time Count)
vote_counts = votes_df.groupBy("candidate_id").count()

# 6. Function to write the results to Postgres
def write_to_postgres(df, epoch_id):
    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://db:5432/voting_db") \
        .option("driver", "org.postgresql.Driver") \
        .option("dbtable", "vote_results") \
        .option("user", "user") \
        .option("password", "password") \
        .mode("overwrite") \
        .save()
    print(f"📊 Batch {epoch_id} processed and saved to Postgres.")

# 7. Start the Streaming Query
query = (vote_counts.writeStream
         .foreachBatch(write_to_postgres)
         .outputMode("complete")
         .start())

print("🚀 Spark Processor is running and counting votes...")
query.awaitTermination()