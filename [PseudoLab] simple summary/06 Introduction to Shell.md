- https://minsoo9506.github.io/blog/linux/
  - 여기에 없는 내용 위주 or 모르는 내용 위주 추가 정리

## Manipulating files and directories
- shell에서 `/`으로 시작하면 절대경로, 아니면 상대경로로 이해한다.
- copy
  - `cp original.txt duplicate.txt`
  - 여러개를 한번에 할 수도 있다. seasonal에 있는 두 파일을 backup 디렉토리로 `cp seasonal/spring.csv seasonal/summer.csv backup`
- 이름바꾸기
  - `mv`를 통해서 파일 이동 뿐만 아니라 이름도 바꾼다 : `mv winter.csv winter.csv.bck`
- 디렉토리 지우기
  - `rmdir`
  - 단, 디렉토리에 파일이 없어야 한다

## Manupulating data
- 파일 내용 보기
  - `cat`
  - `less` : 파일의 한 페이지만 보여준다. spacebar로 뒤로가기 `:n`으로 다음페이지, `q`로 끝낼 수 있다.
  - `head -n 5` : 5줄만 보기
- 디렉토리 모든 내용 보기
  - `ls -R` : 현재 디렉토리에 있는 모든 디렉토리와 파일을 보여준다.
- 파일에서 column 확인
  - `cut -f 2-5,8 -d , sample.csv` : select columns 2 through 5 and columns 8, using comma as the separator
- 최근 명령어 보기
  - `history`
  - 최근 명령어를 1부터 시작하는 숫자를 할당하고 순서를 보여준다. `!숫자`를 통해 해당 명령어를 실행시킬 수 있다.
- 특정 값을 갖고 있는 부분 보기
  - `grep`
    - `c`: print a count of matching lines rather than the lines themselves
    - `h`: do not print the names of files when searching multiple files
    - `i`: ignore case (e.g., treat "Regression" and "regression" as matches)
    - `l`: print the names of files that contain matches, not the matches
    - `n`: print line numbers for matching lines
    - `v`: invert the match, i.e., only show lines that don't match

## Combining tools
- command line 결과 저장
  - `head -n 5 seasonal/summer.csv > top.csv` 에서 처럼 `>` 이용한다. redirect 하는 것이다.
- 명령어 이어서 사용
  - `|` : pipe simbol 이용
  - `head -n 5 seasonal/summer.csv | tail -n 3`
- 파일 characters, words, lines 수 세기
  - `wc`
    - `-c`, `-w`, `-l` : characters, words, lines 옵션 
- 여러개의 파일을 한번에 다룰 수 있다
  - 예를 들어 `cut -d , -f 1 seasonal/winter.csv seasonal/spring.csv seasonal/summer.csv seasonal/autumn.csv` 처럼 나열하면 된다.
  - 그런데 이런 경우 `cut -d , -f 1 seasonal/*.csv` 이런식으로 하면 더 편하다
  - `*`:  means "match zero or more characters"
  - `?`: matches a single character
    - `201?.txt` will match `2017.txt` or `2018.txt`, but not `2017-01.txt`
  - `[...]`: matches any one of the characters inside the square brackets
    - `201[78].txt` matches `2017.txt` or `2018.txt`, but not `2016.txt`
  - `{...}`: matches any of the comma-separated patterns inside the curly brackets
    - `{*.txt, *.csv}` matches any file whose name ends with `.txt` or `.csv`
- 정렬
  - `sort`
- 똑같은 값 제거
  - `uniq`
    - 근데 바로 근접한 경우만 지운다
    - 그래서 `sort`랑 자주 같이 쓰인다
    - `uniq -c`로 똑같은게 몇 개인지 알 수 있다 (pandas의 value_count랑 같은 기능인듯)

## Batch processing
- variable 값 보는 법
  - `echo`
    - `echo $SHELL` 이런식으로
- shell variable
  - `training=seasonal/summer.csv` 처럼 띄어씌기 없이 `=`부호로 할당한다
- command 반복
  - shell variable을 이용하여 loop문도 사용할 수 있다.
  - 예를 들어
    - `for filetype in gif jpg png; do echo $filetype; done`
    - `for filename in seasonal/*.csv; do echo $filename; done`
    - `for file in seasonal/*.csv; do head -n 2 $file | tail -n 1; done`

## Creating new tools
- text editor를 이용하여 file을 수정할 수 있다.
  - nano
    - `CTRL + O` : 끝나고 저장 (Enter를 눌러야함)
    - `CTRL + X` : editor 나가기
    - `CTRL + K` : 해당 line을 cut(잘라내기)
    - `CTRL + U` : 붙여넣기
- 내가 했던 명령어 저장하는 법
  - `history`를 실행하고 pipe로 `tail -n `을 이용하여 원하는 만큼 output을 만든 뒤에 이를 `>`하여 파일로 저장
  - 예) `history | tail -n 5 > my_command.txt`
- command를 저장하여 다시 실행하는 법
  - 실행하고 싶은 command를 `.sh`파일로 저장
  - `bash 파일이름.sh` 하면 된다.
- script에 filename을 넣는 법
  - `$@`: all of the command-line parameters given to the script
  - `bash unique-lines.sh seasonal/summer.csv` 이런식으로 `.sh`뒤에 filename을 넣으면 script에 `$@`에 넣는 것
- script에 parameter를 넣는 법
  - 예)
    - `cut -d , -f $2 $1`을 column.sh에 저장
    - `bash column.sh seasonal/autumn.csv 1`
- shell script에 loop 사용
  - indent는 필요없지만
```sh
# Print the first and last data records of each file.
for filename in $@
do
    head -n 2 $filename | tail -n 1
    tail -n 1 $filename
done
```