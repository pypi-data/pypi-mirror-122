import argparse
import json
from .metadata import MetriqlMetadata
from .metabase import DatabaseOperation
import sys

__version__ = "0.3"


def main(args: list = None):
    parser = argparse.ArgumentParser(description="Synchronizes Metriql datasets to Metabase")

    parser.add_argument("command", choices=["create-database", "list-databases", "sync-database"],
                        help="command to execute")

    parser.add_argument("--metriql-url", help="metriql URL")
    parser.add_argument("--file", help="Read dataset from file instead of stdin")

    parser.add_argument("--database", help="Metabase database name that will be used when creating databases")
    parser.add_argument("--verbose", action="store_true", default=False, help="Verbose output",)

    parser.add_argument("--metabase-url", help="Metabase URL that you want to analyze metriql data")

    parser.add_argument("--metabase-username", help="Metabase username for generating API token")
    parser.add_argument("--metabase-password", help="Metabase password for generating API token")

    parsed = parser.parse_args(args=args)
    operation = DatabaseOperation(parsed.metabase_url, parsed.metabase_username, parsed.metabase_password, parsed.verbose)
    if parsed.command == "list-databases":
        databases = operation.list_databases()
        print(json.dumps(databases))
    elif parsed.command == "sync-database":
        if parsed.file is not None:
            source = open(parsed.file).read()
        else:
            source = sys.stdin.readline()
        metriql_metadata = MetriqlMetadata(parsed.metriql_url, json.loads(source))
        operation.sync(parsed.database, metriql_metadata)
