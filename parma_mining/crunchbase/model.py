"""Model for the Crunchbase data."""
import json
from datetime import datetime

from pydantic import BaseModel


class AcquisitionModel(BaseModel):  # done
    """Acquisition model for Crunchbase data."""

    title: str | None
    permalink: str | None
    price_usd: int | None
    date: datetime | None


class AcquireeModel(BaseModel):  # done
    """Acquiree model for Crunchbase data."""

    name: str
    permalink: str | None
    acquisition: AcquisitionModel | None


class AcquirerModel(BaseModel):  # done
    """Acquirer model for Crunchbase data."""

    name: str
    permalink: str | None
    acquisition: AcquisitionModel | None


class ActivityModel(BaseModel):  # done
    """Activity model for Crunchbase data."""

    title: str | None
    activity_type: str | None
    author: str | None
    publisher: str | None
    date: datetime | None
    url: str | None


class EventModel(BaseModel):  # done
    """Event model for Crunchbase data."""

    name: str | None
    permalink: str | None
    interaction_type: str | None


class PersonModel(BaseModel):  # done
    """Person model for Crunchbase data."""

    name: str | None
    job_titles: list[str] | None
    permalink: str | None
    email: str | None
    phone: str | None
    linkedin: str | None


class InvestorModel(BaseModel):  # done
    """Investor model for Crunchbase data."""

    name: str | None
    investment_title: str | None
    permalink: str | None
    partners: list[PersonModel] | None


class FundingRoundModel(BaseModel):  # done
    """Funding model for Crunchbase data."""

    name: str | None
    permalink: str | None
    announced_on: datetime | None
    money_raised_usd: int | None
    num_investors: int | None
    lead_investors: list[InvestorModel] | None


class ProductModel(BaseModel):
    """Product model for Crunchbase data."""

    name: str | None
    created_at: datetime | None


class SimilarCompanyModel(BaseModel):  # done
    """Similar Company model for Crunchbase data."""

    name: str | None
    permalink: str | None
    description: str | None


class TechnologyModel(BaseModel):  # done
    """Technology model for Crunchbase data."""

    name: str
    category: str | None
    num_of_company_using: int | None


class WebsiteDataModel(BaseModel):
    """Website data model for Crunchbase data."""

    visits_pct: float | None
    rank_mom_pct: float | None
    rank: int | None
    location: str | None


class CompanyModel(BaseModel):
    """Company model for Crunchbase data."""

    # general data
    name: str | None
    description: str | None
    permalink: str | None
    website: str | None
    ipo_status: str | None
    company_type: str | None
    founded_on: datetime | None
    categories: list[str] | None
    legal_name: str | None

    # location data
    location_city: str | None
    location_region: str | None
    location_country: str | None

    # employee and contact data
    num_employees_enum: str | None
    rank_org_company: int | None

    # financial data
    funding_rounds: list[FundingRoundModel] | None
    total_funding_usd: int | None
    last_funding_type: str | None
    last_funding_at: datetime | None
    num_funding_rounds: int | None
    investors: list[InvestorModel] | None
    num_investors: int | None

    # acquisition data
    acquirers: list[AcquirerModel] | None
    num_acquirers: int | None
    acquirees: list[AcquireeModel] | None
    num_acquirees: int | None

    # technology stats by builtwith
    technologies: list[TechnologyModel] | None
    num_technologies: int | None

    # app data by apptopia
    apptopa_total_apps: int | None
    apptopia_total_downloads: int | None

    # contact data
    email: str | None
    phone: str | None
    num_contact_email: int | None
    num_contact_phone: int | None
    num_contact: int | None
    contacts: list[PersonModel] | None

    # similar company data
    similar_companies: list[SimilarCompanyModel] | None
    num_similar_companies: int | None

    # employee data
    employees: list[PersonModel] | None
    num_current_positions: int | None

    # event data
    num_event_appearances: int | None
    events: list[EventModel] | None

    # patent and trademark data by ipqwery
    num_patents: int | None
    num_trademarks: int | None
    popular_trademark_classes: str | None

    # activity news data
    activities: list[ActivityModel] | None
    num_activity: int | None

    # website stats by semrush
    semrush_rank: int | None
    semrush_visits_last_month: int | None
    semrush_visits_mom_pct: float | None
    country_data: list[WebsiteDataModel] | None

    # social media data
    social_media: dict[str, str] | None

    # extra data
    growth_insight: str | None
    sifter_num_products: int | None

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

    handles: list[str] = []


class FinalDiscoveryResponse(BaseModel):
    """Define the final discovery response model."""

    identifiers: dict[str, DiscoveryResponse]
    validity: datetime


class CompaniesRequest(BaseModel):
    """Companies request model for Crunchbase data."""

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
