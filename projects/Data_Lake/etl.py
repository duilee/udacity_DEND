import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col ,monotonically_increasing_id, from_unixtime
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from pyspark.sql.types import StructType, StructField, DoubleType, StringType, IntegerType, TimestampType

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    """
    create a new spark session
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    process song data in JSON file and output parquet format files
    """
    # get filepath to song data file
    song_data = os.path.join(input_data, 'song_data/*/*/*/*.json')
    
    song_schema = StructType([
        StructField("artist_id", StringType()),
        StructField("artist_latitude", DoubleType()),
        StructField("artist_location", StringType()),
        StructField("artist_longitude", StringType()),
        StructField("artist_name", StringType()),
        StructField("duration", DoubleType()),
        StructField("num_songs", IntegerType()),
        StructField("title", StringType()),
        StructField("year", IntegerType()),
    ])
    
    # read song data file
    df = spark.read.json(song_data, schema=song_schema)

    # extract columns to create songs table
    song_cols = ["title", "artist_id", "year", "duration"]
    songs_table = df.select(song_cols).dropDuplicates().withColumn("song_id", monotonically_increasing_id())
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.mode("overwrite").partitionBy("year", "artist_id").parquet(output_data + "songs")

    # extract columns to create artists table
    artists_cols = ["artist_id", "artist_name as name", "artist_location as location", "artist_latitude as latitude", "artist_longitude as longitude"]
    artists_table = df.selectExpr(artists_cols).dropDuplicates()
    
    # write artists table to parquet files
    artists_table.write.mode("overwrite").parquet(output_data + 'artists')


def process_log_data(spark, input_data, output_data):
    """
    process log data in json format and output parquet files
    """

    # get filepath to log data file
    log_data = os.path.join(input_data, 'log_data/*/*/*/*.json') 

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong')

    # extract columns for users table    
    users_cols = ["userId as user_id", "firstName as first_name", "lastName as last_name", "gender", "level"]
    users_table = df.selectExpr(users_cols).dropDuplicates()
    
    # write users table to parquet files
    users_table.write.mode("overwrite").parquet(output_data + 'users')

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: x / 1000, TimestampType())
    df = df.withColumn("timestamp", get_timestamp(df.ts))
    
    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: datetime.fromtimestamp(x), TimestampType())
    df = df.withColumn("start_time", get_datetime(df.timestamp))
    
    # extract time details
    df = df.withColumn("hour", hour("start_time")) \
        .withColumn("day", hour("start_time")) \
        .withColumn("week", hour("start_time")) \
        .withColumn("month", hour("start_time")) \
        .withColumn("year", hour("start_time")) \
        .withColumn("weekday", hour("start_time")) \
    
    # extract columns to create time table
    time_table = df.select("start_time", "hour", "day", "week", "month", "year", "weekday")
    
    # write time table to parquet files partitioned by year and month
    time_table.write.mode("overwrite").partitionBy("year", "month").parquet(output_data + "time")

    # read in song data to use for songplays table
    song_df = spark.read.parquet(os.path.join(output_data, "songs/*/*/*/*"))
    songs_logs = df.join(songs_df, (df.song == songs_df.title))
    
    artists_df = spark.read.parquet(os.path.join(output_dataa, "artists"))
    artists_logs = songs_logs.join(artists_df, (songs_logs.artist == artists_df.name))
    songplays = artists_logs.join(time_table, artists_logs.ts == time_table.ts, 'left').drop(artists_logs.year)

    # extract columns from joined song and log datasets to create songplays table 
    songplays_cols = ["start_time", "userId as user_id", "level", "song_id", "artist_id", "sessionId as session_id", "location", "userAgent as user_agent", "year", "month"]
    songplays_table = songplays.select(songplays_cols).repartition("year", "month")

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.mode("overwrite").partitionBy("year", "month").parquet(output_data, 'songplays')


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://datalakedemo2/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
