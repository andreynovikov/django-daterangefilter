.PHONY: test sdist wheel release pre-release clean

test:
	coverage run --source=daterangefilter runtests.py
	coverage report -m

build:
	python -m build

release: clean build wheel
	twine upload dist/*

pre-release: build wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
