## Getting to know PySpark
- RDD, DataFrame
- To start working with Spark DataFrames, you first have to create a `SparkSession` object from your `SparkContext`. You can think of the `SparkContext` as your connection to the cluster and the `SparkSession` as your interface with that connection.
- Creating a SparkSession
  - 이미 SparkSession이 있으면 새로 만드는 것보다 이를 불러오는게 좋다.
  - 이때, `SparkSession.builder.getOrCreate()` 사용
- Viewing tables
  - SparkSession에는 `catalog`라는 attribute가 존재한다.
  - 이는 해당 cluster안에 있는 data들의 list이다.
  - `session이름.catalog.listTables()`하면 이들을 볼 수 있다.
- DataFrame의 장점 : Spark cluster에 있는 table에 SQL 쿼리사용이 가능하다.
```python
query = "SELECT origin, dest, COUNT(*) as N FROM flights GROUP BY origin, dest"

flight_counts = my_session.sql(query)
```
- 위에서 `pd_counts = flight_counts.toPandas()`를 통해 `pandas`로 만들 수 있다.
- 반대도 가능하다.
  - `.createDataFrame()` method takes a pandas DataFrame and returns a Spark DataFrame.
  - 하지만 이 결과는 `SparkSession` catalog가 아니라 locally 저장된다.
  - `.createTempView` spark DataFrame method를 통해 catalog에 등록할 수 있다. 하지만 이는 임시저장이라 해당 spark DataFrame을 만든 SparkSession으로만 접근 할 수 있다.

```python
# Create pd_temp
pd_temp = pd.DataFrame(np.random.random(10))

# Create spark_temp from pd_temp
spark_temp = my_spark.createDataFrame(pd_temp)

# Examine the tables in the catalog
print(my_spark.catalog.listTables())

# Add spark_temp to the catalog
spark_temp.createOrReplaceTempView("temp")

# Examine the tables in the catalog again
print(my_spark.catalog.listTables())
```
- 위에서는 `pandas`를 통해 data를 Spark에 넣었는데 바로 file을 Spark로 읽을 수도 있다. : `airports = my_spark.read.csv(file_path, header=True)`

## Manipulating data
### Crearting columns
- Updating a Spark DataFrame is somewhat different than working in pandas because the Spark DataFrame is immutable.
- 그래서 항상 새로운 df를 return한다.

```python
# Create the DataFrame flights
flights = spark.table("flights")

# Show the head
flights.show()

# Add duration_hrs
flights = flights.withColumn("duration_hrs", flights.air_time/60)
```
### Filtering Data
- SQL의 `WHERE`에 해당하는 방법
- 아래처럼 2가지 방법으로 가능하다.
```python
# Filter flights by passing a string
long_flights1 = flights.filter("distance > 1000")

# Filter flights by passing a column of boolean values
long_flights2 = flights.filter(flights.distance   > 1000)
```
### Selecting
- SQL의 `SELECT`에 해당하는 방법

```python
# Select the first set of columns
selected1 = flights.select("tailnum", "origin", "dest")

# Select the second set of columns
temp = flights.select(flights.origin, flights.dest, flights.carrier)

# Define first filter
filterA = flights.origin == "SEA"

# Define second filter
filterB = flights.dest == "PDX"

# Filter the data, first by filterA then by filterB
selected2 = temp.filter(filterA).filter(filterB)
```

```python
# Define avg_speed
avg_speed = (flights.distance/(flights.air_time/60)).alias("avg_speed")

# Select the correct columns
speed1 = flights.select("origin", "dest", "tailnum", avg_speed)

# Create the same table using a SQL expression
speed2 = flights.selectExpr("origin", "dest", "tailnum", "distance/(air_time/60) as avg_speed")
```

### Group, Aggregating
- `df.groupBy().min("col").show()`

```python
by_plane = flights.groupBy("tailnum")
by_plane.count().show()

by_origin = flights.groupBy("origin")
by_origin.avg("air_time").show()

# Import pyspark.sql.functions as F
import  pyspark.sql.functions as F

by_month_dest = flights.groupBy('month','dest')
by_month_dest.avg('dep_delay').show()
by_month_dest.agg(F.stddev('dep_delay')).show()
```
- `.agg()` method. This method lets you pass an aggregate column expression that uses any of the aggregate functions from the `pyspark.sql.functions` submodule.

### Join
```python
print(airports.show())

airports = airports.withColumnRenamed("faa", "dest")

flights_with_airports = flights.join(airports, on='dest', how='leftouter')

print(flights_with_airports.show())
```

## Getting started with machine learning pipelines
- At the core of the `pyspark.ml` module are the `Transformer` and `Estimator` classes. 
- `Transformer` : `.transform()`으로 DataFrame을 새로운 DataFrame으로 변환
- `Estimator` : `.fit()`으로 모델을 fitting하여 model object를 return
### Data types
- spark ml을 하려면 data가 numeric이여야 한다.
- data를 import할 떄, spark session이 자동으로 type을 결정해주지만 직접 할당도 당연히 가능하다.
- `.cast()`을 columns, `.withColumn()`은 DataFrame에 사용된다.
  - `dataframe = dataframe.withColumn("col", dataframe.col.cast("new_type"))`
### Create a new column
```python
df = df.withColumn("is_late", df.arr_delay > 0)

df = df.withColumn("label", df.is_late.cast('integer'))
```

### Strings and factors
- 아래처럼 one-hot encoding
  
```python
# Create a StringIndexer
carr_indexer = StringIndexer(inputCol="carrier", outputCol="carrier_index")

# Create a OneHotEncoder
carr_encoder = OneHotEncoder(inputCol="carrier_index", outputCol="carrier_fact")
```

### Assemble a vector
- combine all of the columns containing our features into a single column

```python
# y값은 data에 label이라는 이름으로 존재해야한다
vec_assembler = VectorAssembler(inputCols=["month", "air_time", "carrier_fact", "dest_fact", "plane_age"], outputCol='features')
```

### Pipeline
```python
# Import Pipeline
from pyspark.ml import Pipeline

# Make the pipeline
flights_pipe = Pipeline(stages=[dest_indexer, dest_encoder, carr_indexer, carr_encoder, vec_assembler])
```

### fit, transform
- `piped_data = flights_pipe.fit(model_data).transform(model_data)`

### Split data
- `training, test = piped_data.randomSplit([.6, .4])`


## Model tuning and selection
```python
# Import LogisticRegression
from pyspark.ml.classification import LogisticRegression

# Create a LogisticRegression Estimator
lr = LogisticRegression()

# Import the evaluation submodule
import pyspark.ml.evaluation as evals

# Create a BinaryClassificationEvaluator
evaluator = evals.BinaryClassificationEvaluator( metricName="areaUnderROC")

# Import the tuning submodule
import pyspark.ml.tuning as tune

# Create the parameter grid
grid = tune.ParamGridBuilder()

# Add the hyperparameter
grid = grid.addGrid(lr.regParam, np.arange(0, .1, .01))
grid = grid.addGrid(lr.elasticNetParam, [0, 1])

# Build the grid
grid = grid.build()

# Create the CrossValidator
cv = tune.CrossValidator(estimator=lr,
               estimatorParamMaps=grid,
               evaluator=evaluator
               )

# Call lr.fit()
best_lr = lr.fit(training)

# Print best_lr
print(best_lr)

# Use the model to predict the test set
test_results = best_lr.transform(test)

# Evaluate the predictions
print(evaluator.evaluate(test_results))
```