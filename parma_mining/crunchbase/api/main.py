"""Main entrypoint for the API routes in of parma-analytics."""
import json
import logging
import os
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, status

from parma_mining.crunchbase.analytics_client import AnalyticsClient
from parma_mining.crunchbase.api.dependencies.auth import authenticate
from parma_mining.crunchbase.client import CrunchbaseClient
from parma_mining.crunchbase.model import (
    CompaniesRequest,
    DiscoveryRequest,
    FinalDiscoveryResponse,
)
from parma_mining.crunchbase.normalization_map import CrunchbaseNormalizationMap
from parma_mining.mining_common.exceptions import (
    ClientInvalidBodyError,
)

env = os.getenv("DEPLOYMENT_ENV", "local")

if env == "prod":
    logging.basicConfig(level=logging.INFO)
elif env in ["staging", "local"]:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.warning(f"Unknown environment '{env}'. Defaulting to INFO level.")
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()
crunchbase_client = CrunchbaseClient()
analytics_client = AnalyticsClient()
normalization = CrunchbaseNormalizationMap()


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


@app.get("/initialize", status_code=status.HTTP_200_OK)
def initialize(source_id: int, token: str = Depends(authenticate)) -> str:
    """Initialization endpoint for the API."""
    # init frequency
    time = "weekly"
    normalization_map = CrunchbaseNormalizationMap().get_normalization_map()
    # register the measurements to analytics
    analytics_client.register_measurements(
        token=token, mapping=normalization_map, source_module_id=source_id
    )

    # set and return results
    results = {}
    results["frequency"] = time
    results["normalization_map"] = str(normalization_map)
    return json.dumps(results)


@app.post(
    "/discover",
    response_model=FinalDiscoveryResponse,
    status_code=status.HTTP_200_OK,
)
def discover_companies(
    request: list[DiscoveryRequest], token: str = Depends(authenticate)
):
    """Endpoint to discover organizations based on provided names."""
    if not request:
        msg = "Request body cannot be empty for discovery"
        logger.error(msg)
        raise ClientInvalidBodyError(msg)

    response_data = {}
    for company in request:
        logger.debug(
            f"Discovering with name: {company.name} for company_id {company.company_id}"
        )
        response = crunchbase_client.discover_company(company.name)
        response_data[company.company_id] = response

    current_date = datetime.now()
    valid_until = current_date + timedelta(days=180)

    return FinalDiscoveryResponse(identifiers=response_data, validity=valid_until)


@app.post(
    "/companies",
    status_code=status.HTTP_200_OK,
)
def get_company_info(companies: CompaniesRequest, token: str = Depends(authenticate)):
    """Run the actor and fetch the data, send it to analytics."""
    company_urls = []
    for company in companies.companies:
        # iterate all input items and find a crunchbase url
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
