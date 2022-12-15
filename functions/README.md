### Functions

Two files containing [Tasks](https://docs.prefect.io/concepts/tasks/#tasks) are housed in this folder:

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

3. The function `snowflake_upload(*sql_querues)` from `snowflake_upload.py` is does the following:
	* Takes *args, consistening of SQL queries to execute in Snowflake
	* Spins up Snowflake connection
	* Executes the respective queries
	* Spins down Snowflake connection