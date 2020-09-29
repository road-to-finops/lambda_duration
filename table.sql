CREATE EXTERNAL TABLE `lambda_usage`(
  `fucntionname` string COMMENT 'from deserializer', 
  `fucntionarn` string COMMENT 'from deserializer', 
  `minimum` string COMMENT 'from deserializer', 
  `average` string COMMENT 'from deserializer', 
  `maximum` string COMMENT 'from deserializer', 
  `memorysize` int COMMENT 'from deserializer', 
  `log` string COMMENT 'from deserializer', 
  `REPORT RequestId` string COMMENT 'from deserializer', 
  `Duration` string COMMENT 'from deserializer',
  `Billed Duration` string COMMENT 'from deserializer',
  `Memory Size` string COMMENT 'from deserializer',
  `Max Memory Used` string COMMENT 'from deserializer',
  `Init Duration` string COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat'
LOCATION
  's3://<bucket_name>/lambda'
TBLPROPERTIES (
  'has_encrypted_data'='false', 
  'transient_lastDdlTime'='1601376960')
