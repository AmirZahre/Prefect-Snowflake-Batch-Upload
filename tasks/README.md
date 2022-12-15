### Prefect Tasks

Two files containing [Tasks](https://docs.prefect.io/concepts/tasks/#tasks) are housed in this folder:
1. `prep_snowflake_environment_task.py`, which contains a single task that runs the function `initiate_stage()` from`prep_snowflake_environment_function.py` and adds logging in the terminal; and,
2. `update_sharadar_db_parallel_task.py`, which is home to five tasks that each invoke the function `put_method(table: str)` from within `update_sharadar_db_function_parallel.py`, with differing paramaters for `table`, while also adding logging to the terminal.