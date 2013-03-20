## R script for RMA processing of .CEL data

args <- commandArgs(TRUE);

## display & set working directory
getwd();
wk_dir <- args[1];
setwd(wk_dir);

## load affy package
library(affy);
library(Biobase);
data <- ReadAffy();
eset <- rma(data);

## save results to excel file
write.csv(eset,file="rma_result.csv");

