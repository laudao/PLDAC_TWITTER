#!/bin/bash
res=0
for f in */*.xml
do
nb=$(wc -l "$f" | cut  -d" " -f1)
nb=$(($nb-2))
nb=$(($nb/5))
res=$(($nb+$res))
done
echo $res

