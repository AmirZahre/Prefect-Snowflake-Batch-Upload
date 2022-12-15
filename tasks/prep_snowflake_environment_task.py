from prefect import task, get_run_logger
from functions.prep_snowflake_environment_function import initiate_stage

@task
def set_snowflake_stage():
    logger = get_run_logger()
    initiate_stage()
    logger.info("✅ INFO successfully created upload (internal) stage")

