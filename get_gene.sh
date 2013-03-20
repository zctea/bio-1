#!/bin/bash
#

for f in `ls *.csv`;
do
  python ~/scripts/python/correlation/GeoFile.py -f $f -n gene_list
done
