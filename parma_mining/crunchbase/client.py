"""Module for fetching data from Crunchbase using Apify and Google search.

This module communicates with the Apify and Google to discover and scrape
"""
import os

from apify_client import ApifyClient
from dotenv import load_dotenv
from fastapi import HTTPException, status
from googlesearch import search

from parma_mining.crunchbase.model import CompanyModel, DiscoveryModel


class CrunchbaseClient:
    """Class for fetching data from Crunchbase using Apify and Google search."""

    def __init__(self):
        """Initialize the CrunchbaseClient class."""
        load_dotenv()
        self.key = str(os.getenv("APIFY_API_KEY") or "")
        self.actor_id = str(os.getenv("APIFY_ACTOR_ID") or "")

    def discover_company(self, query: str):  # -> list[DiscoveryModel]:
        """Discover a company.

        Take name as an input and find its crunchbase url.
        """
        search_query = query + " crunchbase"
        profile_url = ""
        preferred_slash_count = 4
        try:
            for search_item in search(
                search_query, tld="co.in", num=10, stop=10, pause=2
            ):
                # should be like https://www.crunchbase.com/organization/company-id ,
                # should not be more after company id
                if (
                    search_item.count("/") == preferred_slash_count
                    and "https://www.crunchbase.com/organization/" in search_item
                ):
                    profile_url = search_item
                    return [
                        DiscoveryModel.model_validate(
                            {"name": query, "url": profile_url}
                        )
                    ]
                else:
                    raise Exception("No Crunchbase profile url found with given query")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error searching organizations",
            )

    def get_company_details(self, urls: list[str]) -> list[CompanyModel]:
        """Scrape a company for details."""
        # Initialize the ApifyClient with your API token
        client = ApifyClient(self.key)
        print(urls)

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
