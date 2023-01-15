resource "aws_dynamodb_table" "mailchimp-list-import-history" {
  name           = "mailchimp-list-import-history"
  read_capacity  = 20
  write_capacity = 20
  billing_mode   = "PROVISIONED"
  hash_key       = "ListId"

  attribute {
    name = "ListId"
    type = "S"
  }

  tags = {
    Name = "mailchimp-list-import-history"
  }
}

resource "aws_dynamodb_table" "mailchimp-failed-imports" {
  name           = "mailchimp-failed-imports"
  read_capacity  = 20
  write_capacity = 20
  billing_mode   = "PROVISIONED"
  hash_key       = "ListId"
  range_key      = "offset"

  attribute {
    name = "ListId"
    type = "S"
  }

  attribute {
    name = "offset"
    type = "N"
  }

  tags = {
    Name = "mailchimp-failed-imports"
  }
}