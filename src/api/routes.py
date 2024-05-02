# /app/src/api/routes.py
import logging

from fastapi import APIRouter, HTTPException
from typing import List

from src.agent.agent_handler import get_agent_handler
from src.api.handlers import (
    handle_chat,
    handle_document_search,
    handle_document_similarity,
    handle_process_documents,
    handle_scrape,
)
from src.api.models import (
    ChatInput,
    ChatOutput,
    DocumentLoaderRequest,
    DocumentLoaderResponse,
    DocumentSearchRequest,
    ScrapeRequest,
    ScrapeResponse,
    DocumentSimilarityRequest,
)

logger = logging.getLogger(__name__)


# Initialize the router.
router = APIRouter()


# === Web Scraper Endpoint ===
@router.post("/scraper/", response_model=ScrapeResponse)
async def scrape_endpoint(data: ScrapeRequest):
    """
    Endpoint to initiate the web scraping process.

    This asynchronous function receives a URL, passes it to the scrape handler,
    and returns the result of the scraping process.

    Args:
    data (ScrapeRequest): The data containing the URL to be scraped.

    Returns:
    ScrapeResponse: The result of the scraping process encapsulated in a ScrapeResponse object.
    """
    # Delegate to the scrape handler and return the response.
    return await handle_scrape(data)


# === Document Loader Endpoint ===
@router.post("/process-scrape2vector/", response_model=DocumentLoaderResponse)
def process_documents_endpoint(data: DocumentLoaderRequest) -> DocumentLoaderResponse:
    """
    Endpoint to initiate the document loading process.

    This function receives the source directory and the collection name,
    passes them to the document loader handler, and returns the status of the
    processed files encapsulated in a DocumentLoaderResponse object.

    Args:
    data (DocumentLoaderRequest): The data containing the source directory
                                  and the collection name to which the documents should be loaded.

    Returns:
    DocumentLoaderResponse: A response object containing the status of the document
                            loading process and an optional message.
    """
    return handle_process_documents(data)


# === Document Search Endpoint ===
@router.post("/extract-info2json/", response_model=str)
def search_documents_endpoint(data: DocumentSearchRequest) -> str:
    """
    Endpoint to initiate the document search process.

    Args:
    data (DocumentSearchRequest): The data containing the collection name and user input.

    Returns:
    DocumentSearchResponse: The result of the document search process.
    """
    return handle_document_search(data)


# === Document Similarity Endpoint ===
@router.post("/extract-similarity/", response_model=str)
def search_similarity_endpoint(data: DocumentSimilarityRequest) -> str:
    """
    Endpoint to initiate the document similarity process.

    Args:
    data (DocumentSimilarityRequest): The data containing the collection name and user input.

    Returns:
    DocumentSimilarityResponse: The result of the document Similarity process.
    """
    return handle_document_similarity(data)


# === Chat Endpoint ===
@router.post("/chat/", response_model=ChatOutput)
def chat_endpoint(data: ChatInput):
    """
    Endpoint to interact with the chat agent.

    This function receives user input, passes it to the chat handler,
    and returns the chat agent's response.

    Args:
    data (ChatInput): The user input data encapsulated in a ChatInput object.

    Returns:
    ChatOutput: The response from the chat agent encapsulated in a ChatOutput object.
    """
    # Delegate to the chat handler and return the response.
    agent = get_agent_handler()
    return handle_chat(data, agent)


# {
#   "collection": "techdocs",
#   "user_input": "given the company information of a company in json format, I want you to extract information about the company. You are not allowed to make any assumptions while extracting the information. Every link you provide should be from the information given. There should be no assumptions for Links/URLS. You should not return code to do it.:
#         You should extract the following text infromation from the html and show in json: name,contact: email,invest_industry(industries that the company invest),investment_round(Investment Rounds in participate/lead)"


#         {
#   "collection": "techdocs",
#   "user_input": "You should extract the following infromation and show in json: name of company, contact info(email), invest industry(industries that the company invest), investment round(Investment Rounds in participate/lead)"
# }


# {
#   "collection": "techdocs",
#   "user_input": "You should extract the following infromation and show in json for each company separatly and accuratly and completely: name of company, contact info, industries that the company invest, Investment Rounds in participate/lead"
# }

# {
#   "collection": "a16z",
#   "user_input": "You should extract the following infromation and show in json for each company separatly and accuratly and completely: Company Name, contact info and email, industries that the company invest, Investment Rounds in participate/lead"
# }
