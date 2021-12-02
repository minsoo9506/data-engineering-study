## Introduction to Big Data analysis with Spark
### What is Big data?
- 3V
  - volume, variety, velocity
- features of Spark
  - Distributed cluster
  - in-memory computation
  - fast data processing
- Spark Components
  - SparkSQL
  - MLlib
  - GraphX
  - Spark Streaming
- Spark modes of deployment
  - Local mode 
  - Cluster mode

### PySpark
scala랑 성능도 비슷

- Spark shell
  - interactive environment for running Spark Jobs
  - Helpful for fast interactive prototyping 
  - scala, python, R shell DL WHSWO
- PySpark shell
  - python-basaed cli tool
- SparkContext : entry point into the world of Spark
  - entry point is a way of connecting to Spark cluster
  - default SparkContext called `sc`

```python
sc.version
sc.pythonVer
# URL of the cluster or 'local' string to run in local mode of SparkContext
sc.master
```

### Review of functional programming in Python
- `lambda`
  - no return statement for lambda
  - can put lambda function anywhere

```python
f = lambda x : x * 2
print(f(1))
```

- `map`
  - function과 list를 받고 각 원소들을 함수에 적용한 값을 return
  - `map(function, list)`

```python
items = [1,2,3]
list(map(lambda x: x*2, items))
```

- `filter`
  - function과 list를 받고 각 원소들을 함수에 넣고 true인 원소만 return
  - `filter(function, list)`

```python
items = [1,2,3]
list(filter(lambda x: (x%2 != 0), items))
```

## Programming in PySpark RDD

### Abstracting Data with RDDs
- Creating RDD
  - Parallelizing an existing collection of objects
  - External datasets
  - From existing RDD
- Parallelized collection
```python
sc.parallelize([1,2,3,4])
```
- From external dataset
```python
sc.textFile("sample.txt")
```

### Basic RDD Transformations and Actions
- Lazy operation
  - Transformations create new RDD -> Actions perform computation on the RDD

- RDD Transformations
  - `map()`, `filter()`, `flatMap()`, `union()`
- RDD Actions
  - `collect()`, `take()`, `first()`, `count()`

```python
# Create map() transformation to cube numbers
cubedRDD = numbRDD.map(lambda x: x**3)
# Collect the results
numbers_all = cubedRDD.collect()
# Print the numbers from numbers_all
for numb in numbers_all:
	print(numb)
```

### Pair RDDs in PySpark
- creating pair RDD
  - 2가지 방법
    - From a list of key-value tuple
    - From a regular RDD

```python
# Create PairRDD Rdd with key value pairs
Rdd = sc.parallelize([(1,2),(3,4),(3,6),(4,5)])
```
- Transformation on pair RDD
  - `reduceByKey(func)`, `groupByKey()`, `SortByKey()`, `join()` ...

```python
# Apply reduceByKey() operation on Rdd
Rdd_Reduced = Rdd.reduceByKey(lambda x, y: x + y)
# Sort the reduced RDD with the key by descending order
Rdd_Reduced_Sort = Rdd_Reduced.sortByKey(ascending=False)
```

### Advanced RDD Actions
- 여러가지 존재

## PySpark SQL & DataFrames
### Abstracting data with datframe
- DataFrame
  - immutable distributed collection of data with named columns
  - designed for processing both structured and semi-structured data
  - python, R, Scala, Java
  - support both SQL queries or expression methods
- SparkSession
  - Entry point for DataFrame API
  - `spark`라는 이름으로 pyspark shell에서 이용된다.
- Creating DataFrames in PySpark
  - existing RDD를 이용하여 SparkSession의 `createDataFrame()` 이용
  - 외부로부터 read
- Creating DataFrame from RDD
  - `spark.createDataFrame(rdd, schema=col_name)`
- Creating DataFrame from read
  - `spark.read.csv("data.csv", header=True, inferScheme=True)`

### Operating on Dataframe in PySpark
- DataFrame operations: Transformation, Action
- Transformation
  - `select()`, `filter()`, `groupby()`, `orderby()`, `dropDuplicates()`, `withColumnRenamed()`
- Actions
  - `head()`, `show()`, `count()`, `describe()`

### Interacting with DataFrame using PySpark SQL
- DataFrame API vs SQL queries
  - 두 가지를 이용하여 SparkSQL과 interact 가능
  - DataFrame API는 programmatic domain-specific language for data를 제공
  - SQL queries는 명확하고 이해하기 쉽다.
- Executing SQL Queries
  - `sql()`
  - SQL사용하려면 tempView를 만들어야한다.

```python
df.createOrReplaceTempView("table1")
query = '''SELECT ID_NAME FROM table1'''
result = spark.sql(query)
result.show(5)
```

### Data Visualization in PySpark using Dataframe
- python에서 사용하는 것들은 사용불가
  - 대신 pyspark_dist_explore library, toPandas(), HandySpark library
- `Pyspark_dist_explore`
  - `hist()`, `distplot()`, `pandas_histogram()`
 
```python
hist(df, bins=20)
```

- `toPandas()`
  - pandas DF로 만들어서 시각화하는 방법
  
- pandas DataFrame vs pyspark DataFrame
  - pandas는 single-server
  - pandas는 operation를 바로 적용되지만 pyspark는 lazy
  - pandas DataFrame은 mutable, pyspark DataFrame은 immutable

- HandySpark

```python
hdf = df.toHandy()
hdf.cols["Age"].hist()
```

## ML with PySpark 
- `pyspark.mllib` is the builtin library for RDD-based API.
### Collaborative filtering

- Collaborative filtering
  - 비슷한 관심사를 같는 유저를 찾는 것

```python
# Load the data into RDD
data = sc.textFile(file_path)
# Split the RDD 
ratings = data.map(lambda l: l.split(','))
# Transform the ratings RDD
ratings_final = ratings.map(lambda line: Rating(int(line[0]), int(line[1]), float(line[2])))
# Split the data into training and test
training_data, test_data = ratings_final.randomSplit([0.8, 0.2])
# Create the ALS model on the training data
model = ALS.train(training_data, rank=10, iterations=10)
# Drop the ratings column 
testdata_no_rating = test_data.map(lambda p: (p[0], p[1]))
# Predict the model  
predictions = model.predictAll(testdata_no_rating)
# Return the first 2 rows of the RDD
predictions.take(2)
# Prepare ratings data
rates = ratings_final.map(lambda r: ((r[0], r[1]), r[2]))
# Prepare predictions data
preds = predictions.map(lambda r: ((r[0], r[1]), r[2]))
# Join the ratings data with predictions data
rates_and_preds = rates.join(preds)
# Calculate and print MSE
MSE = rates_and_preds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
print("Mean Squared Error of the model for the test data = {:.2f}".format(MSE))
```

### Classification

```python
# Load the datasets into RDDs
spam_rdd = sc.textFile(file_path_spam)
non_spam_rdd = sc.textFile(file_path_non_spam)
# Split the email messages into words
spam_words = spam_rdd.flatMap(lambda email: email.split(' '))
non_spam_words = non_spam_rdd.flatMap(lambda email: email.split(' '))
# Create a HashingTf instance with 200 features
tf = HashingTF(numFeatures=200)
# Map each word to one feature
spam_features = tf.transform(spam_words)
non_spam_features = tf.transform(non_spam_words)
# Label the features: 1 for spam, 0 for non-spam
spam_samples = spam_features.map(lambda features:LabeledPoint(1, features))
non_spam_samples = non_spam_features.map(lambda features:LabeledPoint(0, features))
# Combine the two datasets
samples = spam_samples.union(non_spam_samples)
# Split the data into training and testing
train_samples,test_samples = samples.randomSplit([0.8, 0.2])
# Train the model
model = LogisticRegressionWithLBFGS.train(train_samples)
# Create a prediction label from the test data
predictions = model.predict(test_samples.map(lambda x: x.features))
# Combine original labels with the predicted labels
labels_and_preds = test_samples.map(lambda x: x.label).zip(predictions)
# Check the accuracy of the model on the test data
accuracy = labels_and_preds.filter(lambda x: x[0] == x[1]).count() / float(test_samples.count())
print("Model accuracy : {:.2f}".format(accuracy))
```

### Clustering

```python
# Load the dataset into an RDD
clusterRDD = sc.textFile(file_path)
# Split the RDD based on tab
rdd_split = clusterRDD.map(lambda x: x.split("\t"))
# Transform the split RDD by creating a list of integers
rdd_split_int = rdd_split.map(lambda x: [int(x[0]), int(x[1])])
# Count the number of rows in RDD 
print("There are {} rows in the rdd_split_int dataset".format(rdd_split_int.count()))
# Train the model with clusters from 13 to 16 and compute WSSSE
for clst in range(13, 17):
    model = KMeans.train(rdd_split_int, clst, seed=1)
    WSSSE = rdd_split_int.map(lambda point: error(point)).reduce(lambda x, y: x + y)
    print("The cluster {} has Within Set Sum of Squared Error {}".format(clst, WSSSE))
# Train the model again with the best k
model = KMeans.train(rdd_split_int, k=15, seed=1)
# Get cluster centers
cluster_centers = model.clusterCenters
# Convert rdd_split_int RDD into Spark DataFrame and then to Pandas DataFrame
rdd_split_int_df_pandas = spark.createDataFrame(rdd_split_int, schema=["col1", "col2"]).toPandas()
# Convert cluster_centers to a pandas DataFrame
cluster_centers_pandas = pd.DataFrame(cluster_centers, columns=["col1", "col2"])
# Create an overlaid scatter plot of clusters and centroids
plt.scatter(rdd_split_int_df_pandas["col1"], rdd_split_int_df_pandas["col2"])
plt.scatter(cluster_centers_pandas["col1"], cluster_centers_pandas["col2"], color="red", marker="x")
plt.show()
```
