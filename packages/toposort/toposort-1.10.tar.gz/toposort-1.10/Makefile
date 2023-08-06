all: wheel sdist

wheel:
	python3 -m build --wheel

sdist:
	python3 -m build --sdist

clean:
	rm -rf build/ dist/ src/*.egg-info src/__pycache__ test/__pycache__

test:	unittest doctest

unittest:
	PYTHONPATH=src:test python3 -m test.test_toposort

doctest:
	PYTHONPATH=src python3 -m doctest README.md

upload:
	twine upload dist/*

# I don't think my account is registered on the test server, but this
# is how it should work when that is fixed.
upload-test:
	twine upload --repository=testpypi --verbose dist/*
