import json
import os.path
import re

import requests
from pymilvus import (Collection, CollectionSchema, DataType, FieldSchema,
                      connections, utility)

from ...exceptions import (BadCredentialsError, MilvusInsertDataSchemaError,
                           SchemaValidationError)
from .conf import DEFAULT_SCHEMA_URL, DEFAULT_SEARCH_PARAMS


def setup_connection(milvus_credentials: dict):
    if milvus_credentials.keys() != {"host", "port", "alias"}:
        message = f"Provided credentials are incorrect: {milvus_credentials}"
        raise BadCredentialsError(message=message)

    connections.connect(**milvus_credentials)
    return True


def milvus_dtype_mapping(x: str):
    res = None
    if re.match(r"VARCHAR\(\d+\)$", x):
        max_length = re.findall(r".*\((\d+)\).*", x)[0]
        res = {"dtype": DataType.VARCHAR, "max_length": max_length}

    elif re.match(r"FLOAT_VECTOR\(\d+\)$", x):
        dim = re.findall(r".*\((\d+)\).*", x)[0]
        res = {"dtype": DataType.FLOAT_VECTOR, "dim": dim}

    elif re.match(r"INT\d+$", x):
        bits = int(re.findall(r".*?(\d+)", x)[0])
        if bits in {8, 16, 32, 64}:
            res = {"dtype": DataType[x]}

    elif re.match(r"FLOAT$|DOUBLE$", x):
        res = {"dtype": DataType[x]}

    else:
        formats = ['VARCHAR(int)', 'FLOAT_VECTOR(int)' 'INT8', 'INT16',
                   'INT32', 'INT64']
        raise ValueError(f"Bad input: {x}. Available formats: {formats}")

    return res


def read_schema_json(x: str):
    if os.path.exists(x):
        with open(x) as f:
            schema_json = json.load(f)
    else:
        schema_json = json.loads(x)
    return schema_json


def validate_schema(schema: list[dict]):
    pk, msg = None, None
    available_keys = {'name', 'dtype', 'is_primary', 'description',
                      'index_params'}
    for item in schema:
        keys = set(item.keys())
        if not keys.issubset(available_keys):
            msg = f"Wrong schema keys: {keys}"
            break
        if item.get('is_primary'):
            if pk is None:
                pk = item['name']
            else:
                msg = f"Can't have more then 1 primary_key: `{pk}, {item['name']}`"
                break
        if re.match(r"FLOAT_VECTOR\(\d+\)$", item.get('dtype', '')):
            index_params_keys = {'metric_type', 'index_type', 'params'}
            if item.get('is_primary'):
                msg = f"Vector `{item['name']}` can't be a primary_key"
                break
            if not item.get('index_params'):
                msg = f"Vector `{item['name']}` doesn't have `index_params`"
                break
            keys = set(item.get('index_params').keys())
            if not keys.issubset(index_params_keys):
                msg = f"Vector `{item['name']} has wrong " \
                      f"index_params_keys keys: {keys}"
                break
        try:
            milvus_dtype_mapping(item['dtype'])
        except ValueError as e:
            msg = f"`dtype` validation error: {e}"
    if pk is None:
        msg = "Primary key is absent"
    if msg is not None:
        raise SchemaValidationError(message=msg)
    return True


def parse_schema(schema: list):
    validate_schema(schema)
    fields, index_params = [], {}
    for item in schema:
        if item.get('index_params'):
            index_params.update({item['name']: item['index_params']})
            item.pop('index_params')
        item.update(milvus_dtype_mapping(item['dtype']))
        fields.append(FieldSchema(**item))

    return fields, index_params


def open_schema_url(url):
    schema = json.loads(requests.get(url).content.decode())
    validate_schema(schema)
    return schema


def generate_schema(tag: str, schema: list = None) -> (CollectionSchema, dict):
    if tag == 'yp':
        schema = open_schema_url(DEFAULT_SCHEMA_URL)
    fields, index_params = parse_schema(schema)

    collection_schema = CollectionSchema(
        fields=fields,
        description='test collection')

    return collection_schema, index_params


def create_milvus_collection(
        collection_name,
        tag: str = 'yp',
        drop_existing: bool = True
):
    schema, indices = generate_schema(tag)

    if utility.has_collection(collection_name):
        if drop_existing:
            utility.drop_collection(collection_name)
        else:
            collection = Collection(collection_name)
            return collection
    collection = Collection(name=collection_name, schema=schema)

    for field_name, index_params in indices.items():
        collection.create_index(field_name=field_name,
                                index_params=index_params)
    return collection


def df2milvus(df, collection_name):
    collection = Collection(collection_name)
    collection_fields = {_.name for _ in collection.schema.fields}
    data_fields = set(df.columns)

    if data_fields == collection_fields:
        collection.insert(df)
        return True
    if collection_fields - data_fields:
        msg = f"Such fields are absent in provided df: {collection_fields - data_fields}"
    elif data_fields - collection_fields:
        msg = f"Such fields are redundant in provided df: {data_fields - collection_fields}"
    else:
        msg = f"No data fields provided: {data_fields}"
    raise MilvusInsertDataSchemaError(message=msg)


def search_similar_vector(
        collection_name,
        field_name,
        data,
        output_fields,
        limit=10,
        expr=None,
        search_params=DEFAULT_SEARCH_PARAMS

):
    collection = Collection(collection_name)
    collection.load()

    results = collection.search(
        data=[data],
        anns_field=field_name,
        param=search_params,
        limit=limit,
        expr=expr,
        output_fields=output_fields,
        consistency_level="Strong"
    )
    res = [{
        "distance": i.score,
        "values": i.entity._row_data  # {i.entity.get(j) for j in output_fields}
    }
        for i in results[0]]
    return res


# def construct_milvus_record(
#         id,
#         args,
#         path,
#         embedding,
#         metadata
# ):
#     data = [
#         [id],
#         [int(args['biz_id'])],
#         [int(args['customer_id'])],
#         [int(args['year'])],
#         [int(args['month'])],
#         [int(args['day'])],
#         [args.get('mlflow_parent_run_id', '')],
#         [args.get('mlflow_run_id', '')],
#         [args['batch_id']],
#         [int(args['mail_log_id'])],
#         [args['file_name']],
#         [path],
#         embedding,
#         [metadata]
#     ]
#     return data
#
#
# def search_similar_vectors(
#         collection_name,
#         emb_name,
#         data,
#         biz_id,
#         search_params: dict = None
# ):
#     collection = Collection(collection_name)
#     collection.load()
#
#     if search_params is None:
#         search_params = {"metric_type": "L2", "params": {"nprobe": 1},
#                          "offset": 1}
#
#     results = collection.search(
#         data=data,
#         anns_field=emb_name,
#         param=search_params,
#         limit=10,
#         expr=f"biz_id in [{biz_id}]",
#         output_fields=['id', 'customer_id', 'path'],
#         consistency_level="Strong"
#     )
#     return results
#
#
# def query_milvus_data(collection_name: str):
#     collection = Collection(collection_name)
#     collection.load()
#     res = collection.query(
#         expr="biz_id in [1]",
#         offset=0,
#         limit=10,
#         output_fields=["path", "customer_id"],
#         consistency_level="Strong"
#     )
#     return res
