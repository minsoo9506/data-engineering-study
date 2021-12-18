Dockerfile이 있는 위치에서 아래의 명령어 사용하면 이미지 만들고 컨테이너를 실행한다.

```
$ docker build -t minsoo/flaskapp:latest ./
$ docker run -d -p 8000:8000 minsoo/flaskapp
```
- `-t 이미지이름:버전`
- `-d` : 백그라운드 실행
- `-p 8000:8000` : port mapping