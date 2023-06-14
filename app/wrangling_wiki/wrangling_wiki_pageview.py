from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace


def main(spark: SparkSession):
    # Load the parquet data
    df = spark.read.parquet("/tmp/wiki_pageview.parquet")

    # Wrangling the dataframe
    df = df.withColumn(
        "page_title",
        regexp_replace(col("page_title"), "[^a-zA-Z0-9\\s]", ""))
    df = df.filter(col("page_title") != "")

    # Save the preprocessed dataframe
    df.write.parquet(
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
