## Downloading Data on the Command Line
### Downloading data using curl
- `curl`
  - `curl [option] [URL]`
- option
  - `-O` : file의 원래 이름 그대로 저장
  - `-o` : 원하는 이름으로 저장 `curl -o name.txt https~`
- data가 여러개면 하나씩 URL 다 하지 말고 `*`이용, `[1-100]`처럼 원하는 숫자도 가능
  
### Downloading data using Wget
- `Wget`
  - 많은 파일을 다운받을 때 `curl`보다 좋다.
  - `wget [option] [URL]`
- option
  - `-b` : download occur in the background
  - `-q` : turn off the wget output
  - `-c` : resume broken download

### Advanced downloading using Wget
- 특정 file에 url들이 있을 때: `-i`
  - `wget -i url_list.txt`
- Set upper download bandwidth limit (bytes per secone): `--limit-rate`
  - `wget --limit-rate=200k -i url_list.txt`
- Set a pause time between file download: `--wait`
  - `wget --wait=2.5 -i url_list.txt`

## Data Cleaning and Munging on the Command Line
### csvkit
- `in2csv` : file을 csv로 바꿔준다
  - `in2csv data.xlsx > data.csv`
  - `in2csv -n data.xlsx`하면 모든 sheet 이름 보여준다. 그리고 `in2csv data.xlsx --sheet "sheet이름" > data.csv` 하면 된다.
- `csvlook` : data preview on the command line
  - `csvlook data.csv`
- `csvstat` : descriptive stats on csv
  - `csvstat data.csv`
- `csvcut` : filtering data by column
  - `csvcut -n data.csv` : 모든 column 이름
  - `csvcut -c 1 data.csv`  : 첫번째 column 보여줌, 숫자말고 column이름도 가능, 여러개 보려면 그냥 여러개 쓰면 된다
- `csvgrep` : filtering data by row
  - `csvgrep -c "name" -m "minsoo" data.csv` : name column에서 값이 minsoo인 row
- `csvstack` : csv 파일 여러 개 쌓기
  - `csvstack data1.csv data2.csv > data.csv` : 같은 컬럼을 갖는 파일 합치기
  - `csvstack -g "one", "two" data1.csv data2.csv > data.csv` : 이러면 새로운 column이 하나 더 생기고 그 값들(`one`, `two`)은 각 row가 어떤 csv 파일에서 왔는지 나타낸다
- chaining command-line commands
  - `;` : 한줄에 command를 쓰고 순서대로 실행
  - `&&` : 먼저 앞에 나온 command가 성공을 해야 뒤의 command가 실행

## Database Operations on the Command Line
### Pulling data from DB : `sql2csv` 
- 원하는 데이터를 `.csv`로 뽑아낼 수 있다
  - `sql2csv --db "sqlite:///data.db" --query "SELECT * FROM data_ex" > data.csv`
  - 위에서 Postgre, MySQL은 `postgres:///`, `mysql:///` 이고 끝에 `.db`는 필요없다.

### Manipulating data using SQL syntax : `csvsql`
- 너무 큰 데이터는 x
- local csv file에 SQL을 사용
- `csvsql --query "SELECT * FROM data LIMIT 1" data.csv`

### Pushing data back to DB : `csvsql`
- DB에 SQL바로 쓸 수도 있고
- table을 만들 수도 있다.
- `csvsql --db "sqlite:///data.db --insert data.csv`

## Data Pipeline on the Command Line
### Python on the command line
- `.py`를 이용해서 command line 에서 사용 : `python 이름.py`

### Python package installation with `pip`
- `pip`으로 패키지들 설치
- `pip --version` : `pip`의 버전이고 이는 python의 버전과 맞아야한다.
- `pip list` : `pip`로 설치한 것들 보여준다.
- `pip install 패키지이름`
- `pip install --upgrade 패키지이름` : 패키지 버전 업그레이드
- `pip install -r requirements.txt` : requirements.txt에 있는 패키지들을 설치한다.

### Data job automation with `cron`
- `Cron`
  - time-based job-scheduler
  - pre-installed MacOs, Unix
  - automate jobs like system maintenance, bash scripts, python jobs...
- Crontab
  - cental file to keep track of cron jobs
- `echo "* * * * * python hello_world.py" | crontab`
  - `*` 이는 각 minute, hour, day, month, year 를 의미한다. 예를 들어, 15분 마다 특정파일을 실행하고 싶으면 `15 * * * * python file.py` 이렇게 한다.
  - `crontab -l` : 지금 crontab에 있는 것들 보여준다.