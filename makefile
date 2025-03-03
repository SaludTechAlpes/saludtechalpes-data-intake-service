activate:
	if [ -d "venv" ]; then \
        echo "Python 🐍 environment was activated"; \
    else \
        echo "The folder environment doesn't exist"; \
		python -m venv venv; \
        echo "The environment folder was created and the python 🐍 environment was activated"; \
    fi
	. ./venv/bin/activate

install:
	pip3 install -r requirements.txt

run:
	@if [ -z "$(strip $(PORT))" ]; then \
		flask --app ./src run; \
	else \
		flask --app ./src run -p $(PORT); \
	fi

run-docker:
ifeq ($(strip $(PORT)),)
	flask --app ./src run -h 0.0.0.0
else
	flask --app ./src run -p $(PORT) -h 0.0.0.0
endif

run-tests:
	FLASK_ENV=test python -m unittest discover -s tests -p '*Test.py' -v

run-tests-coverage:
	 FLASK_ENV=test coverage run -m unittest discover -s tests -p '*Test.py' -v
	 coverage report -m
	 coverage html
	 coverage report --fail-under=50

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-local-up:
	docker compose -f=docker-compose.local.yaml up --build

docker-local-down:
	docker compose -f=docker-compose.local.yaml down

kubernetes-local-up:
	kubectl apply -f kubernetes/local/k8s-configMap.yaml
	kubectl apply -f kubernetes/local/k8s-secrets.yaml
	kubectl apply -f kubernetes/local/k8s-postgres.yaml
	kubectl apply -f kubernetes/local/k8s-pulsar.yaml
	kubectl apply -f kubernetes/local/k8s-pulsar-init.yaml
	kubectl apply -f kubernetes/local/k8s-deployment.yaml
	kubectl apply -f kubernetes/local/k8s-hpa.yaml
	kubectl apply -f kubernetes/local/k8s-ingress.yaml
	sleep 5
	minikube tunnel

kubernetes-local-down:
	kubectl delete configMap/data-intake-configmap
	kubectl delete secrets/data-intake-secrets
	kubectl delete deploy/pulsar-broker
	kubectl delete deploy/bookkeeper
	kubectl delete deploy/postgres-db
	kubectl delete deploy/zookeeper
	kubectl delete deploy/saludtechalpes-data-intake-service
	kubectl delete ingress/saludtechalpes-data-intake-service-ingress
