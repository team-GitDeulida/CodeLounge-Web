# CodeLounge Web

CodeLounge Web은 다양한 프로그래밍 언어와 프레임워크의 코드 예제를 공유하고 탐색할 수 있는 웹 플랫폼입니다.

## 기능

- 다양한 프로그래밍 언어의 코드 예제 제공
- 실시간 코드 미리보기
- 다크모드 지원
- 반응형 디자인
- 코드 복사 기능

## 기술 스택

- Node.js
- Express.js
- Socket.IO
- EJS
- Bootstrap 5
- Prism.js (코드 하이라이팅)

## 실행 방법

### 1. 일반 실행

1. 저장소 클론
```bash
git clone [repository-url]
cd CodeLoungeWeb
```

2. 의존성 설치
```bash
npm install
```

3. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 열어 필요한 환경 변수를 설정합니다.
```

4. 서버 실행
```bash

# 개발 중
npm run dev   

# 배포
npm start
```

서버가 실행되면 `http://localhost:3000`에서 접속할 수 있습니다.

### 2. Docker 실행

1. Docker 이미지 빌드
```bash
docker build -t codelounge-web .
```

2. Docker 컨테이너 실행
```bash
docker run -p 3000:3000 codelounge-web
```

또는 Docker Compose를 사용하는 경우:
```bash
docker-compose up
```

#### Dockerfile 내용
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

#### docker-compose.yml 내용
```yaml
version: '3'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    command: npm start
```

## 프로젝트 구조

```
CodeLoungeWeb/
├── src/
│   ├── public/          # 정적 파일
│   ├── views/           # EJS 템플릿
│   ├── content/         # 마크다운 컨텐츠
│   ├── utils/           # 유틸리티 함수
│   └── app.js           # 메인 애플리케이션 파일
├── Dockerfile
├── docker-compose.yml
└── package.json
```

## 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요. 


