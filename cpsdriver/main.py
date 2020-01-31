import sys
import logging

from cpsdriver.clients import (
    CpsMongoClient,
    CpsApiClient,
    TestCaseClient,
)
from cpsdriver.cli import parse_configs
from cpsdriver.log import setup_logger


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def main(args=None):
    args = parse_configs(args)
    setup_logger(args.log_level)
    mongo_client = CpsMongoClient(args.db_address)
    api_client = CpsApiClient()
    test_client = TestCaseClient(mongo_client, api_client)
    test_client.load(f"{args.command}-{args.sample}")
    logger.info(f"Available Test Cases are {test_client.available_test_cases}")
    test_client.set_context(args.command, load=False)
    generate_receipts(test_client)


def generate_receipts(test_client):
    products = test_client.list_products()
    logger.info(f"An example product is {products[-1]}")
    facings = test_client.find_product_facings(products[-1].product_id)
    logger.info(f"The facings of it are {facings}")
    logger.info(
        f"Valid data types for this sample are {test_client.valid_data_types}"
    )
    example_types = ["depth", "targets", "plate_data", "frame_message"]
    for _type in example_types:
        example = test_client.find_first_after_time(_type, 0.0)
        logger.info(f"The first {_type} is {example}")


if __name__ == "__main__":
    main(args=sys.argv[1:])
