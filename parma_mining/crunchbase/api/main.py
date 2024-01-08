"""Main entrypoint for the API routes in of parma-analytics."""
import logging

from fastapi import Depends, FastAPI, status

from parma_mining.crunchbase.api.dependencies.auth import authenticate

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()


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
