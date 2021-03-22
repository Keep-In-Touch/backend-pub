MAIN_CONTAINER_NAME=kit_web

# Entry points {{{
build:
	docker-compose -f docker_config/compose-local.yml build
exec:
	docker exec -it kit_web bash
up: run
rebuild: build run
logs:
	docker logs -f $(MAIN_CONTAINER_NAME)
restart:
	docker restart $(MAIN_CONTAINER_NAME)
bash:
	docker exec -it $(MAIN_CONTAINER_NAME) bash
shell:
	docker exec -it $(MAIN_CONTAINER_NAME) bash -c 'python manage.py shell'
attach:
	docker attach $(MAIN_CONTAINER_NAME)
run:
	docker-compose -f docker_config/compose-local.yml up -d
down:
	docker-compose -f docker_config/compose-local.yml down
fix_cross_device:
	# https://gist.github.com/Francesco149/ce376cd83d42774ed39d34816b9e21db
	echo N | sudo tee /sys/module/overlay/parameters/metacopy
# }}}
#  Testing {{{
# This command is used on CI as well.
test:
	docker exec -it $(MAIN_CONTAINER_NAME) pytest --ds=backend.settings.test -s --create-db ./tests
test_coverage:
	docker exec -it $(MAIN_CONTAINER_NAME) pytest --create-db --cov=. --cov-report=xml --junitxml=test-reports/junit.xml ./tests
typing:
	docker exec $(MAIN_CONTAINER_NAME) mypy --config-file .mypy.ini .
# NOTE: Currently in development and has a lot of warnings.
typing_strict:
	docker exec $(MAIN_CONTAINER_NAME) mypy --strict --config-file .mypy.ini libs/
# }}}
# Maintenance {{{
cleanup:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs sudo rm -rf
static:
	docker exec -it $(MAIN_CONTAINER_NAME) bash -c 'python manage.py collectstatic -l --noinput'
makemigrations:
	docker exec -it $(MAIN_CONTAINER_NAME) bash -c 'python manage.py makemigrations'
migrate:
	docker exec -it $(MAIN_CONTAINER_NAME) bash -c 'python manage.py migrate'

# }}}
# vim:foldmethod=marker:foldlevel=1
