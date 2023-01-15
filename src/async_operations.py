import asyncio
import aiohttp

from data import Params
from data import DynamicParams
import aws_operations
import api_operations
import dto


async def process_task(session, offset, dynamicParamsIns: DynamicParams):
    try:
        mailchimp_response = await api_operations.get_maillist(session, offset, dynamicParamsIns)
        converted_data = dto.convert_mailchimp_data(mailchimp_response)
        target_response = await api_operations.post_maillist_to_target(session, converted_data)
    except:
        list_id = dynamicParamsIns.get_list_id()
        aws_operations.put_failed_import_item(list_id, offset)

    return converted_data


def get_tasks(session, dynamicParamsIns: DynamicParams):
    tasks = []
    offsets = dynamicParamsIns.get_offsets()
    for offset in offsets:
        tasks.append(asyncio.create_task(process_task(session, offset, dynamicParamsIns)))

    return tasks


async def run_processes(dynamicParamsIns: DynamicParams):
    connector = aiohttp.TCPConnector(limit=Params.TCP_CONNECTOR_LIMIT)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = get_tasks(session, dynamicParamsIns)
        responses = await asyncio.gather(*tasks)


async def initial_run(since_timestamp, dynamicParamsIns: DynamicParams):
    total_items = 0
    page_count = 0
    async with aiohttp.ClientSession() as session:
        try:
            mailchimp_response = await api_operations.get_maillist(session, 0, dynamicParamsIns, since_timestamp=since_timestamp)
            converted_data = dto.convert_mailchimp_data(mailchimp_response)
            target_response = await api_operations.post_maillist_to_target(session, converted_data)
            total_items = mailchimp_response['total_items']

            dynamicParamsIns.set_total_count(total_items)
            page_count = total_items//Params.DEFAULT_COUNT

            if (total_items % Params.DEFAULT_COUNT != 0):
                page_count += 1

            for i in range(1, page_count):
                dynamicParamsIns.add_offset(i)

        except:
            dynamicParamsIns.set_initial_error(True)
