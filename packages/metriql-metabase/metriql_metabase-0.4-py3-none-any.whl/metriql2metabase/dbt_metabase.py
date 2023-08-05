# Source file: https://github.com/gouline/dbt-metabase/blob/master/dbtmetabase/metabase.py
import json
import logging
from typing import (
    Sequence,
    Optional,
    Tuple,
    Iterable,
    MutableMapping,
    Union,
    List,
    Mapping,
)

import requests
import time

from .models.metabase import MetabaseModel, MetabaseColumn

import re


class MetabaseClient:
    """Metabase API client."""

    _SYNC_PERIOD_SECS = 5

    def __init__(
            self,
            host: str,
            user: str,
            password: str,
            verify: Union[str, bool] = None,
    ):
        """Constructor.
        Arguments:
            host {str} -- Metabase hostname.
            user {str} -- Metabase username.
            password {str} -- Metabase password.
        Keyword Arguments:
            use_http {bool} -- Use HTTP instead of HTTPS. (default: {False})
            verify {Union[str, bool]} -- Path to certificate or disable verification. (default: {None})
        """

        self.host = host.rstrip('/')
        self.verify = verify
        self.session_id = self.get_session_id(user, password)
        self.collections: Iterable = []
        self.tables: Iterable = []
        self.table_map: MutableMapping = {}
        self.models_exposed: List = []
        self.native_query: str = ""
        self.exposure_parser = re.compile(r"[FfJj][RrOo][OoIi][MmNn]\s+\b(\w+)\b")
        self.cte_parser = re.compile(
            r"[Ww][Ii][Tt][Hh]\s+\b(\w+)\b\s+as|[)]\s*[,]\s*\b(\w+)\b\s+as"
        )
        logging.info("Session established successfully")

    def get_session_id(self, user: str, password: str) -> str:
        """Obtains new session ID from API.
        Arguments:
            user {str} -- Metabase username.
            password {str} -- Metabase password.
        Returns:
            str -- Session ID.
        """

        return self.api(
            "post",
            "/api/session",
            authenticated=False,
            json={"username": user, "password": password},
        )["id"]

    def sync_and_wait(
            self,
            database_id: int,
            models: Sequence,
            timeout: Optional[int],
    ) -> bool:
        if timeout is None:
            timeout = 30

        if timeout < self._SYNC_PERIOD_SECS:
            logging.critical(
                "Timeout provided %d secs, must be at least %d",
                timeout,
                self._SYNC_PERIOD_SECS,
            )
            return False

        if not database_id:
            logging.critical("Cannot find database id %s", database_id)
            return False

        self.api("post", f"/api/database/{database_id}/sync_schema")

        deadline = int(time.time()) + timeout
        sync_successful = False
        while True:
            sync_successful = self.models_compatible(database_id, models)
            time_after_wait = int(time.time()) + self._SYNC_PERIOD_SECS
            if not sync_successful and time_after_wait <= deadline:
                time.sleep(self._SYNC_PERIOD_SECS)
            else:
                break
        return sync_successful

    def models_compatible(self, database_id: str, models: Sequence) -> bool:
        """Checks if models compatible with the Metabase database schema.
        Arguments:
            database_id {str} -- Metabase database ID.
            models {list} -- List of dbt models read from project.
        Returns:
            bool -- True if schema compatible with models, false otherwise.
        """

        _, field_lookup = self.build_metadata_lookups(database_id)

        are_models_compatible = True
        for model in models:

            schema_name = model.schema.upper()
            model_name = model.name.upper()

            lookup_key = f"{schema_name}.{model_name}"

            if lookup_key not in field_lookup:
                logging.warning(
                    "Model %s not found in %s schema", lookup_key, schema_name
                )
                are_models_compatible = False
            else:
                table_lookup = field_lookup[lookup_key]
                for column in model.columns:
                    column_name = column.name.upper()
                    if column_name not in table_lookup:
                        logging.warning(
                            "Column %s not found in %s model", column_name, lookup_key
                        )
                        are_models_compatible = False

        return are_models_compatible

    def export_models(
            self,
            database_id: int,
            models: Sequence[MetabaseModel],
    ):
        table_lookup, field_lookup = self.build_metadata_lookups(database_id)
        for model in models:
            self.export_model(model, table_lookup, field_lookup)

    def export_model(
            self,
            model: MetabaseModel,
            table_lookup: dict,
            field_lookup: dict,
    ):
        """Exports one dbt model to Metabase database schema.
        Arguments:
            model {dict} -- One dbt model read from project.
            table_lookup {dict} -- Dictionary of Metabase tables indexed by name.
            field_lookup {dict} -- Dictionary of Metabase fields indexed by name, indexed by table name.
            aliases {dict} -- Provided by reader class. Shuttled down to column exports to resolve FK refs against relations to aliased source tables
        """

        schema_name = model.schema.upper()
        model_name = model.name.upper()

        lookup_key = f"{schema_name}.{model_name}"

        api_table = table_lookup[lookup_key]
        if not api_table:
            logging.error("Table %s does not exist in Metabase", lookup_key)
            return

        table_id = api_table["id"]
        compiled = {"description": model.description or None,
                    'display_name': model.label or None,
                    "visibility_type": None if model.hidden else "hidden"}

        if self._check_if_subset(compiled, api_table):
            # Update with new values
            self.api("put", f"/api/table/{table_id}", json=compiled, )
            logging.info("Updated table %s successfully", lookup_key)
        else:
            logging.info("Table %s is up-to-date", lookup_key)

        for column in model.columns:
            self.export_column(schema_name, model_name, column, field_lookup)

        for metric in model.metrics:
            self.export_column(schema_name, model_name, MetabaseColumn(metric.name, visibility_type="normal"),
                               field_lookup)

    def export_column(
            self,
            schema_name: str,
            model_name: str,
            column: MetabaseColumn,
            field_lookup: dict,
    ):
        """Exports one dbt column to Metabase database schema.
        Arguments:
            model_name {str} -- One dbt model name read from project.
            column {dict} -- One dbt column read from project.
            field_lookup {dict} -- Dictionary of Metabase fields indexed by name, indexed by table name.
        """

        table_lookup_key = f"{schema_name}.{model_name}"
        column_name = column.name.upper()

        field = field_lookup.get(table_lookup_key, {}).get(column_name)
        if not field:
            logging.error(
                "Field %s.%s does not exist in Metabase", table_lookup_key, column_name
            )
            return

        field_id = field["id"]

        api_field = self.api("get", f"/api/field/{field_id}")

        if "special_type" in api_field:
            semantic_type = "special_type"
        else:
            semantic_type = "semantic_type"

        fk_target_field_id = None
        if column.semantic_type == "type/FK":
            raise Exception("semantic_type `type/FK` is not supported.")

        # Nones are not accepted, default to normal
        if not column.visibility_type:
            column.visibility_type = "normal"

        # Empty strings not accepted by Metabase
        if not column.description:
            column_description = None
        else:
            column_description = column.description

        if (
                api_field["description"] != column_description
                or api_field[semantic_type] != column.semantic_type
                or api_field["visibility_type"] != column.visibility_type
                or api_field["fk_target_field_id"] != fk_target_field_id
        ):
            # Update with new values
            self.api(
                "put",
                f"/api/field/{field_id}",
                json={
                    "description": column_description,
                    semantic_type: column.semantic_type,
                    "display_name": column.label or None,
                    "visibility_type": column.visibility_type,
                    "fk_target_field_id": fk_target_field_id,
                },
            )
            logging.info("Updated field %s.%s successfully", model_name, column_name)
        else:
            logging.info("Field %s.%s is up-to-date", model_name, column_name)

    def find_database_id(self, name: str) -> Optional[str]:
        for database in self.api("get", "/api/database"):
            if database["name"].upper() == name.upper():
                return database["id"]
        return None

    def build_metadata_lookups(
            self, database_id: str, schemas_to_exclude: Iterable = None
    ) -> Tuple[dict, dict]:
        """Builds table and field lookups.
        Arguments:
            database_id {str} -- Metabase database ID.
        Returns:
            dict -- Dictionary of tables indexed by name.
            dict -- Dictionary of fields indexed by name, indexed by table name.
        """

        if schemas_to_exclude is None:
            schemas_to_exclude = []

        table_lookup = {}
        field_lookup = {}

        metadata = self.api(
            "get",
            f"/api/database/{database_id}/metadata",
            params=dict(include_hidden=True),
        )
        for table in metadata.get("tables", []):
            table_schema = table.get("schema")
            table_schema = table_schema.upper() if table_schema else "PUBLIC"
            table_name = table["name"].upper()

            if schemas_to_exclude:
                schemas_to_exclude = {
                    exclusion.upper() for exclusion in schemas_to_exclude
                }

                if table_schema in schemas_to_exclude:
                    logging.debug(
                        "Ignoring Metabase table %s in schema %s. It belongs to excluded schemas %s",
                        table_name,
                        table_schema,
                        schemas_to_exclude,
                    )
                    continue

            lookup_key = f"{table_schema}.{table_name}"
            table_lookup[lookup_key] = table
            table_field_lookup = {}

            for field in table.get("fields", []):
                field_name = field["name"].upper()
                table_field_lookup[field_name] = field

            field_lookup[lookup_key] = table_field_lookup

        return table_lookup, field_lookup

    @staticmethod
    def _get_metric(metabase_metrics, lookup_key, table_id, metric_name, remove=False):
        this_metric: MutableMapping = {}
        for j, existing_metric in enumerate(metabase_metrics):
            if (
                    metric_name == existing_metric["name"]
                    and table_id == existing_metric["table_id"]
            ):
                if this_metric:
                    logging.error("Duplicate metric in model %s", lookup_key)
                logging.info(
                    "Existing metric %s found for %s", metric_name, lookup_key
                )
                this_metric = existing_metric
                if remove:
                    metabase_metrics.pop(j)
        return this_metric

    @staticmethod
    def _check_if_subset(subset: dict, subset_list: dict):
        for key, value in subset.items():
            if subset_list[key] != value:
                return False
        return True

    def sync_metrics(
            self,
            database_id: int,
            models: List[MetabaseModel],
            revision_header: str = "Metric has been updated. ",
    ):
        metabase_metrics = self.api("get", "/api/metric")
        table_lookup, field_lookup = self.build_metadata_lookups(database_id)

        for model in models:
            schema_name = model.schema.upper()
            model_name = model.name.upper()

            lookup_key = f"{schema_name}.{model_name}"
            logging.info("Syncing metrics for %s", lookup_key)

            api_table = table_lookup.get(lookup_key)

            if not api_table:
                logging.error("Table %s does not exist in Metabase", lookup_key)
                continue

            table_id = api_table["id"]

            for metric in model.metrics:
                metric_name = metric.name
                field_id = list(filter(lambda f: f['name'] == metric_name, api_table['fields']))[0]['id']

                this_metric = self._get_metric(metabase_metrics, lookup_key, table_id, metric_name, remove=True)

                metric_description = metric.description or "No description provided"
                compiled = {
                    "name": metric_name,
                    "description": metric_description,
                    "table_id": table_id,
                    "definition": {
                        "source-table": table_id,
                        "aggregation": [
                            [
                                "sum",
                                ["field-id", field_id],
                            ]
                        ],
                    },
                }
                if this_metric:
                    # Revise
                    agglomerate_changes = ""
                    # Check Name, Description, Table Id, and Definition
                    if this_metric["name"] != compiled["name"]:
                        agglomerate_changes += f'Name changed from {this_metric["name"]} to {compiled["name"]}. '
                    if this_metric["description"] != compiled["description"]:
                        agglomerate_changes += f'Description changed from {this_metric["description"]} to {compiled["description"]}. '
                    if this_metric["definition"] != compiled["definition"]:
                        agglomerate_changes += (f'Formula definition updated')

                    if not self._check_if_subset(compiled, this_metric):
                        compiled["revision_message"] = (revision_header + agglomerate_changes)
                        output_metric = self.api("put", f"/api/metric/{this_metric['id']}", json=compiled)
                        logging.info("Metric %s updated!", metric_name)
                        logging.debug(output_metric)
                    else:
                        logging.info("No changes to %s", metric_name)
                else:
                    # Create metric
                    self.api("post", "/api/metric/", json=compiled)
                    logging.info("Metric %s created!", metric_name)
        for metric in metabase_metrics:
            if database_id == metric.get('database_id'):
                output_metric = self.api(
                    "put", f"/api/metric/{metric['id']}",
                    json={"archived": True, "revision_message": "Removed from the Metriql datasets or created manually"}
                )
                logging.info("Metric `%s` retired because it doesn't exist anymore!", metric['name'])
                logging.debug(output_metric)

    def api(
            self,
            method: str,
            path: str,
            authenticated: bool = True,
            critical: bool = True,
            **kwargs,
    ) -> Mapping:
        """Unified way of calling Metabase API.
        Arguments:
            method {str} -- HTTP verb, e.g. get, post, put.
            path {str} -- Relative path of endpoint, e.g. /api/database.
        Keyword Arguments:
            authenticated {bool} -- Includes session ID when true. (default: {True})
            critical {bool} -- Raise on any HTTP errors. (default: {True})
        Returns:
            Any -- JSON payload of the endpoint.
        """

        headers: MutableMapping = {}
        if "headers" not in kwargs:
            kwargs["headers"] = headers
        else:
            headers = kwargs["headers"].copy()

        if authenticated:
            headers["X-Metabase-Session"] = self.session_id

        url_path = f"{self.host}{path}"
        response = requests.request(
            method, url_path, verify=self.verify, **kwargs
        )

        if critical:
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                if "password" in kwargs["json"]:
                    logging.error("HTTP request failed. Response: %s", response.text)
                else:
                    logging.error(
                        "HTTP request failed. Payload: %s. Response: %s",
                        kwargs["json"],
                        response.text,
                    )
                raise
        elif not response.ok:
            return {}

        try:
            response_json = json.loads(response.text)
        except:
            raise Exception("Unable to run API Request on ({}): {}".format(url_path, response.text or '(empty)'))

        # Since X.40.0 responses are encapsulated in "data" with pagination parameters
        if "data" in response_json:
            return response_json["data"]

        return response_json
