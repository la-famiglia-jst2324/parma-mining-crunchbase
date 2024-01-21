from unittest.mock import patch

import httpx
import pytest

from parma_mining.crunchbase.analytics_client import AnalyticsClient
from parma_mining.crunchbase.model import (
    CompanyModel,
    ResponseModel,
)
from parma_mining.mining_common.const import HTTP_200, HTTP_500

TOKEN = "mocked_token"


@pytest.fixture
def analytics_client():
    return AnalyticsClient()


@pytest.fixture
def mock_organization_model():
    mock_company_data = {
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
        "funding_rounds": [
            {
                "name": "Series A",
                "permalink": "series-a",
                "announced_on": "2021-01-01T00:00:00",
                "money_raised_usd": 1000000,
                "num_investors": 5,
                "lead_investors": [
                    {
                        "name": "Investor1",
                        "investment_title": "Lead Investor",
                        "permalink": "investor1",
                    }
                ],
            }
        ],
        "total_funding_usd": 10000000,
        "last_funding_type": "Series B",
        "last_funding_at": "2022-01-01T00:00:00",
        "num_funding_rounds": 3,
        "investors": [
            {
                "name": "Investor3",
                "investment_title": "Investor",
                "permalink": "investor3",
                "partners": [
                    {"name": "Partner1", "title": "Partner", "permalink": "partner1"}
                ],
            }
        ],
        "num_investors": 10,
        "acquirer": {
            "name": "AcquirerCompany",
            "permalink": "acquirer-company",
            "acquisition": {
                "title": "Acquisition Title",
                "permalink": "acquisition-title",
                "price_usd": 5000000,
                "date": "2023-01-01T00:00:00",
            },
        },
        "acquirees": [
            {
                "name": "AcquireeCompany1",
                "permalink": "acquiree-company-1",
                "acquisition": {
                    "title": "Acquisition Title 1",
                    "permalink": "acquisition-title-1",
                    "price_usd": 2000000,
                    "date": "2023-02-01T00:00:00",
                },
            }
        ],
        "num_acquirees": 1,
        "num_technologies": 1,
        "apptopa_total_apps": 1,
        "apptopia_total_downloads": 1,
        "email": "info@abc.com",
        "phone": "+123456789",
        "num_contact_email": 1,
        "num_contact_phone": 1,
        "num_contact": 2,
        "similar_companies": [
            {
                "name": "SimilarCompany1",
                "permalink": "similar-company-1",
                "description": "Similar Company 1",
            }
        ],
        "num_similar_companies": 1,
        "featured_employees": [
            {
                "name": "Employee1",
                "title": "Software Engineer",
                "permalink": "employee-1",
                "email": "employee1@abc.com",
                "start_date": "2020-02-01T00:00:00",
                "phone": "+987654321",
                "linkedin": "https://www.linkedin.com/in/employee1/",
            }
        ],
        "num_current_positions": 1,
        "num_event_appearances": 1,
        "events": [
            {"name": "Event1", "permalink": "event-1", "interaction_type": "Conference"}
        ],
        "num_patents": 1,
        "num_trademarks": 1,
        "popular_trademark_class": "Class 1",
        "activities": [
            {
                "title": "News1",
                "activity_type": "Press Release",
                "author": "Author1",
                "publisher": "Publisher1",
                "date": "2023-04-01T00:00:00",
                "url": "https://news1.com",
            }
        ],
        "num_activity": 1,
        "semrush_rank": 1000,
        "semrush_visits_last_month": 100000,
        "semrush_visits_mom_pct": 5.0,
        "country_data": [
            {
                "visits_pct": 80.0,
                "rank_mom_pct": -2.0,
                "rank": 50,
                "location": "Country1",
            }
        ],
        "social_media": {"twitter": "https://twitter.com/abc"},
        "growth_insight": "Steady growth in user base",
        "siftery_num_products": 1,
    }

    return CompanyModel(**mock_company_data)


@pytest.fixture
def mock_response_model(mock_organization_model):
    return ResponseModel(
        source_name="TestSource",
        company_id="TestCompany",
        raw_data=mock_organization_model,
    )


@patch("httpx.post")
def test_send_post_request_success(mock_post, analytics_client):
    mock_post.return_value = httpx.Response(HTTP_200, json={"key": "value"})
    response = analytics_client.send_post_request(
        TOKEN, "http://example.com", {"data": "test"}
    )
    assert response == {"key": "value"}


@patch("httpx.post")
def test_send_post_request_failure(mock_post, analytics_client):
    mock_post.return_value = httpx.Response(HTTP_500, text="Internal Server Error")
    with pytest.raises(Exception) as exc_info:
        analytics_client.send_post_request(
            TOKEN, "http://example.com", {"data": "test"}
        )
    assert "API request failed" in str(exc_info.value)


@patch("httpx.post")
def test_register_measurements(mock_post, analytics_client):
    mock_post.return_value = httpx.Response(HTTP_200, json={"id": "123"})
    mapping = {"Mappings": [{"DataType": "int", "MeasurementName": "test_metric"}]}
    result, updated_mapping = analytics_client.register_measurements(TOKEN, mapping)
    assert "source_measurement_id" in updated_mapping["Mappings"][0]
    assert result[0]["source_measurement_id"] == "123"


@patch("httpx.post")
def test_feed_raw_data(mock_post, analytics_client, mock_response_model):
    mock_post.return_value = httpx.Response(HTTP_200, json={"result": "success"})
    result = analytics_client.feed_raw_data(TOKEN, mock_response_model)
    assert result == {"result": "success"}
