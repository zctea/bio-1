#!/bin/bash
for a in `ls -1 *.tar`; 
do 
  folder=${a:0:8}
  Rscript cel_rma.R ./$folder
  #mkdir $folder
  #tar -xf $a -C ./$folder
done
