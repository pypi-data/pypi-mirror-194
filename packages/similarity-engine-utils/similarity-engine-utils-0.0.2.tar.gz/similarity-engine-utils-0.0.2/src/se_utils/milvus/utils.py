from pymilvus import (FieldSchema, CollectionSchema, DataType, Collection,
                      utility)


def create_milvus_collection(
        collection_name,
        dim=768,
        drop_existing=False
):
    if drop_existing or not utility.has_collection(collection_name):
        utility.drop_collection(collection_name)

        fields = [
            FieldSchema(name='id', dtype=DataType.VARCHAR,
                        max_length=256, is_primary=True,
                        descrition='aws_filename'),

            FieldSchema(name='biz_id', dtype=DataType.INT64),
            FieldSchema(name='customer_id', dtype=DataType.INT64),
            FieldSchema(name='year', dtype=DataType.INT64),
            FieldSchema(name='month', dtype=DataType.INT64),
            FieldSchema(name='day', dtype=DataType.INT64),
            FieldSchema(name='mlflow_parent_run_id', dtype=DataType.VARCHAR,
                        max_length=256),
            FieldSchema(name='mlflow_run_id', dtype=DataType.VARCHAR,
                        max_length=256),
            FieldSchema(name='batch_id', dtype=DataType.VARCHAR,
                        max_length=256),
            FieldSchema(name='mail_log_id', dtype=DataType.INT64),
            FieldSchema(name='file_name', dtype=DataType.VARCHAR,
                        max_length=256),

            FieldSchema(name='path', dtype=DataType.VARCHAR,
                        descrition='path to image', max_length=512),
            FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR,
                        descrition='image embedding vectors', dim=dim),
            FieldSchema(name='metadata', dtype=DataType.VARCHAR,
                        descrition='metadata', max_length=1024),
        ]
        schema = CollectionSchema(fields=fields,
                                  description='reverse image search')
        collection = Collection(name=collection_name, schema=schema)

        index_params = {
            'metric_type': 'L2',
            'index_type': "IVF_FLAT",
            'params': {"nlist": 2048}
        }
        collection.create_index(field_name="embedding",
                                index_params=index_params)
    else:
        collection = Collection(name=collection_name)
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
