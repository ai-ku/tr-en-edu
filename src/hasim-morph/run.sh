#!/bin/bash

HASIM="/ai/home/ahan/opt/hasim-morph"
PARSER="/ai/home/ahan/opt/hasim-morph/MP-1.0-Linux64"
DISAMB="/ai/home/ahan/opt/hasim-morph/MD-2.0"

$PARSER/parse_corpus.py $PARSER/turkish.fst $1 > $1.mor.amb
$DISAMB/md.pl -disamb $DISAMB/model.txt $1.mor.amb $1.mor.disamb

sed -e 's/]+\[//g;s/]-\[//g;s/\[[^]]*\]//g' $1.mor.disamb > $1.tmp.1
java -cp $HASIM ParseHasimOutput $1.tmp.1 > $1.tmp.2
cat $1.tmp.2 | tr '\n' ' ' | sed 's#<S> ##g;s# <\/S> #\n#g' > $2
rm $1.amb $1.disamb $1.tmp.*