from prefect_snowflake.database import SnowflakeConnector
from snowflake.connector import connect
from prefect.blocks.system import Secret


def snowflake_upload(*sql_querues):
    snowflake_secret = Secret.load("snowflake-secret")
    snowflake_connector_block = SnowflakeConnector.load("quandl-core-us-equities-db")

    conn = connect(
        user=snowflake_connector_block.credentials.user,
        password=snowflake_secret.get(),
        account=snowflake_connector_block.credentials.account,
        warehouse=snowflake_connector_block.warehouse,
        database=snowflake_connector_block.database,
        schema=snowflake_connector_block.schema_,
        )
    cursor = conn.cursor()

    for query in sql_querues[0]:
        cursor.execute(query)

    cursor.close()