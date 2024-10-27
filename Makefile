run:
	adb -a nodaemon server start &> /dev/null &
	podman compose up
