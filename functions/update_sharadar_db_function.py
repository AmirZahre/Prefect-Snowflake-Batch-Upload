import subprocess
from prefect.blocks.system import Secret
import nasdaqdatalink
import os
from functions.snowflake_upload import snowflake_upload


def put_method(table: str):
    """
    Create string for API call
    """
    sharadar = f"SHARADAR/{table.upper()}"

    """
    Base folder locations for the bash and sql queries
    """
    source = os.path.dirname(__file__)
    bash_folder = os.path.join(source, '../bash/')
    sql_folder = os.path.join(source, '../sql/')

    """
    Access Prefect Secret Blocks for Snowflake and Nasdaq credentials
    """
    nasdaq_secret = Secret.load("nasdaq-secret")
    nasdaqdatalink.ApiConfig.api_key = nasdaq_secret.get()
    
    """
    Download the table from source (as .zip)
    """
    nasdaqdatalink.export_table(f'{sharadar}') # download table

    """
    Prep the .zip file for upload
    """
    subprocess.run(['bash', os.path.join(bash_folder, 'move_unzip_rename.sh'), table.upper()]) # Extract and rename the .ZIP file from SHARADAR
    subprocess.run(['bash', os.path.join(bash_folder, 'prep_csv_file.sh'), table.upper()]) # Prep the (now) .csv file for Snowflake upload

    """
    Execute SQL queries
    """
    query_define_role = open(os.path.join(sql_folder, 'use_role_accountadmin.sql'), "r").read() # General query to specify user role
    query_truncate_table = open(os.path.join(sql_folder, table, 'truncate_table.sql'), "r").read() # Truncate table
    query_put_actions_file_to_internal_stage = open(os.path.join(sql_folder, table, 'put_local_to_internal_stage.sql'), "r").read() # Stage to Table
    query_copy_into_actions_table = open(os.path.join(sql_folder, table, 'copy_into_table_from_stage.sql'), "r").read() # Local to Stage

    querues = [
        query_define_role,
        query_truncate_table,
        query_put_actions_file_to_internal_stage,
        query_copy_into_actions_table
    ]

    """
    Spin up Snowflake connection and execute the aforementioned queries
    https://docs.snowflake.com/en/user-guide/python-connector-example.html
    """
    snowflake_upload(querues)