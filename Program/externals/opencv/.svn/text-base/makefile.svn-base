
all: build test

build: BoWclassify.so BoWclassify posit.so

BoWclassify.so: bagofwords_classification_python.cpp
	g++ bagofwords_classification_python.cpp `pkg-config --libs --cflags opencv python` -lboost_python -o BoWclassify.so -shared -fPIC

BoWclassify: bagofwords_classification_python.cpp
	g++ bagofwords_classification_python.cpp `pkg-config --libs --cflags opencv python` -lboost_python -o BoWclassify

posit.so: posit_python.cpp
	g++ posit_python.cpp `pkg-config --libs --cflags opencv python` -lboost_python -o posit.so -shared -fPIC

test: build
	-./BoWclassify
	python -c "import BoWclassify; print BoWclassify.main(0, '', '', '', '', '', [])"
	python -c "import BoWclassify; print BoWclassify.main(0, '', '', '', '', '', [str(u'äbc'.encode('latin-1'))])"
	python -c "import posit; print posit.main([], [], ())"

clean:
	-rm BoWclassify.so BoWclassify posit.so

