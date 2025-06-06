APP_NAME    = codelounge
IMAGE_NAME  = codelounge-web
PORT        = 3000

.PHONY: deploy

deploy:
	@echo "👉 소유권을 index:index로 재설정합 중..."
	@sudo chown -R index:index .

	@echo "👉 Git 최신 코드 가져오는 중..."
	git pull

	@echo "🛑 기존 컨테이너 중지 및 제거 중..."
	-docker stop $(APP_NAME) || true
	-docker rm   $(APP_NAME) || true

	@echo "🔍 3000포트 점유 중인 컨테이너 강제 정리 중..."
	-@docker ps --format '{{.ID}}\t{{.Ports}}' | grep ":$(PORT)->" | cut -f1 | xargs -r docker stop
	-@docker ps -a --format '{{.ID}}\t{{.Ports}}'  | grep ":$(PORT)->" | cut -f1 | xargs -r docker rm

	@echo "🗑️   이미지 강제 제거 중..."
	-docker rmi -f $(IMAGE_NAME) || true

	@echo "🐳 새 이미지 빌드 중..."
	docker build -t $(IMAGE_NAME) .

	@echo "🚀 컨테이너 실행 중..."
	docker run -d --name $(APP_NAME) -p $(PORT):$(PORT) $(IMAGE_NAME)

