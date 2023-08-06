import json
import re

from pymilvus import (Collection, CollectionSchema, DataType, FieldSchema,
                      connections, utility)

from ...exceptions import BadCredentialsError, SchemaParseError
from .schema import DEFAULT_SCHEMA_PARAMETERS


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
        res = {"dtype": DataType.VARCHAR, "dim": dim}

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


def validate_schema(schema: list[dict]):
    # todo: replace prints with extended logs
    pk = None
    available_keys = {'name', 'dtype', 'is_primary', 'description',
                      'index_params'}
    for item in schema:
        keys = set(item.keys())
        if not keys.issubset(available_keys):
            print(f"Wrong schema keys: {keys}")
            return False
        if item.get('is_primary'):
            if pk is None:
                pk = item['name']
            else:
                print(
                    f"Can't have more then 1 primary_key: `{pk}, {item['name']}`")
                return False
        if re.match(r"FLOAT_VECTOR\(\d+\)$", item.get('dtype', '')):
            index_params_keys = {'metric_type', 'index_type', 'params'}
            if item.get('is_primary'):
                print(f"Vector `{item['name']}` can't be a primary_key")
                return False
            if not item.get('index_params'):
                print(f"Vector `{item['name']}` doesn't have `index_params`")
                return False
            keys = set(item.get('index_params').keys())
            if not keys.issubset(index_params_keys):
                print(f"Vector `{item['name']} has wrong "
                      f"index_params_keys keys: {keys}")
                return False
    if pk is None:
        print("Primary key is absent")
        return False
    return True


def read_schema(path):
    with open(path) as f:
        schema_json = json.load(f)
    if not validate_schema(schema_json):
        raise SchemaParseError(
            message="Couldn't parse schema.")  # todo: extend traceback

    fields, index_params = [], []
    for item in schema_json:
        if item.get('index_params'):
            index_params.append({item['name']: item['index_params']})
            item.pop('index_params')
        item.update(milvus_dtype_mapping(item['dtype']))
        fields.append(FieldSchema(**item))

    return fields, index_params


def get_schema_params(tag: str):
    if tag != 'yp':
        raise NotImplementedError(
            f"Such tag=`{tag}` is not implemented."
        )
    return DEFAULT_SCHEMA_PARAMETERS[tag][0]


def generate_schema(tag: str):
    fields, index_params = get_schema_params(tag)

    schema = CollectionSchema(fields=fields,
                              description='test collection')
    indices = [(item.name, index_params[item.name])
               for item in fields if item.dim is not None]

    return schema, indices


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

    for field_name, index_params in indices:
        collection.create_index(field_name=field_name,
                                index_params=index_params)
    return collection


def construct_milvus_record(
        id,
        args,
        path,
        embedding,
        metadata
):
    data = [
        [id],
        [int(args['biz_id'])],
        [int(args['customer_id'])],
        [int(args['year'])],
        [int(args['month'])],
        [int(args['day'])],
        [args.get('mlflow_parent_run_id', '')],
        [args.get('mlflow_run_id', '')],
        [args['batch_id']],
        [int(args['mail_log_id'])],
        [args['file_name']],
        [path],
        embedding,
        [metadata]
    ]
    return data


def search_similar_vectors(
        collection_name,
        emb_name,
        data,
        biz_id,
        search_params: dict = None
):
    collection = Collection(collection_name)
    collection.load()

    if search_params is None:
        search_params = {"metric_type": "L2", "params": {"nprobe": 1},
                         "offset": 1}

    results = collection.search(
        data=data,
        anns_field=emb_name,
        param=search_params,
        limit=10,
        expr=f"biz_id in [{biz_id}]",
        output_fields=['id', 'customer_id', 'path'],
        consistency_level="Strong"
    )
    return results


def query_milvus_data(collection_name: str):
    collection = Collection(collection_name)
    collection.load()
    res = collection.query(
        expr="biz_id in [1]",
        offset=0,
        limit=10,
        output_fields=["path", "customer_id"],
        consistency_level="Strong"
    )
    return res
