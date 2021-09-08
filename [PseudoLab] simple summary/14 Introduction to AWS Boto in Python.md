## Putting Files in the Cloud
- boto3를 통해 AWS이용
- AWS IAM에서 Add user한다. 그러면 key랑 secret이 생성되는데 잘 저장해두자.
```python
import boto3
# Generate the boto3 client for interacting with S3
s3 = boto3.client('s3', region_name='us-east-1', 
                        # Set up AWS credentials 
                        aws_access_key_id=AWS_KEY_ID, 
                         aws_secret_access_key=AWS_SECRET)
# List the buckets
buckets = s3.list_buckets()

# Print the buckets
print(buckets)
```
### Diving into buckets
- S3 Components - Buckets
  - Desktop folder같은 것
  - Own permision policy
  - website storage
  - generate log
  - 이미지, 비디오, csv 등 아무 object나 넣을 수 있다.
- `boto3`를 통해 Bucket을 만들기, 지우기, list보기 가능
- `s3.create_bucket`, `s3.list_buckets`, `s3.delete_bucket`
```python
import boto3

# Create boto3 client to S3
s3 = boto3.client('s3', region_name='us-east-1', 
                         aws_access_key_id=AWS_KEY_ID, 
                         aws_secret_access_key=AWS_SECRET)

# Create the buckets
response_staging = s3.create_bucket(Bucket='gim-staging')
response_processed = s3.create_bucket(Bucket='gim-processed')
response_test = s3.create_bucket(Bucket='gim-test')

# Get the list_buckets response
response = s3.list_buckets()

# Iterate over Buckets from .list_buckets() response
for bucket in response['Buckets']:
  
  	# Print the Name for each bucket
    print(bucket['Name'])

# Delete the gim-test bucket
s3.delete_bucket(Bucket='gim-test')

# Get the list_buckets response
response = s3.list_buckets()

# Print each Buckets Name
for bucket in response['Buckets']:
    print(bucket['Name'])

```
### Uploading and retrieving files
- object의 key는 해당 s3에서 해당 object의 이름으로 이해할 수 있다.
- object는 하나의 bucket에만 들어간다. (unique)
- `s3.upload_file`, `s3.head_object`, `s3.list_objects`, `s3.delete_object`
```python
# Upload final_report.csv with key 2019/final_report_01_01.csv
s3.upload_file(Bucket='gid-staging', 
               # Set filename and key
               Filename='final_report.csv', 
               Key='2019/final_report_01_01.csv')

# Get object metadata and print it
response = s3.head_object(Bucket='gid-staging', 
                       Key='2019/final_report_01_01.csv')

# Print the size of the uploaded object
print(response['ContentLength'])

# List only objects that start with '2018/final_'
response = s3.list_objects(Bucket='gid-staging', 
                           Prefix='2018/final_')

# Iterate over the objects
if 'Contents' in response:
  for obj in response['Contents']:
      # Delete the object
      s3.delete_object(Bucket='gid-staging', Key=obj['Key'])

# Print the keys of remaining objects in the bucket
response = s3.list_objects(Bucket='gid-staging')

for obj in response['Contents']:
  	print(obj['Key'])
```

## Sharing Files Securely
- AWS permission system
  - IAM : 해당 user의 권한 check
  - Bucket Policy : control on the bucket and the object within it
  - ACL : let us set permissions on specific objects within a bucket
  - Presigned URL : provide temporary object permission
- ACL
  - object에 붙어있다고 이해하면 된다.
  - 종류는 private(default), public-read
  - public-read로 하면 `https://{bucket}.s3.amazonaws.com/{key}`로 누구나 다운받을 수 있다.
  - `s3.put_object_acl()`로 ACL을 설정할 수 있고 처음 data를 upload할 때 지정할 수도 있다. (아래처럼)

```python
# Upload the final_report.csv to gid-staging bucket
s3.upload_file(
  # Complete the filename
  Filename='./final_report.csv', 
  # Set the key and bucket
  Key='2019/final_report_2019_02_20.csv', 
  Bucket='gid-staging',
  # During upload, set ACL to public-read
  ExtraArgs = {
    'ACL': 'public-read'})

# List only objects that start with '2019/final_'
response = s3.list_objects(
    Bucket='gid-staging', Prefix='2019/final_')

# Iterate over the objects
for obj in response['Contents']:

    # Give each object ACL of public-read
    s3.put_object_acl(Bucket='gid-staging', 
                      Key=obj['Key'], 
                      ACL='public-read')
    
    # Print the Public Object URL for each object
    print("https://{}.s3.amazonaws.com/{}".format( 'gid-staging', obj['Key']))
```

### Accessing private objects in S3
```python
# Generate presigned_url for the uploaded object
share_url = s3.generate_presigned_url(
  # Specify allowable operations
  ClientMethod='get_object',
  # Set the expiration time
  ExpiresIn=3600, # 초단위
  # Set bucket and shareable object's name
  Params={'Bucket': 'gid-staging','Key': 'final_report.csv'}
)

# Opening a private file
df_list =  [ ] 

for file in response['Contents']:
    # For each file in response load the object from S3
    obj = s3.get_object(Bucket='gid-requests', Key=file['Key'])
    # Load the object's StreamingBody with pandas
    obj_df = pd.read_csv(obj['Body'])
    # Append the resulting DataFrame to list
    df_list.append(obj_df)

# Concat all the DataFrames with pandas
df = pd.concat(df_list)
```
### Sharing files through a website
- html을 s3에 업로드하고 url을 공유하면 된다.

```python
# html 만들기
# Generate an HTML table with no border and selected columns
services_df.to_html('./services_no_border.html',
           # Keep specific columns only
           columns=['service_name', 'link'],
           # Set border
           border=0)

# Upload the lines.html file to S3
s3.upload_file(Filename='lines.html', 
               # Set the bucket name
               Bucket='datacamp-public', Key='index.html',
               # Configure uploaded file
               ExtraArgs = {
                 # Set proper content type
                 'ContentType':'text/html',
                 # Set proper ACL
                 'ACL': 'public-read'})

# Print the S3 Public Object URL for the new file.
print("http://{}.s3.amazonaws.com/{}".format('datacamp-public', 'index.html'))
```

## Reporting and Notifying
### SNS Topics
- AWS에 SNS 서비스 존재
- s3에서와 비슷하게 client 만들고 topic을 만든다.
- 해당 topic의 구독자들은 email, text를 통해 메세지를 받을 수 있다.
- 

```python
# Initialize boto3 client for SNS
sns = boto3.client('sns', 
                   region_name='us-east-1', 
                   aws_access_key_id=AWS_KEY_ID, 
                   aws_secret_access_key=AWS_SECRET)

# Create the city_alerts topic
response = sns.create_topic(Name="city_alerts")
c_alerts_arn = response['TopicArn']

# Print all the topics in SNS
topic_list = sns.list_topics()

# Get the current list of topics
topics = sns.list_topics()['Topics']

for topic in topics:
  # For each topic, if it is not marked critical, delete it
  if "critical" not in topic['TopicArn']:
    sns.delete_topic(TopicArn=topic['TopicArn'])
```

### SNS subscription
```python
# Subscribe Elena's phone number to streets_critical topic
resp_sms = sns.subscribe(
  TopicArn = str_critical_arn, 
  Protocol='sms', Endpoint="+16196777733")

# Subscribe Elena's email to streets_critical topic.
resp_email = sns.subscribe(
  TopicArn = str_critical_arn, 
  Protocol='email', Endpoint="eblock@sandiegocity.gov")

# Deleting multiple subscription
# List subscriptions for streets_critical topic.
response = sns.list_subscriptions_by_topic(
  TopicArn = str_critical_arn)

# For each subscription, if the protocol is SMS, unsubscribe
for sub in response['Subscriptions']:
  if sub['Protocol'] == 'sms':
	  sns.unsubscribe(SubscriptionArn=sub['SubscriptionArn'])

# List subscriptions for streets_critical topic in one line
subs = sns.list_subscriptions_by_topic(
  TopicArn=str_critical_arn)['Subscriptions']

# Print the subscriptions
print(subs)
```

### Sending message
- Publish to Topic 또는 Single SMS
  - Publish to Topic
    - topic이 있어야 한다.
    - subsciption도 있어야 한다.
    - receiver가 여러명일 때 좋다.
    - SMS, Email 둘 다 가능하다.
  - Single SMS
    - topic, subscription이 필요없다.
    - SMS만 가능하다.

```python
# Publish to Topic
# If there are over 100 potholes, create a message
if streets_v_count > 100:
  # The message should contain the number of potholes.
  message = "There are {} potholes!".format(streets_v_count)
  # The email subject should also contain number of potholes
  subject = "Latest pothole count is {}".format(streets_v_count)

  # Publish the email to the streets_critical topic
  sns.publish(
    TopicArn = str_critical_arn,
    # Set subject and message
    Subject = subject,
    Message = message
  )
```

```python
# Single SMS
# Loop through every row in contacts
for idx, row in contacts.iterrows():
    
    # Publish an ad-hoc sms to the user's phone number
    response = sns.publish(
        # Set the phone number
        PhoneNumber = str(row['Phone']),
        # The message should include the user's name
        Message = 'Hello {}'.format(row['Name'])
    )
   
    print(response)
```

## Pattern Rekognition
- Rekognition
  - computer vision API in AWS
  - detect object, extract text from image ...