import os
import time
import shutil
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
        .mode("append") \
        .save()
    
    print("Sinking data to postgresql is finished.")

    time.sleep(10)

    # remove 
    remove_data()

def remove_data() -> None:
    dir_path = "/mnt"

    # Get a list of all files in the directory
    file_list = os.listdir(dir_path)

    # Iterate over the file list and remove each file
    for file_name in file_list:
        file_header = file_name.split("-")[0]
        if file_header in ["liblz4", "spark", "hsperfdata_root"]:
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    print("Removing previous data is finished.")

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

    
