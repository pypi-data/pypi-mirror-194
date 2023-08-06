import pytest
from pymilvus.exceptions import MilvusException

from se_utils.backend.milvus.core import milvus_dtype_mapping, setup_connection
from se_utils.exceptions import BadCredentialsError

from .utils import milvus_test_credentials


class TestBackendMilvus:
    @pytest.fixture(scope="function")
    def valid_milvus_credentials(self):
        creds = milvus_test_credentials()
        return creds

    @pytest.fixture(scope="function")
    def invalid_milvus_credentials(self):
        creds = milvus_test_credentials()
        creds.pop('host')
        return creds

    @pytest.mark.skip(reason="Can't be tested only under VPN")
    def test_setup_connection(self, milvus_credentials):
        try:
            res_good = setup_connection(milvus_credentials)
        except MilvusException:
            res_good = False

        try:
            milvus_credentials.pop('host')
            res_bad = setup_connection(milvus_credentials)
        except BadCredentialsError:
            res_bad = False

        assert res_good is True
        assert res_bad is False

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
