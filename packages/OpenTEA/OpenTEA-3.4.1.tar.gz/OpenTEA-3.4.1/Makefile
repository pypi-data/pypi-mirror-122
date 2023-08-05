init:
	pip install -r requirements.txt

test:
	PYTHONDONTWRITEBYTECODE=1 py.test tests --cov=opentea --cov-config=.coveragerc


lint:
	pylint src/opentea

wheel:
	rm -rf build
	rm -rf dist
	python setup.py sdist bdist_wheel

upload_test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload:
	twine upload dist/*

.PHONY: init test
