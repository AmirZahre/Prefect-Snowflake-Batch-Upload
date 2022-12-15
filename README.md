The Prefect Flow contained within this folder is used to download five tables from SHARADAR, prime them for upload to Snowflake, and subsequently upload them to Snowflake. The five tables in question are: actions, daily, sep, sf1, sfp.

## The Flow:

![image](https://user-images.githubusercontent.com/71795488/207937816-ce738480-14c4-4d6c-92ba-6688259a4b1f.png)

This Flow folder contains the following folders:

*  `/flows`: Includes a single file, `put_method_sequential.py`, that contains the [flow](https://docs.prefect.io/concepts/flows/) for this pipeline. A flow is a container for workflow logic and allows users to interact with and reason about the state of their workflows. The flow, which makes calls to tasks located within `/tasks`. The Flow utilizes DaskTaskRunner to run the tasks in parallel.


*  `/tasks`: Contains basic Python functions decorated with the `task` operator. These [tasks](https://docs.prefect.io/concepts/tasks/) are used to add additional logging for when the flow is running, and modularize the flow's operations. They reference functions located with `/functions`.


*  `/functions`: Contain the Python functions used within the pipeline.

   1. The function `initiate_stage()` from`prep_snowflake_environment_function.py` is invoked by the Prefect Task `prep_snowflake_environment_task.py`. This function is used to initialize the flow and Snowflake environments, and does several things:
	  * Invokes `subprocess.call()` to create the temp folder system, which contains child folders for each table. This utilizes the `create_temp_folder.sh` script.
	  * Invokes `subprocess.call()` again to install unzip by using the `install_unzip.sh` script.
	  * Spins up a Snowflake connection and runs the following queries:
		  * `use_role_accountadmin.sql`, which contains `USE ROLE ACCOUNTADMIN` used to specify the account type for the next operation; and,
		  * `stage_csv_upload.sql`, which contains the query used to define a new (overwrite) internal stage for file upload.
  
    2. The function `put_method(table: str)` from `update_sharadar_db_function_parallel.py` is invoked by the Prefect Task `update_sharadar_db_parallel_task.py`. This function does the following:
	    * Downloads the table in the form of a .zip file by invoking the method `nasdaqdatalink.export_table(f'{sharadar}')`, with **sharadar** equating to the table name.
	    * Runs several bash scripts to move, unzip, and split the table into smaller (100k row) partitions.
	    * Invokes the `snowflake_upload(*sql_querues)` function, passing queries respective of the current table (.csv).
    
    3. The function `snowflake_upload(*sql_querues)` from `snowflake_upload.py` does the following:
	    * Takes *args, consistening of SQL queries to execute in Snowflake
	    * Spins up Snowflake connection
	    * Executes the respective queries
	    * Spins down Snowflake connection


* `/bash` which houses the bash scripts used within the flow.
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


* `/sql` which houses the SQL scripts used within the flow.
  The SQL scripts in this flow can be broken down into two categories: those used for specific tables, and those for general Snowflake environment initialization:
  
  #### General Snowflake Environment Initialization
  Two scripts fall into this category:
  
   1. `use_role_accountadmin.sql` specifies the account to use when spinning up a Snowflake connection via. `conn.cursor()`. We want to be using **ACCOUNTADMIN** in order to manipulate stages and truncate tables.
   2. `stage_csv_upload.sql` creates, or replaces, the internal stage **csv_upload**. This stage is used when putting local, partitioned .csv files into Snowflake (via PUT). The stage is primed to accept .csv files, without a header, converting datetime values to the format 'YYYY-MM-DD'.
  
  #### Table-Specific Queries
  There are five subfolders, aptly named **table_1** through **table_5** to anonymize the table names for public viewing, that each contain three identical queries which only differ by table name. The queries are as follow:
  
   1. `put_local_to_internal_stage.sql` executes a PUT query that uploads the partitioned .csv files from **temp/TABLE/** to the aforementioned internal stage **csv_upload/TABLE**. The tables are picked up locally by utilizing **wildcard** characters, as each are suffixed by an integer, which enables uploading multiple files in a directory. The PUT query also utilizes 16 cores (x-small warehouse for this operation), auto compresses the files to csv.gz, and overwrites any potential existing copies in the staging area. The latter parameter is a redundancy, as the stage should be created anew as per the `stage_csv_upload.sql` operation.
   2. `truncate_table.sql` truncates the respective table prior to copying over from internal stage.
   3. `copy_into_table_from_stage.sql` copies the content from the internal stage **csv_upload/TABLE** to the respective table, **TABLE**.


* `/temp` which will **eventually** house the tables once downloaded. This folder, when the flow is deployed to Azure Blob Storage, is automatically omitted (as Blob doesn't like empty folders by default) - therefore, `/temp` and all its sub-directories are recreated from within a bash script.


More information about the content of these folders may be found from within their respective `README.md`'s.

**To temporarily export the folder system paths:**

`export PYTHONPATH=$PYTHONPATH:$(pwd)/functions:$(pwd)/tasks`


## **To deploy the flow:**

  The Flow may be deployed into three separate environments. From within the terminal, navigate to the top-level folder and enter one of the following:

**Development**:

`prefect deployment build flows/put_method_sequential.py:file_to_snowflake_stage -n dev -t snowflake -t dev  -q staging -sb azure/dev-storage -ib kubernetes-job/aks-job --apply`

**Staging**:

`prefect deployment build flows/put_method_sequential.py:file_to_snowflake_stage -n staging -t snowflake -t staging -q staging -sb azure/staging-sharadar-db-upload-storage -ib kubernetes-job/aks-job --apply`

**Production**:

`prefect deployment build flows/put_method_sequential.py:file_to_snowflake_stage -n production -t snowflake -t production -q production -sb azure/production-sharadar-db-upload-storage -ib kubernetes-job/aks-job --apply`

**Deployment Definitions**:

*  `-t` is for tags. For this deployment, the tags used are:
	* `snowflake` to signify it's related to Snowflake
	* `dev`/`staging`/

*  `-n` deployment name (`dev`, `staging`, `production`)

*  `-q` work queue
   *   For Development and Staging deployments, use `-q staging` 
   *   For Production, use `-q production`

*  `-sb` storage block where the flow is held (we use Azure Blob)
   *  Development storage block: `azure/dev-storage`
   *  Staging: `azure/staging-sharadar-db-upload-storage`
   *  Production: `azure/production-sharadar-db-upload-storage`

*  `-ib` the location of the Agent (we use AKS)
   *  Regardless of deployment type, this value will be `kubernetes-job/aks-job`.
   *  AKS has two containers, one primed to pick up Dev/Staging deployments with the work queue `-q staging`, and one Production with `-q production`

* `-rrule (depreciated for this flow in favour of CRON)` specifies the frequency of the flow run (usually weekly, ex. --rrule 'FREQ=WEEKLY;BYDAY=SU;BYHOUR=9'). This has been depreciated in favour of CRON, which is set in the Prefect UI.

*  `--apply` pushes this deployment to the cloud.

  ## **Potential Warnings (Ignore):**

* You may receive the following warning when deploying. This can be safely ignored, and is a minor bug recognized by Prefect:

> /Users/**[USER]**/.pyenv/versions/3.9.12/lib/python3.9/site-packages/prefect/blocks/core.py:649: UserWarning: Block document has schema checksum sha256:**[HASH]** which does not match the schema checksum for class 'Azure'. This indicates the schema has changed and this block may not load.
