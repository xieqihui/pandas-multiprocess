.PHONY: clean-build clean-pyc

TEST_PATH=./tests

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	name '*~' -exec rm --force  {} 

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

build: clean-build
	python setup.py bdist_wheel

test: clean-pyc
	pytest --verbose --color=yes $(TEST_PATH)
