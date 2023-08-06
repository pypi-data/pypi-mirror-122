#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Code to handle status commands"""

import click
from requests.models import HTTPError

from osducli.click_cli import global_params
from osducli.cliclient import CliOsduClient, handle_cli_exceptions
from osducli.config import (
    CONFIG_FILE_URL,
    CONFIG_LEGAL_URL,
    CONFIG_SCHEMA_URL,
    CONFIG_SEARCH_URL,
    CONFIG_STORAGE_URL,
    CONFIG_UNIT_URL,
    CONFIG_WORKFLOW_URL,
)


@click.command()
@handle_cli_exceptions
@global_params
def _click_command(state):
    # def _click_command(ctx, debug, config, hostname):
    """Shows the status of OSDU services"""
    status(state)


def status(state):  # pylint: disable=unused-argument
    """status command entry point

    Args:
        state (State): Global state
    """
    connection = CliOsduClient(state.config)
    # HTTPConnection.debuglevel = 1
    check_print_status(connection, "File service", CONFIG_FILE_URL, "readiness_check")
    check_print_status(connection, "Legal service", CONFIG_LEGAL_URL, "_ah/readiness_check")
    check_print_status(connection, "Schema service", CONFIG_SCHEMA_URL, "schema?limit=1")
    check_print_status(connection, "Search service", CONFIG_SEARCH_URL, "health/readiness_check")
    check_print_status(connection, "Storage service", CONFIG_STORAGE_URL, "health")
    check_print_status(connection, "Unit service", CONFIG_UNIT_URL, "../_ah/readiness_check")
    check_print_status(connection, "Workflow service", CONFIG_WORKFLOW_URL, "../readiness_check")


def check_print_status(
    connection: CliOsduClient, name: str, config_url_key: str, url_extra_path: str
):
    """Check the status of the given service and print information"""
    try:
        response = connection.cli_get(config_url_key, url_extra_path)
        print(f"{name.ljust(20)} {response.status_code}\t {response.reason}")
    except (HTTPError) as ex:
        print(f"{name.ljust(20)} {ex.response.status_code}\t {ex.response.reason}")
