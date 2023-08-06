from pymilvus import Collection, CollectionSchema, connections, utility

from ...exceptions import BadCredentialsError
from .schema import DEFAULT_SCHEMA_PARAMETERS


def setup_connection(milvus_credentials: dict):
    if milvus_credentials.keys() != {"host", "port", "alias"}:
        message = f"Provided credentials are incorrect: {milvus_credentials}"
        raise BadCredentialsError(message=message)

    connections.connect(**milvus_credentials)
    return True


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
        biz_id,
        data
):
    collection = Collection(collection_name)
    collection.load()

    search_params = {"metric_type": "L2", "params": {"nprobe": 10},
                     "offset": 5}

    results = collection.search(
        data=data,
        anns_field="embedding",
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
