import logging 
import os
import shutil
from typing import List
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import Settings

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name = Settings.EMBEDDING_MODEL,
                model_kwargs = {"trust_remote_code": True}
            )

            self.vector_db = Chroma(
                persist_directory = Settings.CHROMA_PERSIST_DIR,
                embedding_function = self.embeddings,
                collection_name = Settings.COLLECTION_NAME
            )
            logger.info(f"VectorStore connected to {Settings.CHROMA_PERSIST_DIR}")
        
        except Exception as e:
            logger.error(f"Failed to initialize VectorStore: {str(e)}")
            raise e

    def add_documents(self, documents: List[Document]):
        try:
            if not documents:
                logger.warning("No documents provided to add to the VectorStore")
                return

            logger.info(f"Adding {len(documents)} documents to ChromaDB...")
            self.vector_db.add_documents(documents)
            logger.info("Documents added to ChromaDB successfully")

        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise e

    def get_retriever(self, k: int = 5):
        return self.vector_db.as_retriever(
            search_type = "similarity",
            search_kwargs = {"k": k}
        )