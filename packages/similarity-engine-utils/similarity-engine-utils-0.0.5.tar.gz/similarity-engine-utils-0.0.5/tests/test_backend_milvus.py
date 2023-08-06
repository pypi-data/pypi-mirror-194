from json.decoder import JSONDecodeError

import pymilvus
import pytest
from pymilvus.exceptions import MilvusException

from se_utils.backend.milvus.conf import DEFAULT_SCHEMA_URL
from se_utils.backend.milvus.core import (create_milvus_collection,
                                          generate_schema,
                                          milvus_dtype_mapping,
                                          open_schema_url, parse_schema,
                                          read_schema_json, setup_connection,
                                          validate_schema)
from se_utils.exceptions import BadCredentialsError, SchemaValidationError

from .utils import milvus_credentials, milvus_schema, milvus_schema_path


class TestBackendMilvus:
    @pytest.fixture(scope="function")
    def valid_milvus_credentials(self):
        creds = milvus_credentials(valid=True)
        return creds

    @pytest.fixture(scope="function")
    def invalid_milvus_credentials(self):
        creds = milvus_credentials(valid=False)
        return creds

    @pytest.fixture(scope="function")
    def valid_schema_valid_path(self):
        schema_path = milvus_schema_path(valid_schema=True, valid_path=True)
        return schema_path

    @pytest.fixture(scope="function")
    def valid_schema_invalid_path(self):
        schema_path = milvus_schema_path(valid_schema=False, valid_path=True)
        return schema_path

    @pytest.fixture(scope="function")
    def invalid_schema_path(self):
        schema_path = milvus_schema_path(valid_path=False)
        return schema_path

    @pytest.fixture(scope="function")
    def valid_schema(self):
        schema = milvus_schema(valid=True)
        return schema

    @pytest.fixture(scope="function")
    def invalid_schema(self):
        schema = milvus_schema(valid=False)
        return schema

    @pytest.mark.skip(reason="Can't be tested only under VPN")
    def test_setup_connection_valid(self, valid_milvus_credentials):
        res = setup_connection(valid_milvus_credentials)

        assert res is True

    @pytest.mark.skip(reason="Can't be tested only under VPN")
    def test_setup_connection_invalid(self, invalid_milvus_credentials):
        with pytest.raises(MilvusException):
            setup_connection(invalid_milvus_credentials)

        with pytest.raises(BadCredentialsError):
            invalid_milvus_credentials.pop('alias')
            setup_connection(invalid_milvus_credentials)

    @pytest.mark.parametrize(
        "valid_dtype",
        ["VARCHAR(32)", "INT16", "FLOAT_VECTOR(1024)"]
    )
    def test_milvus_dtype_mapping_valid(self, valid_dtype):
        valid = milvus_dtype_mapping(valid_dtype)

        assert isinstance(valid, dict)

    @pytest.mark.parametrize(
        "invalid_dtype",
        ["ololo", "lol32", "kek(1024)"]
    )
    def test_milvus_dtype_mapping_invalid(self, invalid_dtype):
        with pytest.raises(ValueError):
            milvus_dtype_mapping(invalid_dtype)

    def test_read_schema_json_valid(self, valid_schema_valid_path):
        schema_json = read_schema_json(valid_schema_valid_path)

        assert isinstance(schema_json, list)
        assert len(schema_json) != 0

    def test_read_schema_json_invalid(self, invalid_schema_path):
        with pytest.raises(JSONDecodeError):
            read_schema_json(invalid_schema_path)

    def test_validate_schema_valid(self, valid_schema):
        res = validate_schema(valid_schema)

        assert res is True

    def test_validate_schema_invalid(self, invalid_schema):
        with pytest.raises(SchemaValidationError):
            validate_schema(invalid_schema)

    def test_parse_schema_valid(self, valid_schema):
        fields, index_params = parse_schema(valid_schema)

        assert len(fields) != 0
        assert isinstance(fields[0], pymilvus.FieldSchema)
        assert len(index_params) != 0
        assert isinstance(index_params, dict)

    def test_parse_schema_invalid(self, invalid_schema):
        with pytest.raises(SchemaValidationError):
            parse_schema(invalid_schema)

    @pytest.mark.parametrize(
        "schema_url_valid",
        [DEFAULT_SCHEMA_URL]
    )
    def test_open_schema_url_valid(self, schema_url_valid):
        schema = open_schema_url(schema_url_valid)
        x = validate_schema(schema)

        assert isinstance(schema, list)
        assert x is True

    @pytest.mark.parametrize(
        "tag",
        ["yp"]
    )
    def test_generate_schema(self, tag):
        collection_schema, indices = generate_schema(tag)

        assert isinstance(collection_schema, pymilvus.CollectionSchema)
        assert isinstance(indices, dict)
        assert len(indices) > 0

    @pytest.mark.parametrize(
        "collection_name",
        ["test_collection"]
    )
    @pytest.mark.parametrize(
        "tag",
        ["yp"]
    )
    def test_create_milvus_collection(self, setup_milvus_test_connection, collection_name, tag):
        collection = create_milvus_collection(collection_name, tag)
        assert isinstance(collection, pymilvus.Collection)
