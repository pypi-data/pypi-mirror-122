# Metriql Metabase Integration 

Synchronize Metabase datasets from Metriql datasets. The idea is to leverage Metriql datasets in your Metabase workflow without any additional modeling in Metabase.

### Usage

The library is available in PyPI so you can install it via pip as follows:

```
pip install metriql-metabase
```

The library expects `stdin` for the Metriql metadata and interacts with Metabase via its API. Here is an example:

```
curl http://metriql-server.com/api/v0/metadata | metriql-metabase --metriql-url http://metriql-server.com --metabase-username USERNAME --metabase-password PASSWORD --metabase-database METABASE_DATABASE_NAME sync-database
```

You can use `--file` argument instead of reading the metadata from `stdin` as an alternative.

Available commands are `list-databases`, `sync-database`.

### FAQ

#### Do you support Metabase Cloud?

Yes!

#### How is this related to [dbt-metabase](https://github.com/gouline/dbt-metabase)?

While this metriql-metabase is heavily influenced by the [dbt-metabase](https://github.com/gouline/dbt-metabase) codebase, 
it integrates Metabase with Metriql, not directly to dbt. While you need to maintain Metriql as a separate service, here are advantages of Metriql over dbt-metabase:

* You can define the metrics as native SQL
* You can leverage [Aggregates](https://metriql.com/introduction/aggregates) to speed up your queries
* Sync the datasets into [various data tools](https://metriql.com/integrations/bi-tools/index), not just Metabase
* Native [MQL](https://metriql.com/query/mql) experience when running ad-hoc queries on data.

