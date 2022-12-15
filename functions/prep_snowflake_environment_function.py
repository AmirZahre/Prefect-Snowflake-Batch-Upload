import subprocess
import os
from functions.snowflake_upload import snowflake_upload

def initiate_stage():

    """
    Base folder locations for the bash and sql queries
    """
    source = os.path.dirname(__file__)
    bash_folder = os.path.join(source, '../bash/')
    sql_folder = os.path.join(source, '../sql/')

    """
    Create the temp folders `temp/*` and install unzip.
    """
    subprocess.run(['bash', os.path.join(bash_folder, 'create_temp_folder.sh')])
    subprocess.run(['bash', os.path.join(bash_folder, 'install_unzip.sh')])

    """
    Create SQL queries
    """
    query_define_role = open(os.path.join(sql_folder, 'use_role_accountadmin.sql'), "r").read() # General query to specify user role
    create_temporary_internal_stage = open(os.path.join(sql_folder, 'stage_csv_upload.sql'), "r").read() # Create internal stage

    querues = [
        query_define_role,
        create_temporary_internal_stage
    ]

    """
    Spin up Snowflake connection and execute the aforementioned queries
    https://docs.snowflake.com/en/user-guide/python-connector-example.html
    """
    snowflake_upload(querues)