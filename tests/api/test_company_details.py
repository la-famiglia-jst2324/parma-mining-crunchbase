import logging
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from parma_mining.crunchbase.api.dependencies.auth import authenticate
from parma_mining.crunchbase.api.main import app
from parma_mining.mining_common.const import HTTP_200, HTTP_404
from tests.dependencies.mock_auth import mock_authenticate


@pytest.fixture
def client():
    assert app
    app.dependency_overrides.update(
        {
            authenticate: mock_authenticate,
        }
    )
    return TestClient(app)


logger = logging.getLogger(__name__)


@pytest.fixture
def mock_crunchbase_client(mocker) -> MagicMock:
    """Mocking the CrunchbaseClient's method to avoid actual API calls."""
    mock = mocker.patch(
        "parma_mining.crunchbase.api.main.CrunchbaseClient.get_company_details"
    )
    mock.return_value = {
        "name": "ABC Company",
        "description": "A tech company",
        "permalink": "abc-company",
        "website": "https://www.abc.com",
        "ipo_status": "Public",
        "company_type": "Technology",
        "founded_on": "2020-01-01T00:00:00",
        "categories": ["Technology", "Software"],
        "legal_name": "ABC Tech Inc",
        "location": {"city": "Cityville", "country": "Countryland"},
        "num_employees_enum": "100-500",
        "rank_org_company": 1,
        "funding_rounds": [],
        "total_funding_usd": 10000000,
        "last_funding_type": "Series B",
        "last_funding_at": "2022-01-01T00:00:00",
        "num_funding_rounds": 0,
        "investors": [],
        "num_investors": 0,
        "acquirer": None,
        "acquirees": [],
        "num_acquirees": 0,
        "num_technologies": 1,
        "apptopa_total_apps": 1,
        "apptopia_total_downloads": 1,
        "email": "info@abc.com",
        "phone": "+123456789",
        "num_contact_email": 1,
        "num_contact_phone": 1,
        "num_contact": 2,
        "similar_companies": [],
        "num_similar_companies": 0,
        "featured_employees": [],
        "num_current_positions": 0,
        "num_event_appearances": 0,
        "events": [],
        "num_patents": 1,
        "num_trademarks": 1,
        "popular_trademark_class": "Class 1",
        "activities": [],
        "num_activity": 1,
        "semrush_rank": 1000,
        "semrush_visits_last_month": 100000,
        "semrush_visits_mom_pct": 5.0,
        "country_data": [],
        "social_media": {"twitter": "https://twitter.com/abc"},
        "growth_insight": "Steady growth in user base",
        "siftery_num_products": 1,
    }

    return mock


@pytest.fixture
def mock_analytics_client(mocker) -> MagicMock:
    """Mocking the AnalyticClient's method to avoid actual API calls during testing."""
    mock = mocker.patch(
        "parma_mining.crunchbase.api.main.AnalyticsClient.feed_raw_data"
    )
    mock = mocker.patch(
        "parma_mining.crunchbase.api.main.AnalyticsClient.crawling_finished"
    )
    # No return value needed, but you can add side effects or exceptions if necessary
    return mock


def test_get_company_details(
    mock_crunchbase_client: MagicMock,
    mock_analytics_client: MagicMock,
    client: TestClient,
):
    payload = {
        "task_id": 123,
        "companies": {
            "Example_id1": {
                "url": ["https://www.crunchbase.com/organization/finto-acba"]
            },
            "Example_id2": {
                "url": ["https://www.crunchbase.com/organization/personio"]
            },
        },
    }

    headers = {"Authorization": "Bearer test"}
    response = client.post("/companies", json=payload, headers=headers)

    mock_analytics_client.assert_called()

    assert response.status_code == HTTP_200


def test_get_company_details_bad_request(mocker, client: TestClient):
    mocker.patch(
        "parma_mining.crunchbase.api.main.CrunchbaseClient.get_company_details",
        side_effect=HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
        ),
    )

    payload = {
        "task_id": 123,
        "companies": {
            "Example_id1": {
                "url": ["https://www.crunchbase.com/organization/finto-acba"]
            },
            "Example_id2": {
                "url": ["https://www.crunchbase.com/organization/personio"]
            },
        },
    }

    headers = {"Authorization": "Bearer test"}
    response = client.post("/companies", json=payload, headers=headers)
    assert response.status_code == HTTP_404
