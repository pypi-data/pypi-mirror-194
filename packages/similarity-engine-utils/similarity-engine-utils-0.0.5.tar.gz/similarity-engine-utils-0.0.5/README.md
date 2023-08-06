# similarity-engine-utils

Utility tools for easier management of feature-vector database and similar 
vector comparison

## Installation
---------------

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install library.

```bash
pip install similarity-engine-utils
```


## Initialize feature group
---------------------------

```python
bucket_name = '{bucket_for_feature_store}'
s3_folder = '{folder_for_feature_store}'
featuregroup_name = '{my_feature_name}_{commit_id}'

feature_group_name = f'{my_feature_name}/commit_id={featuregroup_name}'
feature_group = FeatureGroup(
        name=featuregroup_name,
        boto3_session = boto3_session,
        s3_uri=f"s3://{bucket_name}/{s3_folder}"
        )
```


## Create feature group
--------------------

```python

def create_feature_group(feature_group):
    description="What is my feature group about"
    feature_script_repo="{repo_link_to_script}"
    data_source="{what data are used}"

    record_identifier_feature_name = "column name to store id" 
    event_time_feature_name = "{column name to store timestamp}"

    partition_columns=['biz_id','customer_id']
    
    feature_definitions=[
        FeatureDefinition(feature_name="column_name1", feature_type=FeatureTypeEnum.INTEGRAL),
        FeatureDefinition(feature_name="column_name2", feature_type=FeatureTypeEnum.STRING),
        ]
    
    feature_group.create(
        record_identifier_name=record_identifier_feature_name,
        event_time_feature_name=event_time_feature_name,
        feature_script_repo=feature_script_repo,
        partition_columns=partition_columns,
        data_source=data_source,
        description=description,
        file_format='parquet/json',
        feature_definitions=feature_definitions
    )
    
    return feature_group

if feature_group.exists() is None:
    feature_group = create_feature_group(feature_group)

```

## Ingest data
--------------

```python
import pandas as pd
data = pd.read_json('data.json')
feature_group.ingest_data_frame(data,f"mlfow_parent_run_id={parent_run_id}/{filename_without_extention}")
```