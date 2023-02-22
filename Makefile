runTests:
	ab -v 4 -c 100 -n 100000000000000 -t 360 http://127.0.0.1:8077/

up:
	docker compose up -d --wait

down:
	docker compose down

upAndRunTests: up runTests down