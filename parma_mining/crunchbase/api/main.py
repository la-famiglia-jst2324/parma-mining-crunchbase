"""Main entrypoint for the API routes in of parma-analytics."""
import logging

from fastapi import FastAPI, status

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint for the API."""
    logger.debug("Root endpoint called")
    return {"welcome": "at parma-mining-crunchbase"}
