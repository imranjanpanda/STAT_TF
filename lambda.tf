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
  timeout          = "900"
  memory_size      = "128"
  environment {
    variables = {
      TABLE_NAME = "Shortlisted_Stocks"
    }
  }
}

data "archive_file" "create_shortlisted_stocks" {
  type        = "zip"
  source_dir  = "${path.module}/Lambda/create-shortlisted-stocks/"
  output_path = "${path.module}/Lambda/create-shortlisted-stocks.zip"
}

resource "aws_lambda_function" "create_shortlisted_stocks" {
  filename         = data.archive_file.create_shortlisted_stocks.output_path
  function_name    = "create_shortlisted_stocks"
  role             = "arn:aws:iam::118078187306:role/service-role/Dynamodb_lambda"
  handler          = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.create_shortlisted_stocks.output_base64sha256
  runtime          = "python3.12"
  timeout          = "900"
  memory_size      = "128"
  environment {
    variables = {
      TABLE_NAME = "Shortlisted_Stocks"
    }
  }
}

data "archive_file" "update_shortlisted_stocks" {
  type        = "zip"
  source_dir  = "${path.module}/Lambda/update-shortlisted-stocks/"
  output_path = "${path.module}/Lambda/update-shortlisted-stocks.zip"
}

resource "aws_lambda_function" "update_shortlisted_stocks" {
  filename         = data.archive_file.update_shortlisted_stocks.output_path
  function_name    = "update_shortlisted_stocks"
  role             = "arn:aws:iam::118078187306:role/service-role/Dynamodb_lambda"
  handler          = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.update_shortlisted_stocks.output_base64sha256
  runtime          = "python3.12"
  timeout          = "900"
  memory_size      = "128"
  
  environment {
    variables = {
      TABLE_NAME = "Shortlisted_Stocks"
    }
  }
}

data "archive_file" "delete_shortlisted_stocks" {
  type        = "zip"
  source_dir  = "${path.module}/Lambda/delete-shortlisted-stocks/"
  output_path = "${path.module}/Lambda/delete-shortlisted-stocks.zip"
}

resource "aws_lambda_function" "delete_shortlisted_stocks" {
  filename         = data.archive_file.delete_shortlisted_stocks.output_path
  function_name    = "delete_shortlisted_stocks"
  role             = "arn:aws:iam::118078187306:role/service-role/Dynamodb_lambda"
  handler          = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.delete_shortlisted_stocks.output_base64sha256
  runtime          = "python3.12"
  timeout          = "900"
  memory_size      = "128"
  environment {
    variables = {
      TABLE_NAME = "Shortlisted_Stocks"
    }
  }
}

data "archive_file" "lambda_authorizer" {
  type        = "zip"
  source_dir  = "${path.module}/Lambda/lambda-authorizer/"
  output_path = "${path.module}/Lambda/lambda-authorizer.zip"
}

resource "aws_lambda_function" "lambda_authorizer" {
  filename         = data.archive_file.lambda_authorizer.output_path
  function_name    = "STAT_lambda_authorizer"
  role             = "arn:aws:iam::118078187306:role/service-role/Dynamodb_lambda"
  handler          = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.lambda_authorizer.output_base64sha256
  runtime          = "python3.12"
  timeout          = "900"
  memory_size      = "128"
  layers           = ["arn:aws:lambda:ap-south-1:118078187306:layer:pyjwt:1"]
}

data "archive_file" "user_authorization" {
  type        = "zip"
  source_dir  = "${path.module}/Lambda/user_authorization/"
  output_path = "${path.module}/Lambda/user_authorization.zip"
}

resource "aws_lambda_function" "user_authorization" {
  filename         = data.archive_file.user_authorization.output_path
  function_name    = "STAT_user_authorization"
  role             = "arn:aws:iam::118078187306:role/service-role/Dynamodb_lambda"
  handler          = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.user_authorization.output_base64sha256
  runtime          = "python3.12"
  timeout          = "900"
  memory_size      = "128"
  layers           = [
    "arn:aws:lambda:ap-south-1:118078187306:layer:pyjwt:1",
    "arn:aws:lambda:ap-south-1:118078187306:layer:bcrypt:1"
  ]
}