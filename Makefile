run:
	nohup adb -a nodaemon server start &> /dev/null &
	docker compose up -d 
