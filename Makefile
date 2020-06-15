clean:
	rm -rf build

build: clean
	python setup.py build_ext --inplace

install:
	python setup.py install
