#/bin/bash
#
# calculate the Person Correlation Coefficient by call several scripts
#
#


echo -e "Calculate the PCC of a dataset by calling serveral python scripts"

filebasename=$1

echo $filebasename

echo "Transpose the data"
org_file=$filebasename".csv"
python /cewit/home/shhan/scripts/python/correlation/GeoFile.py -f $org_file -t

echo "dump the data matrix"
t_file=$filebasename".t"
python /cewit/home/shhan/scripts/python/correlation/GeoFile.py -f $t_file -d

echo "cacluate PCC..."
mat_file=$filebasename".mat"
python /cewit/home/shhan/scripts/python/correlation/dataProc.py -f $mat_file -p

echo "done!"

exit 0
