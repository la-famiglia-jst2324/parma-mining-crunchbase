"""Model for the Crunchbase data."""
import json
from datetime import datetime

from pydantic import BaseModel


class AcquisitionModel(BaseModel):  # done
    """Acquisition model for Crunchbase data."""

    title: str | None = None
    permalink: str | None = None
    price_usd: int | None = None
    date: datetime | None = None


class AcquireeModel(BaseModel):  # done
    """Acquiree model for Crunchbase data."""

    name: str | None = None
    permalink: str | None = None
    acquisition: AcquisitionModel | None = None


class AcquirerModel(BaseModel):  # done
    """Acquirer model for Crunchbase data."""

    name: str | None = None
    permalink: str | None = None
    acquisition: AcquisitionModel | None = None


class ActivityModel(BaseModel):  # done
    """Activity model for Crunchbase data."""

    title: str | None = None
    activity_type: str | None = None
    author: str | None = None
    publisher: str | None = None
    date: datetime | None = None
    url: str | None = None


class EventModel(BaseModel):  # done
    """Event model for Crunchbase data."""

    name: str | None = None
    permalink: str | None = None
    interaction_type: str | None = None


class PersonModel(BaseModel):  # done
    """Person model for Crunchbase data."""

    name: str | None = None
    title: str | None = None
    permalink: str | None = None
    email: str | None = None
    start_date: datetime | None = None
    phone: str | None = None
    linkedin: str | None = None


class InvestorModel(BaseModel):  # done
    """Investor model for Crunchbase data."""

    name: str | None = None
    investment_title: str | None = None
    permalink: str | None = None
    partners: list[PersonModel] | None = None


class FundingRoundModel(BaseModel):  # done
    """Funding model for Crunchbase data."""

    name: str | None = None
    permalink: str | None = None
    announced_on: datetime | None = None
    money_raised_usd: int | None = None
    num_investors: int | None = None
    lead_investors: list[InvestorModel] | None = None


class ProductModel(BaseModel):
    """Product model for Crunchbase data."""

    name: str | None = None
    created_at: datetime | None = None


class SimilarCompanyModel(BaseModel):  # done
    """Similar Company model for Crunchbase data."""

    name: str | None = None
    permalink: str | None = None
    description: str | None = None


class WebsiteDataModel(BaseModel):
    """Website data model for Crunchbase data."""

    visits_pct: float | None = None
    rank_mom_pct: float | None = None
    rank: int | None = None
    location: str | None = None


class CompanyModel(BaseModel):
    """Company model for Crunchbase data."""

    # general data
    name: str | None = None
    description: str | None = None
    permalink: str | None = None
    website: str | None = None
    ipo_status: str | None = None
    company_type: str | None = None
    founded_on: datetime | None = None
    categories: list[str] | None = None
    legal_name: str | None = None

    # location data
    location: dict[str, str] | None = None

    # employee and contact data
    num_employees_enum: str | None = None
    rank_org_company: int | None = None

    # financial data
    funding_rounds: list[FundingRoundModel] | None = None
    total_funding_usd: int | None = None
    last_funding_type: str | None = None
    last_funding_at: datetime | None = None
    num_funding_rounds: int | None = None
    investors: list[InvestorModel] | None = None
    num_investors: int | None = None

    # acquisition data
    acquirer: AcquirerModel | None = None
    acquirees: list[AcquireeModel] | None = None
    num_acquirees: int | None = None

    # technology stats by builtwith
    num_technologies: int | None = None

    # app data by apptopia
    apptopa_total_apps: int | None = None
    apptopia_total_downloads: int | None = None

    # contact data
    email: str | None = None
    phone: str | None = None
    num_contact_email: int | None = None
    num_contact_phone: int | None = None
    num_contact: int | None = None

    # similar company data
    similar_companies: list[SimilarCompanyModel] | None = None
    num_similar_companies: int | None = None
    # employee data
    featured_employees: list[PersonModel] | None = None
    num_current_positions: int | None = None

    # event data
    num_event_appearances: int | None = None
    events: list[EventModel] | None = None

    # patent and trademark data by ipqwery
    num_patents: int | None = None
    num_trademarks: int | None = None
    popular_trademark_class: str | None = None

    # activity news data
    activities: list[ActivityModel] | None = None
    num_activity: int | None = None

    # website stats by semrush
    semrush_rank: int | None = None
    semrush_visits_last_month: int | None = None
    semrush_visits_mom_pct: float | None = None
    country_data: list[WebsiteDataModel] | None = None

    # social media data
    social_media: dict[str, str] | None = None

    # extra data
    growth_insight: str | None = None
    siftery_num_products: int | None = None

    def updated_model_dump(self) -> str:
        """Dump the CompanyModel instance to a JSON string."""
        # Convert datetime objects to string representation
        json_serializable_dict = self.model_dump()
        # nested fields will be added
        return json.dumps(json_serializable_dict, default=str)


class DiscoveryRequest(BaseModel):
    """Request model for the discovery endpoint."""

    company_id: str
    name: str


class DiscoveryResponse(BaseModel):
    """Define the output model for the discovery endpoint."""

    urls: list[str] = []


class FinalDiscoveryResponse(BaseModel):
    """Define the final discovery response model."""

    identifiers: dict[str, DiscoveryResponse]
    validity: datetime


class CompaniesRequest(BaseModel):
    """Base model for the companies request."""

    task_id: int
    companies: dict[str, dict[str, list[str]]]


class ResponseModel(BaseModel):
    """Response model for Crunchbase data."""

    source_name: str
    company_id: str
    raw_data: CompanyModel


class ErrorInfoModel(BaseModel):
    """Error info for the crawling_finished endpoint."""

    error_type: str
    error_description: str | None


class CrawlingFinishedInputModel(BaseModel):
    """Internal base model for the crawling_finished endpoints."""

    task_id: int
    errors: dict[str, ErrorInfoModel] | None = None
