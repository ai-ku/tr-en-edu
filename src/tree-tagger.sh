#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"
cd $DIR

TT="../lib/tree-tagger"

sed 's#^#<S> #g;s#$# <\/S>#g;s# #\n#g' $1 > $1.tmp.1
$TT/bin/tree-tagger -token -lemma -sgml -no-unknown $TT/lib/english.par $1.tmp.1 $1.tmp.2
java -cp . ParseTreeTaggerOutput $1.tmp.2 > $1.tmp.3
cat $1.tmp.3 | tr '\n' ' ' | sed 's#<S> ##g;s# <\/S> #\n#g' > $1.mor
rm $1.tmp.*