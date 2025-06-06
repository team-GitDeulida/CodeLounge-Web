# 🚀 GitHub Actions 기반 자동 배포 (CI/CD) 설정

## 📌 개요

이 프로젝트는 `main` 브랜치에 push 시 GitHub Actions를 통해 **서버에 자동으로 접속 후**, Docker 컨테이너를 중지 → 제거 → 재빌드 → 재실행하는 자동 배포 환경을 구성합니다.

---

## 🛠️ 1. 서버에 SSH 공개 키 등록

### ✅ (1) GitHub Actions용 SSH 키 생성 (로컬 또는 서버)

```bash
ssh-keygen -t rsa -b 4096 -C "github-actions" -f ~/.ssh/github_actions -N ""
```

- 생성된 파일:
  - `~/.ssh/github_actions` → **개인키**
  - `~/.ssh/github_actions.pub` → **공개키**

### ✅ (2) 공개키를 서버에 등록

```bash
cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys
```

> ⚠️ 서버 유저가 `index`일 경우, `index` 계정의 홈 디렉토리에서 수행합니다.

---

## 🔐 2. GitHub 저장소에 비밀키 등록

### ✅ (1) 개인키 내용 복사

```bash
cat ~/.ssh/github_actions
```

### ✅ (2) GitHub → Repository → Settings → Secrets → Actions → `New repository secret`

- `Name`: `SSH_PRIVATE_KEY`
- `Value`: (위에서 복사한 개인키 전체)

---

## 🐳 3. 서버에서 Docker 권한 설정

> GitHub Actions에서 SSH로 접속한 후 Docker 명령을 실행해야 하므로, 유저에게 Docker 권한이 필요합니다.

```bash
sudo usermod -aG docker $USER
newgrp docker  # 또는 reboot
```

> `$USER`는 예: `index`

---

## 🧱 4. 서버의 `Makefile` 예시

```Makefile
deploy:
	@echo "👉 Git 최신 코드 가져오는 중..."
	git pull

	@echo "🛑 기존 컨테이너 중지 및 제거 중..."
	docker stop codelounge || true
	docker rm codelounge || true

	@echo "🔍 3000포트 점유 중인 컨테이너 강제 정리 중..."
	docker ps -aq --filter "publish=3000" | xargs -r docker rm -f

	@echo "🗑️  이미지 강제 제거 중..."
	docker rmi -f codelounge-web || true

	@echo "🐳 새 이미지 빌드 중..."
	docker build -t codelounge-web .

	@echo "🚀 새 컨테이너 실행 중..."
	docker run -d --name codelounge -p 3000:3000 codelounge-web
```

---

## 🔁 5. GitHub Actions 워크플로우 설정

`.github/workflows/deploy.yml` 파일 생성:

```yaml
name: Auto Deploy to VPS

on:
  push:
    branches:
      - main  # 혹은 배포 트리거 브랜치명

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: SSH & Deploy
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: index.zapto.org
          username: index
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          port: 22
          script: |
            cd ~/github/CodeLounge-Web
            git pull
            make
```

---

## ✅ 6. 작동 확인

1. `main` 브랜치에 push
2. GitHub Actions 탭에서 Workflow 실행 로그 확인
3. 서버에서 컨테이너가 재실행되는지 확인

---

## 🌐 참고

- `index.zapto.org`는 `no-ip` 등을 이용한 DDNS 도메인입니다. 도메인이 서버와 연결되어 있어야 합니다.
- HTTPS 문제로 GitHub Actions의 `host:` 값은 **도메인만 입력**하고, `http://`는 생략해야 합니다.
  - ❌ `host: http://index.zapto.org`
  - ✅ `host: index.zapto.org`
