# /app/src/tools/doc_search.py
import logging

# Primary Components
from llama_index import ServiceContext, VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from src.utils.config import load_config, setup_environment_variables
from src.utils.embedding_selector import EmbeddingConfig, EmbeddingSelector

logger = logging.getLogger(__name__)


class DocumentSearch:
    """
    Class to perform document searches using a vector store index.

    Attributes:
    - collection (str): Name of the collection to be queried.
    - query (str): User input query for searching documents.
    - CONFIG (dict): Loaded configuration settings.
    - client (QdrantClient): Client to interact with the Qdrant service.
    """

    def __init__(self, query: str, collection: str):
        """
        Initializes with collection name and user input.

        Parameters:
        - collection (str): Name of the collection to be queried.
        - query (str): User input query for searching documents.
        """
        self.collection = collection
        self.query = query
        self.CONFIG = load_config()
        setup_environment_variables(self.CONFIG)
        self.client = QdrantClient(url="http://VC_ASSISTANT_QDRANT:6333")
        # self.embed_model = OpenAIEmbedding()
        # self.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1")
        self.embedding_config = EmbeddingConfig(type=self.CONFIG["Embedding_Type"])
        self.embed_model = EmbeddingSelector(
            self.embedding_config
        ).get_embedding_model()

    def setup_index(self) -> VectorStoreIndex:
        """
        Sets up and returns the vector store index for the collection.

        Returns:
        - VectorStoreIndex: The set up vector store index.

        Raises:
        - Exception: Propagates any exceptions that occur during the index setup.
        """
        try:
            vector_store = QdrantVectorStore(
                client=self.client, collection_name=self.collection
            )
            service_context = ServiceContext.from_defaults(embed_model=self.embed_model)
            index = VectorStoreIndex.from_vector_store(
                vector_store=vector_store, service_context=service_context
            )

            return index

        except Exception as e:
            logging.error(f"setup_index: Error - {str(e)}")
            raise e

    def search_documents(self):
        """
        Searches and returns documents based on the user input query.

        Returns:
        - Any: The response received from querying the index.

        Raises:
        - Exception: Propagates any exceptions that occur during the document search.
        """
        try:
            query_engine = (self.setup_index()).as_query_engine()
            response = query_engine.query(self.query)
            logging.info(f"search_documents: Response - {response}")

            return response

        except Exception as e:
            logging.error(f"search_documents: Error - {str(e)}")
            raise e
