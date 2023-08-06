import pytest
from pymilvus.exceptions import MilvusException

from se_utils.backend.milvus.core import setup_connection
from se_utils.exceptions import BadCredentialsError
from .utils import milvus_test_credentials


class TestBackendMilvus:
    @pytest.fixture(scope="function")
    def milvus_credentials(self):
        return milvus_test_credentials()

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
