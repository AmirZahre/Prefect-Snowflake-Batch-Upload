### Prefect Flow

The flow `put_method_sequential.py` invokes six tasks to run an ETL pipeline that downloads, transforms, and uploads five tables exceeding an aggregate of 100m rows in size to Snowflake.

This pipeline utilizes Snowflakes [PUT](https://docs.snowflake.com/en/sql-reference/sql/put.html) command and Prefect's [SequentialTaskRunner](https://docs.prefect.io/api-ref/prefect/task-runners/#prefect.task_runners.SequentialTaskRunner) to run the pipline in ~20 minutes. It utilizes AKS as the Prefect Agent engine, and Azure Blob Storage as the cloud storage location for the flow files.

To redeploy the pipeline following any updates, please run:

    prefect deployment build flows/put_method_sequential.py:file_to_snowflake_stage -t snowflake -t dev -n dev -q staging -sb azure/dev-storage -ib kubernetes-job/aks-job --apply
    
Where 
*  `-t` is for tags

*  `-n` is the deployment name

*  `-q` specifies the work queue (staging or production) picked up by AKS

*  `-sb` defines the storage block where the flow is held (Azure Blob Storage, in this case)

*  `-ib` is the location of the Agent (AKS)

*  `-rrule (depreciated for this flow)` specifies the frequency of the flow run (usually weekly, ex. --rrule 'FREQ=WEEKLY;BYDAY=SU;BYHOUR=9'). This has been depreciated in favour of CRON, which is set in the Prefect UI.

*  `--apply` pushes this deployment to the cloud