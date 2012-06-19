#!/bin/bash

echo source directory: $1
echo target directory: $2

for f in `ls $1`
do
    echo $f
    gzip < $1/$f > $2/$f.gz
done

# int_path=$1
# echo "directory:"$int_path
# for f in {`ls $1`}
# do
#     echo $f
#     if [ -f $f ]
#     then
# 	echo $f;
# #	gzip $f
#     fi
# done