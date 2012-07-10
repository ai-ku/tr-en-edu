CORES=8

sources = $(wildcard *.java)
classes = $(sources:.java=.class)


all: libs scripts

libs: 
	tar -xzf giza-pp-v1.0.7.tar.gz
	tar -xzf mgizapp-0.6.3.tar.gz
	cd tree-tagger; ./install-tagger.sh
	cd srilm; make World
	cd giza-pp; make
	cd mgizapp; ./configure --prefix=$(shell pwd)/mgizapp/bin; make; make install
	mkdir -p moses/giza
	cp giza-pp/GIZA++-v2/GIZA++ giza-pp/mkcls-v2/mkcls giza-pp/GIZA++-v2/plain2snt.out giza-pp/GIZA++-v2/snt2cooc.out giza-pp/GIZA++-v2/snt2plain.out moses/giza
	cp mgizapp/bin/bin/mgiza mgizapp/bin/scripts/merge_alignment.py moses/giza
	-cd moses; ./bjam -j${CORES} --with-giza=$(shell pwd)/moses/giza --with-srilm=$(shell pwd)/srilm

scripts: $(classes)

%.class: %.java
	javac -cp . $<
