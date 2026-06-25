output "data_lake_bucket_name" {
  value = aws_s3_bucket.data_lake.bucket
}

output "transactions_table_name" {
  value = aws_dynamodb_table.transactions.name
}
