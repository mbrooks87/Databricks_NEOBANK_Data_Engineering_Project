-- %sql
select * from banking.metadata.tables

select * from banking.metadata.table_parameters

select * from banking.metadata.pipeline_runs order by start_time desc

select * from banking.metadata.table_parameters where table_id = 4

select t.table_name, table_parameters.parameter_value from banking.metadata.tables t join banking.metadata.table_parameters where t.table_id = table_parameters.table_id and table_parameters.parameter_name='load_type'

select * from banking.metadata.table_watermarks
