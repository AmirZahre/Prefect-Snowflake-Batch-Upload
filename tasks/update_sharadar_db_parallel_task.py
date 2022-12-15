from prefect import task, get_run_logger
from functions.update_sharadar_db_function import put_method

@task
def local_to_snowflake_actions_task():
    logger = get_run_logger()
    put_method('actions')
    logger.info("✅ INFO successfully updated ACTIONS data")

@task
def local_to_snowflake_daily_task():
    logger = get_run_logger()
    put_method('daily')
    logger.info("✅ INFO successfully updated DAILY data")

@task
def local_to_snowflake_sep_task():
    logger = get_run_logger()
    put_method('sep')
    logger.info("✅ INFO successfully updated SEP data")

@task
def local_to_snowflake_sf1_task():
    logger = get_run_logger()
    put_method('sf1')
    logger.info("✅ INFO successfully updated SF1 data")

@task
def local_to_snowflake_sfp_task():
    logger = get_run_logger()
    put_method('sfp')
    logger.info("✅ INFO successfully updated SFP data")