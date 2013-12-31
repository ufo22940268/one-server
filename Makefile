.PHONY: docs test

help:
	@echo "  env         create a development environment using virtualenv"
	@echo "  deps        install dependencies using pip"
	@echo "  clean       remove unwanted files like .pyc's"
	@echo "  lint        check style with flake8"
	@echo "  test        run all your tests using py.test"

env:
	sudo easy_install pip && \
	pip install virtualenv && \
	virtualenv env && \
	. env/bin/activate && \
	make deps

deps:
	pip install -r requirements.txt

clean:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' -exec rm -f {} \;

lint:
	flake8 --exclude=env .

test:
	py.test -s -x tests

test-current:
	py.test -m current -s -x tests

testdb:
	py.test -s -x tests/test_db.py

testride:
	py.test -s -x tests/test_ride.py

testuser:
	py.test -s -x tests/test_user.py

server:
	./manage.py runserver
