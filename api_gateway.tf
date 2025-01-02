# Create API Gateway REST API
resource "aws_api_gateway_rest_api" "STAT_API" {
  name        = "STAT_API"
  description = "API for STAT"
}

# Create API Gateway Resource
resource "aws_api_gateway_resource" "stocks_resource" {
  rest_api_id = aws_api_gateway_rest_api.STAT_API.id
  parent_id   = aws_api_gateway_rest_api.STAT_API.root_resource_id
  path_part   = "shortlisted_stocks" # Endpoint: /shortlisted_stocks
}

# Enable CORS
resource "aws_api_gateway_method" "cors_options" {
  rest_api_id   = aws_api_gateway_rest_api.STAT_API.id
  resource_id   = aws_api_gateway_resource.stocks_resource.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "cors_integration" {
  rest_api_id = aws_api_gateway_rest_api.STAT_API.id
  resource_id = aws_api_gateway_resource.stocks_resource.id
  http_method = aws_api_gateway_method.cors_options.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "cors_response" {
  rest_api_id = aws_api_gateway_rest_api.STAT_API.id
  resource_id = aws_api_gateway_resource.stocks_resource.id
  http_method = aws_api_gateway_method.cors_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

# Lambda Integration for GET /stocks
resource "aws_api_gateway_method" "get_stocks" {
  rest_api_id   = aws_api_gateway_rest_api.STAT_API.id
  resource_id   = aws_api_gateway_resource.stocks_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_get_integration" {
  rest_api_id             = aws_api_gateway_rest_api.STAT_API.id
  resource_id             = aws_api_gateway_resource.stocks_resource.id
  http_method             = aws_api_gateway_method.get_stocks.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.get_shortlisted_stocks.invoke_arn
}

# Lambda Integration for POST /shortlisted_stocks
resource "aws_api_gateway_method" "post_stocks" {
  rest_api_id   = aws_api_gateway_rest_api.STAT_API.id
  resource_id   = aws_api_gateway_resource.stocks_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_post_integration" {
  rest_api_id             = aws_api_gateway_rest_api.STAT_API.id
  resource_id             = aws_api_gateway_resource.stocks_resource.id
  http_method             = aws_api_gateway_method.post_stocks.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.create_shortlisted_stocks.invoke_arn
}

# Lambda Integration for PUT /shortlisted_stocks
resource "aws_api_gateway_method" "put_stocks" {
  rest_api_id   = aws_api_gateway_rest_api.STAT_API.id
  resource_id   = aws_api_gateway_resource.stocks_resource.id
  http_method   = "PUT"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_put_integration" {
  rest_api_id             = aws_api_gateway_rest_api.STAT_API.id
  resource_id             = aws_api_gateway_resource.stocks_resource.id
  http_method             = aws_api_gateway_method.put_stocks.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.update_shortlisted_stocks.invoke_arn
}

# Lambda Integration for DELETE /shortlisted_stocks
resource "aws_api_gateway_method" "delete_stocks" {
  rest_api_id   = aws_api_gateway_rest_api.STAT_API.id
  resource_id   = aws_api_gateway_resource.stocks_resource.id
  http_method   = "DELETE"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_delete_integration" {
  rest_api_id             = aws_api_gateway_rest_api.STAT_API.id
  resource_id             = aws_api_gateway_resource.stocks_resource.id
  http_method             = aws_api_gateway_method.delete_stocks.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.delete_shortlisted_stocks.invoke_arn
}

# Lambda Permission to Allow API Gateway Invocation
resource "aws_lambda_permission" "allow_api_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_shortlisted_stocks.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.STAT_API.execution_arn}/*/*"
}

# Lambda Permissions to Allow API Gateway Invocation
resource "aws_lambda_permission" "allow_api_invoke_create" {
  statement_id  = "AllowAPIGatewayInvokeCreate"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create_shortlisted_stocks.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.STAT_API.execution_arn}/*/*"
}

resource "aws_lambda_permission" "allow_api_invoke_update" {
  statement_id  = "AllowAPIGatewayInvokeUpdate"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.update_shortlisted_stocks.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.STAT_API.execution_arn}/*/*"
}

resource "aws_lambda_permission" "allow_api_invoke_delete" {
  statement_id  = "AllowAPIGatewayInvokeDelete"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.delete_shortlisted_stocks.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.STAT_API.execution_arn}/*/*"
}

# Deploy API
resource "aws_api_gateway_deployment" "api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.STAT_API.id
  depends_on = [
    aws_api_gateway_integration.lambda_get_integration,
    aws_api_gateway_integration.cors_integration,
    aws_api_gateway_integration.lambda_post_integration,
    aws_api_gateway_integration.lambda_put_integration,
    aws_api_gateway_integration.lambda_delete_integration
  ]
}

resource "aws_api_gateway_stage" "prod" {
  rest_api_id   = aws_api_gateway_rest_api.STAT_API.id
  stage_name    = "prod"
  deployment_id = aws_api_gateway_deployment.api_deployment.id
}
