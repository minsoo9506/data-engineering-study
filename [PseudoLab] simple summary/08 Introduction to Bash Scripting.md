## From Command-Line to Bash Script
### Bash script
- `#!/usr/bash`를 맨 첫 줄로 사용
- `bash 이름.sh`로 실행할 수 있고 `#!/usr/bash`이 있으면 `./이름.sh`로 쉽게 실행할 수도 있다.

### Standard streams & arguments
- STDIN-STDOUT-STDERR 가 bash에서 일반적인 stream
- ARGV
  - array of all the arguments given to the program
  - `$` 를 이용

```sh
#!/usr/bash

echo $1
echo $2
echo $@
echo "There are" $# "arguments"
```
- `bash args.sh one two three` 치면 argument들이 들어가는 것이다.
- `$@`는 전체 argument, `$#`는 argument의 갯수

## Variables in Bash Scripting
### Variables in Bash
- `var='minsoo'` 같이 만들면 된다.
- 사용할 때는 `$var`같이 `$`를 꼭 붙여야 한다.
- quotation
  - single quotes `''` : shell이 literally 이해
  - double quotes `""` : shell이 literally 이해하지만 `$`가 들어있는 경우 변수로 이해
  - backticks : shell-within-a-shell, backticks에 들어간 명령어가 실행된다. `$(something)`이렇게 써도 동일한 기능 (근데 이걸 더 많이 쓴다고 함)

### Numeric variables in Bash
- `expr`
  - terminal에서 연산가능
  - 근데 소수는 불가능
  - `expr 1 + 3`
- `bc`
  - 소수점도 가능
  - `echo "10/3" | bc` 하면 3이 나오는데 `echo "scale=3; 10/3" | bc` 하면 3.333이 나온다.
- 당연히 변수할당 가능
  - `var=3`

### Arrays in Bash
- array 만들기
  - `declare -a my_array`처럼 선언을 먼저해도 되고 `my_array=(1 2 3)`처럼 바로 만들어도 된다.
  - comma를 쓰지 않는다.
- indexing
  - `echo $(my_array[0])`
  - python처럼 0부터 시작한다.
  - `my_array[@]`는 전체 원소를 return한다.
  - `my_array[0]=10` 이렇게 값도 바꿀 수 있다.
  - `my_array[@]:N:M` : N부터 시작해서 M개 원소 return한다.
- append
  - `my_array+=(10 20)`
- Associative array
  - python 딕셔너리 같음
  - `declare -A city`
  - `city=([city_name]="Seoul", [population]=100)`
  - 한번에 해도 된다 `declare -A city=([city_name]="Seoul" [population]=100)`
  - `!city[@]` : 모든 key를 보여준다.

## Control Statements in Bash Scripting
### If
- 아래처럼 사용
- `[]` 내부에서 띄어쓰기 주의
- `&&` : and, `||` : or
```sh
x="Queen"
if [ $x == "King" ]; then
    echo "$x is a King"
else
    echo "$x is not a King"
fi
```
- if and command-line programs
```sh
if grep -q Hello words.txt; then
    echo "Hello is inside"
fi
```

### For, While
- For
  - `{start..stop..increment}`

```sh
for x in {1..5..2}
do
  echo $x
done

for book in books/*
do
  echo $book
done

for book in $(ls books/ | grep -i 'air')
do
  echo $book
done
```

- while

```sh
x=1
while [ $x -le 3 ];
do
  echo $x
  ((x+=1))
done
```
### CASE
```sh
case $1 in
  # Match on all weekdays
  Monday|Tuesday|Wednesday|Thursday|Friday)
  echo "It is a Weekday!";;
  # Match on all weekend days
  Saturday|Sunday)
  echo "It is a Weekend!";;
  # Create a default
  *) 
  echo "Not a day!";;
esac
```

## Functions and Automation
### Basic functions in Bash
```sh
function print_hello() {
    echo "Hi~"
}
print_hello
```
### Arguments, return value, scope
```sh
function print_filename {
    echo "The first file is $1"
    for file in $@
    do
        echo "This file is $file"
    done
}

print_filename "file1.txt" "file2.txt"
```
- Bash에서 모든 변수들은 global!
- 이를 제한하기 위해서는 `local`을 사용
  - `local local_var="local!"`
- bash에서 `return`은 함수가 성공했는지 아닌지만 나타낸다. 그 결과는 `$?`으로 확인할 수 있다.

```sh
function return_check {
    echol
}
return_check

# 이렇게 나온다
# 08-func.sh: line 20: echol: command not found
# 127

function sum {
  echo $(expr $1 + $2)
}
result=$(sum 1 20)
echo $result # 21
```

### Scheduling with Cron
- `crontab`file에 cronjob들이 어떻게 돌아가는지 있다.
- `15 10 * * 0 bash script.sh` : 매주 일요일 오전 10시 15분에 진행
- `15,30,45 10 * * 0 bash script.sh` : 매주 일요일 오전 10시 15, 30, 45분에 실행
- `*/15 * * * *` : 매일 15분마다 실행