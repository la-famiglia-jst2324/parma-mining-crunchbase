"""Module for fetching data from Crunchbase using Apify and Google search.

This module communicates with the Apify and Google to discover and scrape
"""
import logging
import os

from apify_client import ApifyClient
from dotenv import load_dotenv
from googlesearch import search

from parma_mining.crunchbase.model import (
    CompanyModel,
    DiscoveryResponse,
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

    def get_company_details(self, urls: list[str]) -> list[CompanyModel]:
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
        run = client.actor(self.actor_id).call(run_input=run_input)

        # Get output of the Actor run
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            pass
        # cannot continue right now, will be able when we have access to Apify actor
        return []
