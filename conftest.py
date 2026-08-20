import pytest
from common.http_client import HttpClient
from config import BASE_URL

@pytest.fixture(scope="module")
def http_client():
    client = HttpClient(BASE_URL)
    yield client
    # 每个用例执行完成后清空cookie
    client.clear_cookie()
