import asyncio
import logging

from data import Params
from data import DynamicParams
import aws_operations

logger = logging.getLogger()


async def get_maillist(session, offset, dynamicParamsIns: DynamicParams, since_timestamp=None, retrying=False):
    url_params = Params.return_mailchimp_url_params(offset, since_timestamp)
    list_id = dynamicParamsIns.get_list_id()

    response = await session.get(
        Params.MAILCHIMP_BASE_URL + "lists/" + list_id + "/members",
        headers=Params.MAILCHIMP_HEADERS,
        params=url_params
    )

    response_json = await response.json()

    if (response.status != 200):
        if (not retrying):
            await asyncio.sleep(1)
            return await get_maillist(session, offset, dynamicParamsIns, since_timestamp, True)
        else:
            error_message = 'Couldn\'t get the data from Mailchimp! Response Status Code: {} // Title: {} // Detail: {}'.format(
                response_json['status'], response_json['title'], response_json['detail'])
            logger.error(error_message)

            snsTopic = aws_operations.SnsTopic()
            snsTopic.publish(error_message)

            raise

    return response_json


async def post_maillist_to_target(session, converted_data, retrying=False):
    response = await session.post(
        Params.TARGET_BASE_URL,
        headers=Params.TARGET_HEADERS,
        json=converted_data)

    response_json = await response.json()

    if (response.status != 201):
        if (not retrying):
            await asyncio.sleep(1)
            return await post_maillist_to_target(session, converted_data, True)
        else:
            error_message = 'Couldn\'t post the data to target! Response Status Code: {} // Title: {} // Detail: {}'.format(
                response_json['status'], response_json['title'], response_json['detail'])
            logger.error(error_message)

            snsTopic = aws_operations.SnsTopic()
            snsTopic.publish(error_message)

            raise

    return response_json
