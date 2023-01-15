class Params:
    MAILCHIMP_BASE_URL = "https://us9.api.mailchimp.com/3.0/"
    TARGET_BASE_URL = "https://api-demo-target-url"
    MAILCHIMP_HEADERS = {
        'Authorization': 'API-Key, 1234-somekey',
        'Content-Type': 'application/json'}
    TARGET_HEADERS = {
        'Authorization': '1234-somekey',
        'Content-Type': 'application/json'}
    S3_BUCKET_NAME = "mailchimp-list-ids"
    DYNAMODB_TABLE_NAME = "mailchimp-list-import-history"
    DYNAMODB__FAILED_IMPORT_TABLE_NAME = "mailchimp-failed-imports"
    DEFAULT_COUNT = 1000
    TCP_CONNECTOR_LIMIT = 10

    @classmethod
    def return_mailchimp_url_params(cls, offset, since_timestamp=None):
        params = {
            'count': cls.DEFAULT_COUNT,
            'offset': offset,
            'fields': 'members.id,members.email_address,members.status,members.merge_fields,total_items'}
        if (since_timestamp):
            params['since_last_changed'] = since_timestamp

        return params


class DynamicParams:
    def __init__(self) -> None:
        self.__LIST_ID = ""
        self.__TOTAL_COUNT = 0
        self.__IS_THERE_INITIAL_ERROR = False
        self.__offsets = []

    def set_list_id(self, list_id):
        self.__LIST_ID = list_id

    def get_list_id(self):
        return self.__LIST_ID

    def set_total_count(self, total_count):
        self.__TOTAL_COUNT = total_count

    def get_total_count(self):
        return self.__TOTAL_COUNT

    def set_initial_error(self, is_initial_error):
        self.__IS_THERE_INITIAL_ERROR = is_initial_error

    def get_initial_error(self):
        return self.__IS_THERE_INITIAL_ERROR

    def add_offset(self, offset):
        self.__offsets.append(offset)

    def get_offsets(self):
        return self.__offsets
