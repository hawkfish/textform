clean:
	rm -rf build dist

test:
	python3 -m unittest discover -s tests

dist:
	python3 -m build

.PHONY: test dist clean
