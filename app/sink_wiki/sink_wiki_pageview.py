import time
from pyspark.sql import SparkSession


def main(spark: SparkSession):
    # Load the parquet data
    df = spark.read.parquet("/tmp/wiki_pageview_wrangled.parquet")

    # Sink data to postgres
    df.write.format("jdbc") \
        .option("url", "jdbc:postgresql://172.23.0.12:5432/wiki") \
        .option("driver", "org.postgresql.Driver") \
        .option("dbtable", "pageview_counts") \
        .option("user", "postgres") \
        .option("password", "postgres") \
        .save()
    
    print("Sinking data to postgresql is finished.")
    time.sleep(10)

if __name__ == '__main__':
    # Create a SparSession
    spark = (SparkSession
             .builder
             .config("spark.jars", "/app/postgresql-42.6.0.jar")
             .master("local")
             .appName("wiki-pageview_sink")
             .getOrCreate())
    
    # Set the log level
    spark.sparkContext.setLogLevel('error')

    # Run the main method
    main(spark=spark)

    # Stop spark context
    spark.stop()

    
