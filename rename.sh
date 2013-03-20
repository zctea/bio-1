#!/bin/bash
for a in `ls -d */`;
do
  folder=${a:0:8}
  nn=$folder".csv"
  mv ./$folder/"rma_result.csv" ./$nn
done
  
