# # STEP 4: Prep the .csv file for upload
# This script first removes the header of the .csv file, an approach that differes based on operating system.
# For local machine (MacOS M1), the first 'sed' line removes the header of the file. For AKS (Ubuntu 18.04), the second 'sed' line is used.
# The file is then split to partitions of 100k rows in size each, with no headers for any of the partitions.
# The split files are then converted to .csv's.

#### Uncomment echo lines for troubleshooting.

# Navigate to /temp folder
# echo cd temp/$1/
cd temp/$1/

# Remove Header. Each line is ran, one will work depending on os
# echo sed -i '' 1d $1.csv
sed -i '' 1d $1.csv || true # works on local
sed -i '1d' $1.csv || true # works on AKS

# # Split file into partitions of 100000 rows each
# echo split -l 100000 -d -a 5 $1.csv file_
split -l 100000 -d -a 5 $1.csv file_

# # Change type of generated files to .csv
# echo "Change type of generated files to .csv"
for i in $(find file_*); 
do 
    mv $i "$i.csv"; 
done