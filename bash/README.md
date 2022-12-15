### Bash Scripts

There are four Bash scripts used in this pipeline, which, in aggregate, transform the downloaded .zip file into partitioned .csv files each 100,000 rows in size.
1. `install_unzip.sh` installs the unzip command used to uncompress the downloaded .csv tables
2. `create_temp_folder.sh` creates the folders that will house the partitioned folders. These have to be created for each run as Azure Blob Storage, by default, deletes empty folders; therefore, these folders are deleted when this flow is deployed to Blob. Lack of persistent storage in AKS also disallows the creation of these folders for perpetual use there.
3. `move_unzip_rename.sh` moves the newly downloaded .zip file to its respective folder, unzips it to yield a .csv file, then renames it to [table].csv. This script utilizes **wildcard** variables to denote the table being worked on, and the wildcard variable is the table name which is fed to the script when it's invoked via the Python method `subprocess.call()`.
4. `prep_csv_file.sh`, the final script, transforms the .csv for Snowflake upload. 
	*	After navigating to the respective folder (also utilizing the aforementioned **wildcard** variables), the script removes the header of the .csv file. There are two methods invoked for this step, as MacOS and Ubuntu utilize a different approach. Although both are ran, one will always fail (wrong OS) and therefore skipped.
		*	`sed -i '' 1d $1.csv || true`  used for MacOS
		*	`sed -i '1d'  $1.csv || true`  used for Ubuntu (OS for the AKS image)
			*	`sed` [A stream-editor](https://archive.vn/cLlnm).
			*	`-i` This option specifies that files are to be edited in-place.
			*	`-1d` specifies the **d**eletion of the **1**st line - in this case, the header. This is the parameter that needs to be changed based on the OS, and will either be wrapped in single quotations or be prefixed by them.

