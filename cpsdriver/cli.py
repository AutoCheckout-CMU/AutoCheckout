import argparse
from os import environ

ENVIRON_BASE = "AIFI_CPSWEEK_COMP__"


def parse_configs(args=None):
    """Read the config from the command line and ENV variables

    Note that command line arguments have priority over ENV variables. If
    neither is provided, we attempt to use a sane default value that is usually
    appropriate for local development.
    """
    # Commands
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--command",
        type=str,
        default=environ.get(f"{ENVIRON_BASE}COMMAND", "test"),
        help="Either the ID of a specific test case or 'submit'",
    )
    parser.add_argument(
        "--sample",
        type=str,
        default=environ.get(f"{ENVIRON_BASE}SAMPLE", "nodepth"),
        help="A subsample of data: 'all', 'nodepth'",
    )
    # Addresses
    parser.add_argument(
        "--db-address",
        type=str,
        default=environ.get(
            f"{ENVIRON_BASE}DB_ADDRESS",
            "mongodb://root:example@localhost:27017",
        ),
        help="The URI for a mongo dbms",
    )
    parser.add_argument(
        "--api-address",
        type=str,
        default=environ.get(
            f"{ENVIRON_BASE}API_ADDRESS",
            "http://aifi.io/cpsweek/api/v1",
        ),
        help="The AiFi submission API address",
    )
    # Submission Token
    parser.add_argument(
        "--token",
        type=str,
        default=environ.get(f"{ENVIRON_BASE}TOKEN", ""),
        help="The token provided to you by AiFi for submission",
    )
    # Log Level
    parser.add_argument(
        "--log-level",
        type=str,
        default=environ.get(f"{ENVIRON_BASE}LOG_LEVEL", "INFO"),
        help="Log level for driver",
    )
    args = parser.parse_args(args)
    # Strip quotes from addresses if they are there
    args.db_address = args.db_address.strip("\"'")
    args.api_address = args.api_address.strip("\"'")
    return args
