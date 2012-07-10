SHELL=/bin/bash

DATA = ../../data
SRC = ../../src

CLEAN = ${SRC}/moses/scripts/training/clean-corpus-n.perl
SPLIT-FILE = ${SRC}/split-file.py
HASIM-MORPH = ${SRC}/hasim-morph.sh
TREE-TAGGER = ${SRC}/tree-tagger.sh
LOWERCASE = java -cp ${SRC} Lowercase
SPLIT = ${SRC}/split.pl

UNIVS = $(shell echo {anadolu,bilgi,ieu,itu,koc,marmara,sabanci}.alcmc.{tr,en})
OTHERS = $(shell echo {os11,setimes,yok-utm}.alcmc.{tr,en})

all : ${UNIVS} ${OTHERS}
	mv os11.alcmc.tr os11.tr
	mv os11.alcmc.en os11.en
	mv setimes.alcmc.tr setimes.tr
	mv setimes.alcmc.en setimes.en
	mv yok-utm.alcmc.tr yok-utm.tr
	mv yok-utm.alcmc.en yok-utm.en
	cp ${SPLIT} .; chmod +x split.pl; ./split.pl
	mv trn.tr univ.tr
	mv trn.en univ.en

clean:
	rm -rf *.a.* *.al.* *.alc.* *.alcm.* split.pl

%.alcmc.tr %.alcmc.en: %.alcm.tr %.alcm.en
	${CLEAN} $*.alcm tr en $*.alcmc 1 80

%.alcm.tr: %.alc.tr
	${SPLIT-FILE} $< ${CORES}
	echo $<.* | xargs -n 1 -P ${CORES} ${HASIM-MORPH}
	cat `ls $<.*.mor` > $@
	rm $<.*

%.alcm.en: %.alc.en
	${SPLIT-FILE} $< ${CORES}
	echo $<.* | xargs -n 1 -P ${CORES} ${TREE-TAGGER}
	cat `ls $<.*.mor` > $@
	rm $<.*

%.alc.tr %.alc.en: %.al.tr %.al.en
	${CLEAN} $*.al tr en $*.alc 1 80

%.al.tr %.al.en: %.a.tr %.a.en
	${LOWERCASE} tr < $*.a.tr > $*.al.tr
	${LOWERCASE} en < $*.a.en > $*.al.en

%.a.tr %.a.en: ${DATA}/%.tr.gz ${DATA}/%.en.gz
	zcat ${DATA}/$*.tr.gz > $*.a.tr
	zcat ${DATA}/$*.en.gz > $*.a.en
