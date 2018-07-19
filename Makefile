.PHONY: clean-build clean-pyc build

TEST_PATH=./tests

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force {} +

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

build: clean-build
	python setup.py bdist_wheel

publish: build
	twine upload dist/*

test: clean-pyc
	pytest --verbose --color=yes $(TEST_PATH)

install: build
	pip uninstall --yes pandas-multiprocess & pip install dist/pandas_multiprocess*.whl
