from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from parma_mining.crunchbase.client import CrunchbaseClient
from parma_mining.crunchbase.model import DiscoveryResponse
from parma_mining.mining_common.exceptions import ClientError, CrawlingError


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


@patch("parma_mining.crunchbase.client.ApifyClient")
def test_get_company_details(mock_apify_client, mock_crunchbase_client):
    # Create a mock for ApifyClient
    mock_client = MagicMock()
    mock_apify_client.return_value = mock_client

    # Prepare mock results
    mock_run_result = {
        "defaultDatasetId": "mocked_dataset_id",
        # ... (other fields you expect in the result)
    }

    # Prepare mock dataset item
    mock_item = {
        "identifier": {"value": "Mocked Company", "permalink": "mocked-company"},
        "short_description": "Mocked description",
        "website": {"value": "http://www.mockedcompany.com"},
        "ipo_status": "Mocked IPO Status",
        "overview_company_fields": {"company_type": "Mocked Company Type"},
        "overview_fields_extended": {
            "founded_on": {"value": "2022-01-20"},
            "legal_name": "Mocked Legal Name",
            "categories": [],
        },
        "num_employees_enum": "100",
        "rank_org_company": 42,
        "location_identifiers": [],
        "funding_rounds_list": [],
        "investors_list": [],
        "acquired_by_fields": {},
        "acquisitions_list": [],
        "org_similarity_list": [],
        "current_employees_featured_order_field": [],
        "event_appearances_list": [],
        "semrush_location_list": [],
        "funding_total": {"value_usd": 1000000},
        "last_funding_type": "Mocked Funding Type",
        "funding_rounds_summary": {
            "last_funding_at": "2022-01-21",
            "num_funding_rounds": 3,
        },
        "investors_summary": {"num_investors": 5},
        "technology_highlights": {"builtwith_num_technologies_used": 10},
        "apptopia_summary": {
            "apptopia_total_apps": 50,
            "apptopia_total_downloads": 100000,
        },
        "contact_fields": {
            "contact_email": "mocked@example.com",
            "phone_number": "+1234567890",
        },
        "company_overview_highlights": {"num_org_similarities": 7},
        "people_highlights": {"num_current_positions": 15},
        "event_appearances_summary": {"num_event_appearances": 20},
        "ipqwery_summary": {
            "ipqwery_num_patent_granted": 5,
            "ipqwery_num_trademark_registered": 3,
            "ipqwery_popular_trademark_class": "Mocked Class",
        },
        "overview_timeline": {"count": 30, "entities": []},
        "semrush_summary": {
            "semrush_global_rank": 1000,
            "semrush_visits_latest_month": 50000,
        },
        "semrush_rank_headline": {"semrush_visits_mom_pct": 10},
        "siftery_summary": {"siftery_num_products": 8},
        "social_fields": {"twitter": {"value": "https://twitter.com/mockedcompany"}},
        "growth_insight_description": {},
    }

    # Configure mocks
    mock_client.actor.return_value.call.return_value = mock_run_result
    mock_client.dataset.return_value.iterate_items.return_value = [mock_item]

    # Run the method
    results = mock_crunchbase_client.get_company_details(
        ["https://www.crunchbase.com/organization/test"]
    )

    # Assert the results
    assert (
        results.name == "Mocked Company"
    )  # Adjust this based on your CompanyModel fields
    assert results.founded_on == datetime.strptime(
        "2022-01-20", "%Y-%m-%d"
    )  # Adjust the date format


@patch("parma_mining.crunchbase.client.ApifyClient")
def test_get_organization_details_exception(mock_apify_client, mock_crunchbase_client):
    exception_instance = CrawlingError("Error fetching company details!")
    mock_apify_client.side_effect = exception_instance
    with pytest.raises(CrawlingError):
        mock_crunchbase_client.get_company_details(
            ["https://www.crunchbase.com/organization/exceptional_test"]
        )
