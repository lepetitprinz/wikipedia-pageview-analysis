import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace, to_date, to_timestamp


def main(spark: SparkSession):
    # Load the parquet data
    df = spark.read.parquet("/tmp/wiki_pageview.parquet")

    # Wrangling the dataframe
    df = df.withColumn(
        "page_title",
        regexp_replace(col("page_title"), "[^a-zA-Z0-9\\s]", ""))
    df = df.filter(col("page_title") != "")

    # Change data types
    df = df \
        .withColumn("view_counts", col("view_counts").cast("integer")) \
        .withColumn("execute_date", to_date(col("execute_date"), "yyyy-MM-dd")) \
        .withColumn("execute_time", to_timestamp(col("execute_time")))

    # Filter view counts
    df = df.filter(col("view_counts") >= 10)

    # Save the preprocessed dataframe
    df.write \
    .mode(saveMode="overwrite") \
    .parquet(
        "/tmp/wiki_pageview_wrangled.parquet",
        compression='gzip'
        )

if __name__ == '__main__':
    # Create a SparSession
    spark = (SparkSession
             .builder
             .appName("wiki-pageview_wrangling")
             .getOrCreate())
    spark.sparkContext.setLogLevel('error')
    main(spark=spark)
    spark.stop()

    time.sleep(10)