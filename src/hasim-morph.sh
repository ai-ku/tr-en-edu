#!/bin/bash

DIR="$( dirname "$0" )"

PARSER="$DIR/hasim-morph/MP-1.0-Linux64"
DISAMB="$DIR/hasim-morph/MD-2.0"

$PARSER/parse_corpus.py $PARSER/turkish.fst $1 > $1.mor.amb
$DISAMB/md.pl -disamb $DISAMB/model.txt $1.mor.amb $1.mor.disamb

sed -e 's/]+\[//g;s/]-\[//g;s/\[[^]]*\]//g' $1.mor.disamb > $1.tmp.1
java -cp $DIR ParseHasimOutput $1.tmp.1 > $1.tmp.2
cat $1.tmp.2 | tr '\n' ' ' | sed 's#<S> ##g;s# <\/S> #\n#g' > $1.mor
rm $1.amb $1.disamb $1.tmp.*