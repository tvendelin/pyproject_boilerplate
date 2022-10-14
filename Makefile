.ONESHELL:

PROJECT_VENV="v"
DOC_SOURCE_ROOT="src/mymodule"
PYTHON=${PROJECT_VENV}/bin/python

all: test coverage dist 

v:
	python3 -m venv v
	. ${PROJECT_VENV}/bin/activate;\
	${PYTHON} -m pip install -U pip

venv: v

bootstrap: venv
	. ${PROJECT_VENV}/bin/activate;\
	${PYTHON} -m pip install -e ".[dev]"

tidy: venv
	. ${PROJECT_VENV}/bin/activate;\
	echo "Running isort";\
	isort src;\
	echo "Running Black";\
	black src;\
	echo "Running Pylint";\
	pylint src

html: venv
	. ${PROJECT_VENV}/bin/activate;\
	${PYTHON} -m pip install -U pdoc3;\
	${PYTHON} -m pdoc --html --force ${DOC_SOURCE_ROOT}

test: tests.log

tests.log: bootstrap tests
	. ${PROJECT_VENV}/bin/activate;\
	${PYTHON} -m unittest discover -b 2> tests.log

coverage: bootstrap
	. ${PROJECT_VENV}/bin/activate;\
	coverage run -m unittest;\
	coverage html

dist: 
	python3 -m pip install -U build
	python3 -m build

upload: dist
	python3 -m twine upload --repository gitlab dist/*

clean:
	rm -rf ${PROJECT_VENV}
	for F in "tests.log" html htmlcov build dist; do rm -r "$$F" || true; done
	find . -name '__pycache__' -exec rm -r '{}' \; || true
	find . -path '*.egg-info*' -exec rm -r '{}' \; || true
