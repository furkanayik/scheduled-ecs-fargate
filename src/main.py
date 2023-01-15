import asyncio
import time
import logging

import aws_operations
import async_operations
from data import DynamicParams


logging.getLogger().setLevel(logging.INFO)


def main():
    logging.info('Import started...')

    start_time = time.time()

    dynamicParams = DynamicParams()

    since_timestamp = None
    list_id = aws_operations.get_s3_list_id()
    dynamicParams.set_list_id(list_id)

    import_history_record = aws_operations.get_list_import_history_record(
        list_id)

    if (import_history_record):
        since_timestamp = import_history_record['LastImportTime']

    asyncio.run(async_operations.initial_run(since_timestamp, dynamicParams))

    if(not dynamicParams.get_initial_error()):
        aws_operations.upsert_list_import_history(list_id)
        asyncio.run(async_operations.run_processes(dynamicParams))
    else:
        error_message = 'Due to errors occured, job is being terminated... Error details are published to the topic'
        logging.error(error_message)

    end_time = time.time()
    total_time = end_time - start_time

    logging.info('Import job has finished.')
    logging.info('Run time {:.2f} seconds. // total process count: {} // Imported member count: {}'.format(
        round(total_time, 2), len(dynamicParams.get_offsets()) + 1, dynamicParams.get_total_count()))


if __name__ == "__main__":
    main()
