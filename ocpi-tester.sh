#!/bin/sh

case "$1" in
	start)
		echo "Starting OCPI tester"
		#source env/bin/activate
		flask run --host=0.0.0.0 --port=8080 1>> flaskrun.log &
		echo "OCPI tester started"
		;;
	stop)
		echo "Stopping OCPI Tester"
		sudo pkill -f python3
		echo "OCPI tester stopped"
		;;
	*)
		echo "Usage: ./ocpi-tester.sh {start|stop}"
		exit 1
		;;
esac

exit 0
