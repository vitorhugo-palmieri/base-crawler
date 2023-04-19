image:
	docker build -t base-crawler .

clean:
	docker kill $$(docker ps -q)
	docker rm $$(docker ps -a -q)

remove-containers:
	docker rm $$(docker ps -a -q)

remove-debug-files:
	rm -f tests/files/debug/*

down:
	docker-compose down

run-unit-tests: image
	docker-compose run --rm --entrypoint ./scripts/run-unit-tests.sh base-crawler

run-integration-tests: image remove-debug-files
	docker-compose --env-file .env run  --entrypoint ./scripts/run-integration-tests.sh base-crawler
shell: image
	docker-compose run --entrypoint /bin/bash base-crawler

run: image remove-debug-files
	docker-compose up