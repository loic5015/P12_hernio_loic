import server
import pytest
from event.views import AdminCustomerViewset, AdminContractViewset

@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client

