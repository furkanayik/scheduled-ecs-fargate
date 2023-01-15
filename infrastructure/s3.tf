resource "aws_s3_bucket" "b" {
  bucket = "mailchimp-list-ids"

  tags = {
    Name        = "mailchimp-list-ids"
  }
}

resource "aws_s3_bucket_object" "json_file" {
  bucket = aws_s3_bucket.b.id
  key    = "data.json"
  content = <<EOF
{
  "listId": "1234-someid"
}
EOF
}