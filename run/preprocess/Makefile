CORES = 40

DATA = ../../data
SRC = ../../src

CLEAN = ${SRC}/moses/scripts/training/clean-corpus-n.perl
SPLIT-FILE = ${SRC}/split-file.py
HASIM-MORPH = ${SRC}/hasim-morph.sh
TREE-TAGGER = ${SRC}/tree-tagger.sh
LOWERCASE = java -cp ${SRC} Lowercase

UNIVS= $(shell for f in anadolu bilgi ieu itu koc marmara sabanci; do $f.alcmc.tr $f.alcmc.en; done)

all : ${UNIVS}

clean:
	rm -rf *.a.* *.al.* *.alc.* *.alcm.*

#make%:
#	for f in koc; do make $$f$*; done

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
