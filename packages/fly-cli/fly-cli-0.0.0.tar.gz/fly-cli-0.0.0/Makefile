default:

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

build:
	python setup.py sdist

check: build
	twine check dist/*

upload: build
	twine upload dist/*
