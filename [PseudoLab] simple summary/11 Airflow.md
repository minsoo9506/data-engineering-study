## Intro to Airflow
- creation, scheduling, monitoring
- implements workflow as DAG
- code, command-line, web 등으로 사용가능

### Airflow DAG
- DAG
  - directed, acyclic, graph

```python
# Import the DAG object
from airflow.models import DAG

# Define the default_args dictionary
default_args = {
  'owner': 'dsmith',
  'start_date': datetime(2020, 1, 14),
  'retries': 2
}

# Instantiate the DAG object
etl_dag = DAG('example_etl', default_args=default_args)
```

## Implementing Airflow DAGs
### Airflow operators
- Operators
  - respresent a single task in a workflow
  - run independently
  - generally do not share information
  - various operators to perform different task
  - 위치, 환경등에 영향을 받기 때문에 주의해야한다.
- BashOperator
  - bash command, script를 실행한다.

```python
# Import the BashOperator
from airflow.operators.bash_operator import BashOperator

# Define the BashOperator 
cleanup = BashOperator(
    task_id='cleanup_task',
    # Define the bash_command
    bash_command="cleanup.sh",
    # Add the task to the dag
    dag=analytics_dag
)
```

### Airflow tasks
- task
  - instance of operator
  - 주로 python에서 변수에 할당된다.
  - Airflow에서는 주로 `task_id`로 불린다.
- Task dependencies
  - task의 순서를 정의, 없으면 누가 먼저될지 모름
  - `bitshift` operator(`>>, <<`)로 정의된다.
  - upstream = before, downstream = after : `먼저할거 >> 나중에할거` 이렇게 표시

### Additional operators
- PythonOperator
  - execute a python function  / callable

```python
def pull_file(URL, savepath):
    r = requests.get(URL)
    with open(savepath, 'wb') as f:
        f.write(r.content)   
    # Use the print method for logging
    print(f"File pulled from {URL} and saved to {savepath}")

from airflow..python_operator import PythonOperator

# Create the task
pull_file_task = PythonOperator(
    task_id='pull_file',
    # Add the callable
    python_callable=pull_file,
    # Define the arguments
    op_kwargs={'URL':'http://dataserver/sales.json', 'savepath':'latestsales.json'},
    dag=process_sales_dag
)
```

- EmailOperator

### Airflow scheduling
- 특정 instance가 원하는 시간에 작동하도록 하고 싶은 경우 `schedule_interval` 이용
- Schedule
  - `start_date`
  - `end_date`
  - `max_tries`
  - `schedule_interval` : cron syntax 사용

```python
# Update the scheduling arguments as defined
default_args = {
  'owner': 'Engineering',
  'start_date': datetime(2019, 11, 1),
  'email': ['airflowresults@datacamp.com'],
  'email_on_failure': False,
  'email_on_retry': False,
  'retries': 3,
  'retry_delay': timedelta(minutes=20)
}

dag = DAG('update_dataflows', default_args=default_args, schedule_interval='30 12 * * 3')
```

## Maintaining and monitoring Airflow workflows
### Airflow sensors
- sensors
  - 특정 조건이 true가 될 때 까지 기다리는 operator
  - `airflow.sensors.base_sensor_operator`
- File sensor
  - `airflow.contrib.sensors`
  - 특정 위치에 file이 있는지 확인하는 역할
- 그이외에도 다양한 sensor 존재

### Airflow executors
- executors run tasks
- different executors handle running the tasks differently
- excutors
  - `SequentialExecutor`
  - `LocalExecutor`
  - `CeleryExecutor`
- SequentialExecutor
  - default Airflow executor
  - 한번에 하나의 task실행
  - debugging하기 좋다.
- LocalExecutor
  - task를 process처럼 다룬다.
  - parallelism을 사용할 수 있다.
- CeleryExecutor
  - 여러 worker system을 정의할 수 있다.

### Debugging and troubleshooting in Airflow
- 여러가지 이유 존재

### SLAs and reporting in Airflow
- SLA : service level agreement
- SLA Miss is any situation where a task or DAG does not meet the expected timing
- SLA Miss가 발생하면 web UI, log를 통해 확인할 수 있다.
- Defining SLAs
  - using the `sla` argument on the task
  - on the `default_args` dictionary

```python
# using the `sla` argument on the task
test_dag = DAG('test_workflow', start_date=datetime(2020,2,20), schedule_interval='@None')

task1 = BashOperator(task_id='first_task',
                     sla=timedelta(hours=3),
                     bash_command='initialize_data.sh',
                     dag=test_dag)

# on the `default_args` dictionary
default_args = {
  'start_date': datetime(2020, 2, 20),
  'sla': timedelta(minutes=30)
}

test_dag = DAG('test_workflow', default_args=default_args, schedule_interval='@None')
```

- timedelta object
  - `datetime` 라이브러리에 있다.

## Building production pipelines in Airflow
### Working with templates
- `jinja` 이용

```python
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

default_args = {
  'start_date': datetime(2020, 4, 15),
}

cleandata_dag = DAG('cleandata',
                    default_args=default_args,
                    schedule_interval='@daily')

# 괄호안에 띄어씌기 주의
templated_command = """
  bash cleandata.sh {{ ds_nodash }} {{ params.filename }}
"""
clean_task = BashOperator(task_id='cleandata_task',
                          bash_command=templated_command,
                          params={'filename': 'salesdata.txt'},
                          dag=cleandata_dag)
clean_task2 = BashOperator(task_id='cleandata_task2',
                          bash_command=templated_command,
                          params={'filename': 'supportdata.txt'},
                          dag=cleandata_dag)

```

### More templates
```python
templated_command="""
{% for filename in params.filenames %}
  echo "Reading {{ filename }}"
{% endfor %}
"""
```
- variables
  - Airflow built-in runtime variables
  - `{{ ds }}, {{ dag }}` 등등

### Branching
- conditional logic을 제공
- `BranchPythonOperator`
- branch_task의 결과에 따라 다른 task들로 가게 하고 싶을 때 사용

```python
# Create a function to determine if years are different
def year_check(**kwargs):
    current_year = int(kwargs['ds_nodash'][0:4])
    previous_year = int(kwargs['prev_ds_nodash'][0:4])
    if current_year == previous_year:
        return 'current_year_task'
    else:
        return 'new_year_task'

branch_task = BranchPythonOperator(task_id='branch_task', dag=branch_dag,
                                   python_callable=year_check, provide_context=True)
branch_dag >> current_year_task
branch_dag >> new_year_task
```

### Creating a production pipeline
- run a specific task from command-line
  - `airflow run <dag_id> <task_id> <date>`
- run a full DAG
  - `airflow trigger_dag -e <date> <dag_id>`
- operator 복습
  - BashOperator는 `bash_command` 필요
  - PythonOperator는 `python_callable` 필요
  - BranchPythonOperator는 `python_callable`, `provied_context=True` 필요
  - FileSensor는 `filepath`, `mode` or `poke_interval` 필요