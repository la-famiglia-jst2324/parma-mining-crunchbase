"""Main entrypoint for the API routes in of parma-analytics."""
import logging
import os

from fastapi import Depends, FastAPI, status

from parma_mining.crunchbase.api.dependencies.auth import authenticate

env = os.getenv("DEPLOYMENT_ENV", "local")

if env == "prod":
    logging.basicConfig(level=logging.INFO)
elif env in ["staging", "local"]:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.warning(f"Unknown environment '{env}'. Defaulting to INFO level.")
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

from parma_mining.crunchbase.client import CrunchbaseClient
from parma_mining.crunchbase.model import CompaniesRequest, DiscoveryModel

app = FastAPI()
crunchbase_client = CrunchbaseClient()


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint for the API."""
    logger.debug("Root endpoint called")
    return {"welcome": "at parma-mining-crunchbase"}


@app.get("/dummy-auth", status_code=status.HTTP_200_OK)
def dummy_auth(token: str = Depends(authenticate)):
    """Dummy endpoint.

    This endpoint is used to demonstrate the usage of authenticate function. This
    function ensures that the incoming request comes from the analytics. token variable
    can be used to make requests to analytics.
    """
    logger.debug("Dummy endpoint called")
    return {"welcome": "at parma-mining-crunchbase"}


@app.get(
    "/discover",
    response_model=list[DiscoveryModel],
    status_code=status.HTTP_200_OK,
)
def search_organizations(query: str):
    """Discover a company."""
    return crunchbase_client.discover_company(query)


@app.post(
    "/companies",
    status_code=status.HTTP_200_OK,
)
def get_company_info(companies: CompaniesRequest):
    """Run the actor and fetch the data, send it to analytics."""
    company_urls = []
    for company in companies.companies:
        # iterate all input items and find a linkedin url
        url_exist = False
        for field in companies.companies[company]:
            for url in companies.companies[company][field]:
                if "crunchbase.com/" in url:
                    url_exist = True
                    company_urls.append(url)
                    break
        if not url_exist:
            raise Exception("No Crunchbase url found for the company")
    # launch the company scraper actor
    crunchbase_client.get_company_details(company_urls)

    return "done"
