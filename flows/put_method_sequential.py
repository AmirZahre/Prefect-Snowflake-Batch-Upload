from prefect.task_runners import SequentialTaskRunner
from prefect import flow
from tasks.update_sharadar_db_parallel_task import local_to_snowflake_actions_task, local_to_snowflake_daily_task, local_to_snowflake_sep_task, local_to_snowflake_sf1_task, local_to_snowflake_sfp_task
from tasks.prep_snowflake_environment_task import set_snowflake_stage


"""
TO DEPLOY TO DEV:
prefect deployment build flows/put_method_sequential.py:file_to_snowflake_stage -t snowflake -t dev -n dev -q staging -sb azure/dev-storage  -ib kubernetes-job/aks-job --apply
"""
@flow(name="sharadar_upload_flow",
    description="This flow runs populates the QUANDL_DB tables",
    task_runner=SequentialTaskRunner()
    )
def file_to_snowflake_stage():

    # Invokes the task that runs the function prep_snowflake_environment_function.py
    set_snowflake_stage.submit()

    # Runs each task in update_sharadar_db_parallel_task.py sequentially
    local_to_snowflake_actions_task.submit()
    local_to_snowflake_daily_task.submit()
    local_to_snowflake_sep_task.submit()
    local_to_snowflake_sf1_task.submit()
    local_to_snowflake_sfp_task.submit()

if __name__ == "__main__":
    file_to_snowflake_stage()