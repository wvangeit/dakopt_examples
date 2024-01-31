SHELL := /bin/bash

test: clean
	source ./venv/bin/activate && \
		python main.py
testenv:
	rm -rf venv
	python -m venv venv
	source ./venv/bin/activate && \
		pip install -r requirements.txt
clean:
	rm -rf *.out *.log *.rst *.dat fort.*
