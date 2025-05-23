import os
import time

from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

table_name = f"sdk-{time.time_ns()}"

created_catalog = w.catalogs.create(name=f"sdk-{time.time_ns()}")

created_schema = w.schemas.create(name=f"sdk-{time.time_ns()}", catalog_name=created_catalog.name)

_ = w.statement_execution.execute(
    warehouse_id=os.environ["TEST_DEFAULT_WAREHOUSE_ID"],
    catalog=created_catalog.name,
    schema=created_schema.name,
    statement="CREATE TABLE %s AS SELECT 2+2 as four" % (table_name),
).result()

# cleanup
w.schemas.delete(full_name=created_schema.full_name)
w.catalogs.delete(name=created_catalog.name, force=True)
