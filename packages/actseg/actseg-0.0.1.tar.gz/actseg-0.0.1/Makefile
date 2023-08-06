init:
	pip install -e .[socks]
	pip install -r requirements-dev.txt

test:
	pytest

build:
	python setup.py bdist_wheel sdist

clean:
	rm -r build/
	rm -r dist/

