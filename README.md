# herren coding test
## overview
- Django을 이용하여 API을 구현 했습니다.
- mysql와 redis을 사용 했습니다.
- 많은 양의 메일을 보내는 경우를 생각하여 메일 전송은 비동기 처리로 진행 했습니다.
- 비동기 처리에는 redis-queue 사용 했습니다.
- 구독자 조회 기능을 추가 했으며, 조회시 토큰이 필요합니다.(토큰은 아래 설명 참고)
- 구독 취소 기능은 구독만 취소하는 기능과, 데이터도 삭제하는 기능으로 나누어서 구현 했습니다.
- docker-compose을 이용하여 django, gunicorn, mysql, redis를 dockerize 했습니다.

## build 및 초기화
- clone을 받은 뒤 src 디렉토리로 이동
- (sudo) docker-compose up -d --force-recreate 명령어로 docker-compose 실행
-  docker-compose run django python manage.py migrate 명령어로 db migrate
- local에서 test 하기 위해서는 redis와 mysql이 있어야 한다.
- local에서 비동기 서버 run 명령어: python manage.py rqworker
<br>
## git branch
- master: 초기 셋팅 상태
- mailing_v1: email 도메인 구분 없이 메일 전송하는 version 1 (docker)
- mailing_v2: naver.com과 google.com을 구분하여 메일 전송하는 verson2 (docker)
- mailing_v3: local 실행용 version 2
<br>
<br>

# 메일링 리스트 API
## post
`host:8000/subscribe`
### body 

|Key|type|설명|
|:--:|:--:|-----|
|email|string|구독자 email 주소|
|name|string|구독자 주소|

### Description
- 구독자 등록
- 구독 취소자 재등록
- 이미 구독 중인 email error 처리
- 지원하지 않는 양식 : email 주소에는 반드시 '**@**'와 '**.**'이 포함 되어야 한다.  
- status code
  - 201 : 정상적으 구독자 등록. 
  - 400 : key error.
  - 409 : 이미 구독 중인 email.
<br>

## patch
`host:8000/subscribe`
### body 

|Key|type|설명|
|:--:|:--:|-----|
|email|string|구독자 email 주소|

### Description
- 구독 취소 등록
- DB에 데이터는 남기고 구독 여부만 취소
- 지원하지 않는 양식 : email 주소에는 반드시 '**@**'와 '**.**'이 포함 되어야 한다.  
- status code
  - 201 : 정상적으 구독 취소. 
  - 400 : key error.
  - 404 : DB에 없는 email.
  - 409 : 이미 구독 중인 email.
<br>

## delete
`host:8000/subscribe` or `host:8000/subscribe/{subscribe_id}`

### Description
- DB에서 데이터 완전 삭제
- path parameter(subscribe_id)가 없는 경우 DB 전제 삭제
- path parameter(subscribe_id)가 있는 경우 해당 id의 데이터만 삭제
- status code
  - 204 : 정상적으 데이터 삭제. 
  - 404 : DB에 없는 id.
<br>

## get
`host:8000/subscribe` or `host:8000/subscribe/{subscribe_id}`
### headers

|Key|value|설명|
|:--:|:--:|-----|
|Authorization|herren-recruit-python|정보 조회 토큰|

### Description
- 구독자 DB 조회
- 구독을 취소 했어도, db에 남아 있으면 조회 가능
- path parameter(subscribe_id)가 없는 경우 DB 전제 조회
- path parameter(subscribe_id)가 있는 경우 해당 id의 데이터만 조회
- status code
  - 200 : 정상적으 구독자 조회. 
<br>
<br>
<br>
# 리스트에 있는 구독자들에게 메일 보내기 API
## post
`host:8000/subscribe`
### body 

|Key|type|설명|
|:--:|:--:|-----|
|subjectl|string|메일 제목|
|content|string|메일 내용|

### Description
- DB에 등록된 email 중 구독자들에게만 메일 전송
- version 1: 도메인 구분 없이 메일 전송
- version 2: naver.com과 google.com은 구분하여 메일 전송 
- status code
  - 203 : 정상적으 비동기 처리 실행. 
  - 400 : key error.
<br>
  


 

