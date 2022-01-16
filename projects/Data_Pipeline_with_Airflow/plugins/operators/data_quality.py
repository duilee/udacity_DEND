from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class DataQualityOperator(BaseOperator):
    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 conn_id,
                 dq_checks=[]
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.conn_id = redshift_conn_id
        self.dq_checks = dq_checks

    def execute(self, context):
        redshift_hook = PostgresHook(self.conn_id)

        for item in self.dq_checks:
            table = item.get('table', None)
            min_count = item.get('min', None)
            max_count = item.get('max', None)

            if table is None:
                continue

            records = redshift_hook.get_records(f"SELECT COUNT(*) FROM {table}")
            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(f"Data quality check failed. {table} returned no results")
            row_count = records[0][0]
            if min_count is not None and row_count < min_count:
                raise ValueError(f"Data quality check failed. {table} contained {row_count} rows, less than expected min {min_count}")
            if max_count is not None and row_count > max_count:
                raise ValueError(f"Data quality check failed. {table} contained {row_count} rows, more than expected max {max_count}")
            self.log.info(f"Data quality on table {table} check passed with {records[0][0]} records")