### SQL Scripts

The SQL scripts in this flow can be broken down into two categories: those used for specific tables, and those for general Snowflake environment initialization.

#### General Snowflake Environment Initialization
Two scripts fall into this category:

 1. `use_role_accountadmin.sql` specifies the account to use when spinning up a Snowflake connection via. `conn.cursor()`. We want to be using **ACCOUNTADMIN** in order to manipulate stages and truncate tables.
 2. `stage_csv_upload.sql` creates, or replaces, the internal stage **csv_upload**. This stage is used when putting local, partitioned .csv files into Snowflake (via PUT). The stage is primed to accept .csv files, without a header, converting datetime values to the format 'YYYY-MM-DD'.

#### Table-Specific Queries
There are five subfolders, aptly named **table_1** through **table_5** to anonymize the table names for public viewing, that each contain three identical queries which only differ by table name. The queries are as follow:

 1. `put_local_to_internal_stage.sql` executes a PUT query that uploads the partitioned .csv files from **temp/TABLE/** to the aforementioned internal stage **csv_upload/TABLE**. The tables are picked up locally by utilizing **wildcard** characters, as each are suffixed by an integer, which enables uploading multiple files in a directory. The PUT query also utilizes 16 cores (x-small warehouse for this operation), auto compresses the files to csv.gz, and overwrites any potential existing copies in the staging area. The latter parameter is a redundancy, as the stage should be created anew as per the `stage_csv_upload.sql` operation.
 2. `truncate_table.sql` truncates the respective table prior to copying over from internal stage.
 3. `copy_into_table_from_stage.sql` copies the content from the internal stage **csv_upload/TABLE** to the respective table, **TABLE**.