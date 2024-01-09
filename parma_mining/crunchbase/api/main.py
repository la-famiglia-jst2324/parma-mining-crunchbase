"""Main entrypoint for the API routes in of parma-analytics."""

from fastapi import FastAPI, status

from parma_mining.crunchbase.client import CrunchbaseClient
from parma_mining.crunchbase.model import DiscoveryModel

app = FastAPI()
crunchbase_client = CrunchbaseClient()


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-crunchbase"}


@app.get(
    "/discover",
    response_model=list[DiscoveryModel],
    status_code=status.HTTP_200_OK,
)
def search_organizations(query: str):
    """Discover a company."""
    return crunchbase_client.discover_company(query)
