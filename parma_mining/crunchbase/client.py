"""Module for fetching data from Crunchbase using Apify and Google search.

This module communicates with the Apify and Google to discover and scrape
"""
import logging
import os
from datetime import datetime

from apify_client import ApifyClient
from dotenv import load_dotenv
from googlesearch import search

from parma_mining.crunchbase.model import (
    AcquireeModel,
    AcquirerModel,
    AcquisitionModel,
    ActivityModel,
    CompanyModel,
    DiscoveryResponse,
    EventModel,
    FundingRoundModel,
    InvestorModel,
    PersonModel,
    SimilarCompanyModel,
    WebsiteDataModel,
)
from parma_mining.mining_common.exceptions import ClientError

logger = logging.getLogger(__name__)


class CrunchbaseClient:
    """Class for fetching data from Crunchbase using Apify and Google search."""

    def __init__(self):
        """Initialize the CrunchbaseClient class."""
        load_dotenv()
        self.key = str(os.getenv("APIFY_API_KEY") or "")
        self.actor_id = str(os.getenv("APIFY_ACTOR_ID") or "")

    def discover_company(self, query: str) -> DiscoveryResponse:
        """Discover a company.

        Take name as an input and find its crunchbase url.
        """
        search_query = query + " crunchbase"
        preferred_slash_count = 4
        handles = []
        try:
            for search_item in search(
                search_query, tld="co.in", num=10, stop=10, pause=2
            ):
                if (
                    search_item.count("/") == preferred_slash_count
                    and "https://www.crunchbase.com/organization/" in search_item
                ):
                    handles.append(search_item)
            if len(handles) == 0:
                raise Exception("No Crunchbase profile url found with given query")
            return DiscoveryResponse.model_validate({"handles": handles})
        except Exception as e:
            msg = f"Error searching organizations for {query}: {e}"
            logger.error(msg)
            raise ClientError()

    def get_company_details(self, urls: list[str]) -> CompanyModel:
        """Scrape a company for details."""
        # Initialize the ApifyClient with your API token
        client = ApifyClient(self.key)
        # Prepare the Actor input
        run_input = {
            "action": "scrapeCompanyUrls",
            "cursor": "",
            "minDelay": 1,
            "maxDelay": 3,
            "scrapeCompanyUrls.urls": urls,
            "proxy": {
                "useApifyProxy": True,
                "apifyProxyGroups": ["RESIDENTIAL"],
            },
        }

        # Run the Actor and wait for it to finish
        try:
            run = client.actor(self.actor_id).call(run_input=run_input)

            # Get output of the Actor run
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                company = {
                    "name": item["identifier"]["value"],
                    "description": item["short_description"],
                    "permalink": item["identifier"]["permalink"],
                    "website": item["website"]["value"],
                    "ipo_status": item["ipo_status"],
                    "company_type": item["overview_company_fields"]["company_type"],
                    "founded_on": datetime.strptime(
                        item["overview_fields_extended"]["founded_on"]["value"],
                        "%Y-%m-%d",
                    ),
                    "legal_name": item["overview_fields_extended"]["legal_name"],
                    "num_employees_enum": item["num_employees_enum"],
                    "rank_org_company": item["rank_org_company"],
                    "total_funding_usd": item["funding_total"]["value_usd"],
                    "last_funding_type": item["last_funding_type"],
                    "last_funding_at": datetime.strptime(
                        item["funding_rounds_summary"]["last_funding_at"], "%Y-%m-%d"
                    ),
                    "num_funding_rounds": item["funding_rounds_summary"][
                        "num_funding_rounds"
                    ],
                    "num_investors": item["investors_summary"]["num_investors"],
                    "num_technologies": item["technology_highlights"][
                        "builtwith_num_technologies_used"
                    ],
                    "apptopa_total_apps": item["apptopia_summary"][
                        "apptopia_total_apps"
                    ]
                    if "apptopia_total_apps" in item["apptopia_summary"]
                    else None,
                    "apptopia_total_downloads": item["apptopia_summary"][
                        "apptopia_total_downloads"
                    ]
                    if "apptopia_total_downloads" in item["apptopia_summary"]
                    else None,
                    "email": item["contact_fields"]["contact_email"]
                    if "contact_email" in item["contact_fields"]
                    else None,
                    "phone": item["contact_fields"]["phone_number"]
                    if "phone_number" in item["contact_fields"]
                    else None,
                    "num_similar_companies": item["company_overview_highlights"][
                        "num_org_similarities"
                    ],
                    "num_current_positions": item["people_highlights"][
                        "num_current_positions"
                    ],
                    "num_event_appearances": item["event_appearances_summary"][
                        "num_event_appearances"
                    ]
                    if "num_event_appearances" in item["event_appearances_summary"]
                    else None,
                    "num_patents": item["ipqwery_summary"][
                        "ipqwery_num_patent_granted"
                    ],
                    "num_trademarks": item["ipqwery_summary"][
                        "ipqwery_num_trademark_registered"
                    ],
                    "popular_trademark_class": item["ipqwery_summary"][
                        "ipqwery_popular_trademark_class"
                    ],
                    "num_activity": item["overview_timeline"]["count"],
                    "semrush_rank": item["semrush_summary"]["semrush_global_rank"],
                    "semrush_visits_last_month": item["semrush_summary"][
                        "semrush_visits_latest_month"
                    ],
                    "semrush_visits_mom_pct": item["semrush_rank_headline"][
                        "semrush_visits_mom_pct"
                    ],
                    "siftery_num_products": item["siftery_summary"][
                        "siftery_num_products"
                    ]
                    if "siftery_num_products" in item["siftery_summary"]
                    else None,
                }

            # categories
            company["categories"] = self.extract_categories(item)
            # location
            company["location"] = self.extract_location(item)
            # funding_rounds
            company["funding_rounds"] = self.extract_funding_rounds(item)
            # investors
            company["investors"] = self.extract_investors(item)
            # acquirees
            company["acquirees"] = self.extract_acquirees(item)
            # acquirers
            company["acquirer"] = self.extract_acquirers(item)
            # similar_companies
            company["similar_companies"] = self.extract_similar_companies(item)
            # employees
            company["featured_employees"] = self.extract_featured_employees(item)
            # events
            company["events"] = self.extract_events(item)
            # activities
            company["activities"] = self.extract_activities(item)
            # country_data
            company["country_data"] = self.extract_country_data(item)
            # social_media
            company["social_media"] = self.extract_social_media(item)
            # growth_insight
            company["growth_insight"] = self.extract_growth_insight(item)

            return CompanyModel.model_validate(company)

        except Exception as e:
            logger.error(f"Failed to scrape product page: {e}")
            return CompanyModel()

    def extract_categories(self, item: dict) -> list[str]:
        """Extract categories from the item."""
        categories = []
        category_list = item["overview_fields_extended"]["categories"]
        for category in category_list:
            categories.append(category["value"])
        return categories

    def extract_location(self, item: dict) -> dict:
        """Extract location from the item."""
        location_identifiers = item["location_identifiers"]
        locations = {}
        for location in location_identifiers:
            locations[location["location_type"]] = location["value"]
        return locations

    def extract_funding_rounds(self, item: dict) -> list[FundingRoundModel]:
        """Extract funding rounds from the item."""
        funding_rounds = []
        funding_rounds_list = item["funding_rounds_list"]
        for funding_round in funding_rounds_list:
            result_funding_round = {
                "name": funding_round["identifier"]["value"],
                "permalink": funding_round["identifier"]["permalink"],
                "announced_on": datetime.strptime(
                    funding_round["announced_on"], "%Y-%m-%d"
                ),
                "money_raised_usd": funding_round["money_raised"]["value_usd"]
                if "money_raised" in funding_round
                else None,
                "num_investors": funding_round["num_investors"],
                "lead_investors": list[InvestorModel],
            }
            lead_investors = []
            if "lead_investor_identifiers" not in funding_round:
                continue
            for lead_investor in funding_round["lead_investor_identifiers"]:
                result_lead_investor = {
                    "name": lead_investor["value"],
                    "permalink": lead_investor["permalink"],
                }
                lead_investors.append(
                    InvestorModel.model_validate(result_lead_investor)
                )
            result_funding_round["lead_investors"] = lead_investors
            funding_rounds.append(
                FundingRoundModel.model_validate(result_funding_round)
            )
        return funding_rounds

    def extract_investors(self, item: dict) -> list[InvestorModel]:
        """Extract investors from the item."""
        investors = []
        investors_list = item["investors_list"]
        for investor in investors_list:
            result_investor = {
                "name": investor["investor_identifier"]["value"],
                "investment_title": investor["funding_round_identifier"]["value"],
                "permalink": investor["investor_identifier"]["permalink"],
                "partners": list[PersonModel],
            }
            partners = []
            if "partner_identifiers" not in investor:
                continue
            for partner in investor["partner_identifiers"]:
                result_partner = {
                    "name": partner["value"],
                    "permalink": partner["permalink"],
                }
                partners.append(PersonModel.model_validate(result_partner))
            result_investor["partners"] = partners
            investors.append(InvestorModel.model_validate(result_investor))
        return investors

    def extract_acquirers(self, item: dict) -> AcquirerModel | None:
        """Extract acquirers from the item."""
        if "acquirer_identifier" not in item["acquired_by_fields"]:
            return None
        else:
            acquirer = {
                "name": item["acquired_by_fields"]["acquirer_identifier"]["value"],
                "permalink": item["acquired_by_fields"]["acquirer_identifier"][
                    "permalink"
                ],
            }
            acquisition = {
                "title": item["acquired_by_fields"]["acquisition_identifier"]["value"],
                "permalink": item["acquired_by_fields"]["acquisition_identifier"][
                    "permalink"
                ],
                "date": datetime.strptime(
                    item["acquired_by_fields"]["acquisition_announced_on"]["value"],
                    "%Y-%m-%d",
                )
                if "acquisition_announced_on" in item["acquired_by_fields"]
                else None,
                "price_usd": item["acquired_by_fields"]["acquisition_price"][
                    "value_usd"
                ]
                if "acquisition_price" in item["acquired_by_fields"]
                else None,
            }
            acquirer["acquisition"] = AcquisitionModel.model_validate(acquisition)
            return AcquirerModel.model_validate(acquirer)

    def extract_acquirees(self, item: dict) -> list[AcquireeModel]:
        """Extract acquirees from the item."""
        acquirees = []
        acquirees_list = item["acquisitions_list"]
        for acquiree in acquirees_list:
            result_acquiree = {
                "name": acquiree["acquiree_identifier"]["value"],
                "permalink": acquiree["acquiree_identifier"]["permalink"],
                "acquisition": AcquisitionModel,
            }
            acquisition = {
                "title": acquiree["identifier"]["value"],
                "permalink": acquiree["identifier"]["permalink"],
                "date": datetime.strptime(acquiree["announced_on"], "%Y-%m-%d"),
                "price_usd": acquiree["price"]["value_usd"]
                if "price" in acquiree
                else None,
            }
            result_acquiree["acquisition"] = AcquisitionModel.model_validate(
                acquisition
            )
            acquirees.append(AcquireeModel.model_validate(result_acquiree))
        return acquirees

    def extract_similar_companies(self, item: dict) -> list[SimilarCompanyModel]:
        """Extract similar companies from the item."""
        similar_companies = []
        similar_companies_list = item["org_similarity_list"]
        for similar_company in similar_companies_list:
            result_similar_company = {
                "name": similar_company["source"]["value"],
                "permalink": similar_company["source"]["permalink"],
                "description": similar_company["source_short_description"],
            }
            similar_companies.append(
                SimilarCompanyModel.model_validate(result_similar_company)
            )
        return similar_companies

    def extract_featured_employees(self, item: dict) -> list[PersonModel]:
        """Extract featured employees from the item."""
        featured_employees = []
        featured_employees_list = item["current_employees_featured_order_field"]
        for featured_employee in featured_employees_list:
            result_featured_employee = {
                "name": featured_employee["person_identifier"]["value"],
                "title": featured_employee["title"],
                "permalink": featured_employee["person_identifier"]["permalink"],
                "email": featured_employee["email_address"]
                if "email_address" in featured_employee
                else None,
                "start_date": datetime.strptime(
                    featured_employee["started_on"]["value"], "%Y-%m-%d"
                )
                if "started_on" in featured_employee
                else None,
            }
            featured_employees.append(
                PersonModel.model_validate(result_featured_employee)
            )
        return featured_employees

    def extract_events(self, item: dict) -> list[EventModel]:
        """Extract events from the item."""
        events = []
        events_list = item["event_appearances_list"]
        for event in events_list:
            result_event = {
                "name": event["identifier"]["value"],
                "permalink": event["identifier"]["permalink"],
                "interaction_type": event["appearance_type"]
                if "appearance_type" in event
                else None,
            }
            events.append(EventModel.model_validate(result_event))
        return events

    def extract_activities(self, item: dict) -> list[ActivityModel]:
        """Extract activities from the item."""
        activities = []
        activities_list = item["overview_timeline"]["entities"]
        for activity in activities_list:
            result_activity = {
                "title": activity["properties"]["identifier"]["value"],
                "activity_type": activity["properties"]["identifier"]["entity_def_id"],
                "author": activity["properties"]["activity_properties"]["author"]
                if "author" in activity["properties"]["activity_properties"]
                else None,
                "publisher": activity["properties"]["activity_properties"]["publisher"]
                if "publisher" in activity["properties"]["activity_properties"]
                else None,
                "date": datetime.strptime(
                    activity["properties"]["activity_date"], "%Y-%m-%d"
                )
                if "activity_date" in activity["properties"]["activity_properties"]
                else None,
                "url": activity["properties"]["activity_properties"]["url"]["value"]
                if "url" in activity["properties"]["activity_properties"]
                else None,
            }
            activities.append(ActivityModel.model_validate(result_activity))
        return activities

    def extract_country_data(self, item: dict) -> list[WebsiteDataModel]:
        """Extract country data from the item."""
        country_data = []
        country_data_list = item["semrush_location_list"]
        for location_stats in country_data_list:
            result_country_data = {
                "visits_pct": location_stats["visits_pct"]
                if "visits_pct" in location_stats
                else None,
                "rank_mom_pct": location_stats["rank_mom_pct"]
                if "rank_mom_pct" in location_stats
                else None,
                "rank": location_stats["rank"],
                "location": location_stats["location_identifiers"][0]["value"]
                if len(location_stats["location_identifiers"]) > 0
                else None,
            }
            country_data.append(WebsiteDataModel.model_validate(result_country_data))
        return country_data

    def extract_social_media(self, item: dict) -> dict:
        """Extract social media from the item."""
        social_media = {}
        social_fields = item["social_fields"]
        for social_field in social_fields:
            social_media[str(social_field)] = str(social_fields[social_field]["value"])
        return social_media

    def extract_growth_insight(self, item: dict) -> str | None:
        """Extract growth insight from the item."""
        if "growth_insight_description" in item["growth_insight_description"]:
            return item["growth_insight_description"]["growth_insight_description"]
        return None
