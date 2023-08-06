from pymilvus import DataType, FieldSchema

DEFAULT_SCHEMA_PARAMETERS = {
    "yp": [
        {
            "fields": [
                FieldSchema(name='id', dtype=DataType.VARCHAR,
                            max_length=256, is_primary=True,
                            descrition='aws_filename'),

                FieldSchema(name='biz_id', dtype=DataType.INT64),
                FieldSchema(name='customer_id', dtype=DataType.INT64),
                FieldSchema(name='year', dtype=DataType.INT64),
                FieldSchema(name='month', dtype=DataType.INT64),
                FieldSchema(name='day', dtype=DataType.INT64),
                FieldSchema(name='mlflow_parent_run_id',
                            dtype=DataType.VARCHAR,
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

                FieldSchema(name="emb1", dtype=DataType.FLOAT_VECTOR,
                            descrition="google/vit-large-patch16-224-in21k",
                            dim=1024)
            ],
            "index_params": {
                "emb1": {
                    'metric_type': 'L2',
                    'index_type': "FLAT",
                    "params": {}
                }
            }
        }
    ]
}
