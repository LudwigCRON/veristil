
export TEST_DIR=$(shell pwd)/tests

.PHONY: tests

update_module:
	python3 -m pip install .

tests: update_module
	python3 -m unittest discover ./tests

test_%: update_module
	python3 -m unittest discover -s ./tests -k $@