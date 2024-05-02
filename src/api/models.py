# /app/src/api/models.py
import logging
from typing import Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

from typing import List, Dict


class VCExtractionRequest(BaseModel):
    query: str
    collection: str


class VCExtractionResponse(BaseModel):
    vc_name: str
    contacts: List[str]
    industries: List[str]
    investment_rounds: List[str]


class OptimizerConfig(BaseModel):
    max_optimization_threads: int = Field(default=1, ge=1)


# === Chat Models ===
class ChatInput(BaseModel):
    """
    Model representing the user input for chat interactions.

    Attributes:
    user_input (str): The input string from the user to the chat.
    """

    user_input: str = (
        "You should extract the following infromation and show in json for each company separatly and accuratly and completely: Company Name, contact info and email, industries that the company invest, Investment Rounds in participate/lead"
    )


class ChatOutput(BaseModel):
    """
    Model representing the response from the chat agent.

    Attributes:
    response (str): The response string from the chat agent to the user.
    """

    response: str


# === Web Scraper Models ===
class ScrapeRequest(BaseModel):
    """
    Model representing the request to initiate web scraping.

    Attributes:
    url (str): The URL of the web page to be scraped.
    """

    # optimizer_config: OptimizerConfig
    url: str = "http://www.a16z.com/"


class ScrapeResponse(BaseModel):
    """
    Model representing the response from the web scraping process.

    Attributes:
    message (str): The status message indicating the success or failure
                   of the scraping process.
    data (Optional[str]): The scraped data from the web page if the
                          scraping process is successful. None, if unsuccessful.
    """

    # optimizer_config: OptimizerConfig
    message: str
    data: Optional[str]


# === Document Loader Models ===
class DocumentLoaderResponse(BaseModel):
    """
    Model representing the response from the document loading process.

    Attributes:
    status (str): The status of the document loading process.
                  It will be 'success' if the documents are processed successfully.
    message (Optional[str]): Optional message field to convey any additional
                             information or details about the process.
    """

    # optimizer_config: OptimizerConfig
    status: str
    message: Optional[str]


class DocumentLoaderRequest(BaseModel):
    """
    Model representing the request to initiate document loading.

    Attributes:
    source_dir (str): The directory from where the documents are to be loaded.
                      Default is set to the directory where scraped data is stored.
    collection (str): The name of the collection to which the documents
                           should be loaded. Default is "default".
    """

    source_dir: str = "/app/src/scraper/scraped_data"
    collection: str = "default"


# === Document Search Models ===
class DocumentSearchRequest(BaseModel):
    """
    Model representing the request to initiate document search.

    Attributes:
    collection (str): "default"
    user_input (str): "You should extract the following infromation and show in json for each company separatly and accuratly and completely: Company Name, contact info and email, industries that the company invest, Investment Rounds in participate/lead"
    """

    # optimizer_config: OptimizerConfig
    collection: str = "default"
    user_input: str = (
        "You should extract the following infromation and show in json for each Venture Capital firms separatly, accuratly and completely: Venture Capital firms company Name, Venture Capital contact info, industries that the Venture Capital invest, Investment Rounds in participate/lead"
    )


# === Document Search Models ===
class DocumentSimilarityRequest(BaseModel):
    """
    Model representing the request to similarity search.

    Attributes:
    collection (str): "default"
    user_input (str): "You should extract the simlar infromation and show in json for each company separatly and accuratly and completely: Company Name, contact info and email, industries that the company invest, Investment Rounds in participate/lead"
    """

    collection: str = "default"
    user_input: str = (
        "You should extract the three similar infromation in [Company Name], [contact info and email], [industries that the company invest], [Investment Rounds in participate/lea]"
    )
