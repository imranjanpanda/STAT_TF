data "archive_file" "get_shortlisted_stocks" {
  type        = "zip"
  source_dir  = "${path.module}/Lambda/get-shortlisted-stocks/"
  output_path = "${path.module}/Lambda/get-shortlisted-stocks.zip"
}
resource "aws_lambda_function" "get_shortlisted_stocks" {
  filename         = data.archive_file.get_shortlisted_stocks.output_path
  function_name    = "get_shortlisted_stocks"
  role             = "arn:aws:iam::118078187306:role/service-role/Dynamodb_lambda"
  handler          = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.get_shortlisted_stocks.output_base64sha256
  runtime          = "python3.12"
  timeout = "15"
  memory_size = "128"
  environment {
    variables = {
      TABLE_NAME = "Shortlisted_Stocks"
    }
  }
}