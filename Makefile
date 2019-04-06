FULL_COMPOSE=docker-compose -f docker-compose.yml -f docker/compose-elk.yml -p interview
.PHONY=requirements logs up

run_all: build build_logstash full_run

demo: run_all generate-traffic
	@echo -e '----------------------------------------------\n'
	@echo Grafana here: 'https://goo.gl/TQtwSb'
	@echo Grafana user/password: admin/admin
	@echo Setup kibana by guide: 'https://goo.gl/pj4aXb'
	@echo -e '\t\t\t\tEnjoy!'
	@echo -e '----------------------------------------------'

up:
	docker-compose -p interview up -d

run: build up

run_local: venv/bin/pytest
	LOG_DIR=/tmp ./venv/bin/python service/run.py --port=8000

build: venv/bin/pytest
	$(FULL_COMPOSE) build

full_run:
	$(FULL_COMPOSE) up -d

run_elk: build_logstash full_run

build_logstash:
	$(FULL_COMPOSE) build logstash

logs:
	$(FULL_COMPOSE) logs -f --tail=100

kill:
	$(FULL_COMPOSE) down -v --remove-orphans

venv:
	virtualenv --python=python3 venv

requirements: venv
	./venv/bin/pip3 install -r requirements.txt

venv/bin/pytest:
	make requirements

generate-traffic: venv/bin/pytest
	./venv/bin/python scripts/generate_traffic.py -n 50000 -p 15
	./venv/bin/python scripts/generate_traffic.py -n 50000 -p 15
