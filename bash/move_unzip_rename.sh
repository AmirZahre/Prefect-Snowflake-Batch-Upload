# # STEP 3: Move .zip file to proper folder, unzip and rename .csv to <table>.csv using wildcard variables.
# This script utilizes wildcard inputs to move the newly downloaded .zip file for upload.
# The wildcard value '$1' is the table name, which is fed to the script when it's invoked via the Python method subprocess.call().

#### Uncomment echo lines for troubleshooting.

# Move downloaded file to new directory
# echo mv 'SHARADAR_$1.zip' 'temp/$1/'
mv SHARADAR_$1.zip temp/$1/

# Navigate to table directory
# echo cd 'temp/$1/'
cd temp/$1/

# Unzip all .zip files
# echo unzip *.zip
unzip *.zip

# Remove zip file (no longer needed)
# echo rm *.zip
rm *.zip

# Rename unzipped .csv file
# echo mv *.csv $1.csv
mv *.csv $1.csv