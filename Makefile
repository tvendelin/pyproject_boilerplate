.ONESHELL:

PROJECT_VENV="v"
DOC_SOURCE_ROOT="src/mymodule"
PYTHON=${PROJECT_VENV}/bin/python

all: dist 

v:
	python3 -m venv v
	. ${PROJECT_VENV}/bin/activate;\
	${PYTHON} -m pip install -U pip

venv: v

bootstrap: venv
	. ${PROJECT_VENV}/bin/activate;\
	${PYTHON} -m pip install -e ".[dev]"

html: venv
	${PROJECT_VENV}/bin/activate;\
	${PYTHON} -m pip install -U pdoc3;\
	${PYTHON} -m pdoc --html --force ${DOC_SOURCE_ROOT}

test: tests.log

tests.log: bootstrap tests
	#${PYTHON} -m pip install ".[test]"
	. ${PROJECT_VENV}/bin/activate;\
	${PYTHON} -m unittest discover -s tests -b 2> tests.log

coverage: bootstrap
	coverage run -m unittest
	coverage html

dist: tests.log
	${PYTHON} -m pip install -U build
	${PYTHON} -m build

upload: build
	echo "To be done"

clean:
	rm -rf ${PROJECT_VENV}
	for F in "tests.log" html htmlcov build dist; do rm -r "$$F" || true; done
	find . -name '__pycache__' -exec rm -r '{}' \; || true
	find . -path '*.egg-info*' -exec rm -r '{}' \; || true