#!/bin/bash

../src/hunalign-1.1/src/hunalign/hunalign -text -bisent -realign -utf ../hunalign-1.1/data/en-tr.dic $1 $2 > $1-$2.aln
