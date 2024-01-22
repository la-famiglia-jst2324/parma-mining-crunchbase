from unittest.mock import patch

import pytest

from parma_mining.crunchbase.client import CrunchbaseClient
from parma_mining.crunchbase.model import DiscoveryResponse
from parma_mining.mining_common.exceptions import ClientError


@pytest.fixture
def mock_crunchbase_client():
    return CrunchbaseClient()


@patch("parma_mining.crunchbase.client.search")
def test_discover_company_success(mock_search, mock_crunchbase_client):
    mock_search.return_value = [
        "https://www.crunchbase.com/organization/test",
        "https://www.crunchbase.com/organization/test/more",
    ]

    results = mock_crunchbase_client.discover_company("Test")
    assert isinstance(results, DiscoveryResponse)
    print(results.handles)
    assert len(results.handles) == 1
    assert results.handles[0] == "https://www.crunchbase.com/organization/test"


@patch("parma_mining.crunchbase.client.search")
def test_search_organizations_exception(mock_search_users, mock_crunchbase_client):
    mock_search_users.side_effect = ClientError()
    with pytest.raises(ClientError):
        mock_crunchbase_client.discover_company("Test")
