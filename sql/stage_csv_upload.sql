create or replace stage csv_upload
  file_format = (type = 'CSV' field_delimiter = ',' skip_header = 0 TIMESTAMP_FORMAT = 'YYYY-MM-DD');