## Ingesting Data
### Components of a data platform
- data lake
  - landing zone -> clean zone -> business zon

### Introduction to data ingestion with Singer
- Singer
  - open-source standard for writing scripts that move data
  - JSON format으로 data exchange
  - *target*으로 data lake에 data load, *tap*으로 data extract
    - communicate over *stream* : schema(metadata), state(process metadata), record(data)

```python
# Import json
import json

database_address = {
  "host": "10.0.0.5",
  "port": 8456
}

# Open the configuration file in writable mode
with open("database_config.json", "w") as fh:
  # Serialize the object in this file handle
  json.dump(obj=database_address, fp=fh)

# Complete the JSON schema
# 이렇게 적절한 schema를 정하는 것은 상당히 효율적
schema = {'properties': {
    'brand': {'type': 'string'},
    'model': {'type': 'string'},
    'price': {'type': 'number'},
    'currency': {'type': 'string'},
    'quantity': {'type': 'number', 'minimum': 1},  
    'date': {'type': 'string', 'format': 'date'},
    'countrycode': {'type': 'string', 'pattern': "^[A-Z]{2}$"}, 
    'store_name': {'type': 'string'}}}

# Write the schema
singer.write_schema(stream_name='products', schema=schema, key_properties=[])
```

### Running an ingestion pipeline with Singer
- ??

## Creating a data transformation pipeline with PySpark
- 4 libraries built on top of Spark core:
  - Spark SQL, Spark Streaming, MLib, GraphX
### Introduction
```python
# Read a csv file and set the headers
df = (spark.read
      .options(header=True)
      .csv("/home/repl/workspace/mnt/data_lake/landing/ratings.csv"))
# Define the schema
schema = StructType([
  StructField("brand", StringType(), nullable=False),
  StructField("model", StringType(), nullable=False),
  StructField("absorption_rate", ByteType(), nullable=True),
  StructField("comfort", ByteType(), nullable=True)
])

better_df = (spark
             .read
             .options(header="true")
             # Pass the predefined schema to the Reader
             .schema(schema)
             .csv("/home/repl/workspace/mnt/data_lake/landing/ratings.csv"))
pprint(better_df.dtypes)
```
### Cleaning data
- Handle invalid rows : `mode='DROPMALFORMED'`
  - 문제가 있는 row는 아예 삭제

```python
spark.read.options(header='true', mode='DROPMALFORMED').csv('df.csv)
```

- Supplying default values for missing data

```python
df.fillna(특정값, subset=['해당컬럼'])
```

- Conditionally replace values
  
```python
from pyspark.sql.functions import col, when
from datetime import date, timedelta

one_year_from_now = date.today().replace(year=date.today().year + 1)
better_frame = employees.withColumn('end_date', when(col('end_date') > one_year_from_now, None).otherwise(col('end_date')))
# when() : if-else 같은 함수
```

### Transforming data with Spark
- filtering, selecting and rename, grouping and aggregation, joining, ordering 등등

```python
from pyspark.sql.functions import col

# Select the columns and rename the "absorption_rate" column
result = ratings.select([col("brand"),
                       col("model"),
                       col("absorption_rate").alias('absorbency')])

# Show only unique values
result.distinct().show()

from pyspark.sql.functions import col, avg, stddev_samp, max as sfmax

aggregated = (purchased
              # Group rows by 'Country'
              .groupBy(col('Country'))
              .agg(
                # Calculate the average salary per group and rename
                avg('Salary').alias('average_salary'),
                # Calculate the standard deviation per group
                stddev_samp('Salary'),
                # Retain the highest salary per group and rename
                sfmax('Salary').alias('highest_salary')
              )
             )

aggregated.show()
```
### Packaging you application
- 강의참고
- pyspark를 돌리려면 먼저 zip your code
  - `pipeline_folder`가 위치한 곳으로 이동한 뒤 `zip --recurse-paths zip_file.zip pipeline_folder` 
- pyspark application은 locally 돌리기 위해서는
  - `spark-submit --py-files PY_FILES MAIN_PYTHON_FILE`

## Testing your data pipeline
### Writing unit test for pyspark
- 아래와 같은 방법으로 construct DataFrame in-memory

```python
from pyspark.sql import Row
sample_r = Row('name', 'age')
record = (sample_r('minsoo', 27), sample_r('kim', 27))
df = spark.createDataFrame(record)
```

- 함수를 만들어서 test하기 쉽게 하자.
- 그리고 pytest로 test하면 된다.

### Coutinuous testing
- CI/CD

## Managing and orchestrating a workflow
- Airflow