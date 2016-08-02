SETUP_PY := python setup.py

all:
	$(SETUP_PY) build

install:
	$(SETUP_PY) install

docs:
	$(SETUP_PY) build_sphinx

test:
	$(SETUP_PY) flake8
	$(SETUP_PY) pytest --addopts="tests --cov=aiomldht"


.PHONY: docs test install all