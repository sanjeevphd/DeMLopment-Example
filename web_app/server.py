from http import HTTPStatus
from typing import Dict

from fastapi import FastAPI

# The API
server = FastAPI(
    title="Written Text Recognizer",
    description="Identify character from handwritten image.",
    version="0.1",
)


# The root endpoint
@server.get("/")
def _index() -> Dict:
    """Health check."""
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {},
    }
    return response
