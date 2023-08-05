import logging
import sys

from metriql2metabase.dbt_metabase import MetabaseClient
from metriql2metabase.models.metabase import MetabaseModel, MetabaseColumn, MetabaseMetric


class DatabaseOperation:
    client: MetabaseClient

    def __init__(self, metabase_url, username, password, verbose):
        self.client = MetabaseClient(metabase_url, username, password)
        if verbose:
            logger = logging.getLogger()
            logger.addHandler(logging.StreamHandler(sys.stdout))
            logger.setLevel(logging.DEBUG)

    def list_databases(self):
        return list(map(lambda database: {"id": database.get('name'), "name": database.get('name')},
                        filter(lambda database: database.get('engine') in ['trino', 'presto'],
                               self.client.api('get', '/api/database'))))

    def sync(self, database, metadata, sync_skip=False, sync_timeout=None):

        models = list(map(
            lambda dataset: self._convert_dataset(dataset,
                                                  metadata.get_dimensions(dataset.get('name')),
                                                  metadata.get_measures(dataset.get('name'))),
            metadata.get_datasets()))

        database_id = self.client.find_database_id(database)

        if not sync_skip:
            if not self.client.sync_and_wait(
                    database_id,
                    models,
                    sync_timeout,
            ):
                logging.critical("Sync timeout reached, models still not compatible")
                return

        table_lookup, field_lookup = self.client.build_metadata_lookups(database_id)

        self.client.export_models(table_lookup, field_lookup, models)
        self.client.sync_metrics(table_lookup, database_id, models)
        print("Successfully synchronized {} datasets".format(len(models)))

    @staticmethod
    def _convert_dataset(dataset, dimensions, measures):
        metrics = list(map(lambda v: DatabaseOperation._convert_measure(v[0], v[1][0]), measures.items()))
        return MetabaseModel(dataset.get('name'),
                             dataset.get('category') or "public",
                             dataset.get('description'),
                             dataset.get('label'),
                             DatabaseOperation._convert_dimensions(dimensions),
                             metrics,
                             dataset.get('hidden') or False)

    @staticmethod
    def _convert_dimensions(dimensions):
        columns = []
        for name, value in dimensions.items():
            description = value[0].get('description')
            label = value[0].get('label') or value[0].get('name')
            prefix = (value[1] or {}).get('label') or (value[1] or {}).get('name')
            if prefix:
                label = prefix + ' / ' + label
            semantic_type = value[0].get('report', {}).get('metabase', {}).get('semantic_type')
            visibility_type = "hidden" if value[0].get('hidden') else None
            if value[0].get('postOperations') is not None:
                for post_operation in value[0].get('postOperations'):
                    columns.append(
                        MetabaseColumn('{}::{}'.format(name, post_operation), description,
                                       '{} ({})'.format(label, post_operation), semantic_type,
                                       visibility_type))
            else:
                columns.append(MetabaseColumn(name, description, label, semantic_type, visibility_type))
        return columns

    @staticmethod
    def _convert_measure(column_reference, measure):
        label = measure.get('label')
        if not label:
            label = measure.get('name')
        return MetabaseMetric(column_reference, label, measure.get('description'))
