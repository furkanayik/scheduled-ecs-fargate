from boto3.dynamodb.types import TypeDeserializer


def convert_mailchimp_data(mailchimp_data):
    payload = []
    for member in mailchimp_data['members']:
        list_member = {
            'id': member['id'],
            'firstname': member['merge_fields']['FNAME'],
            'lastname': member['merge_fields']['LNAME'],
            'email': member['email_address'],
            'status': member['status'],
        }
        payload.append(list_member)

    return payload


def deserialize_dynamodb_items(dynamodb_item, type_deserializer=TypeDeserializer()):
    return type_deserializer.deserialize({"M": dynamodb_item})
