import logging
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import Settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class DocumentProcessor:
    def __init__(self):
        try:
            logger.info(f"Loading embeddings model: {Settings.EMBEDDING_MODEL}")

            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name = Settings.EMBEDDING_MODEL,
                model_kwargs = {"trust_remote_code": True}
            )
            
            # Initialize text Semantic splitter
            self.text_splitter = SemanticChunker(
                embeddings = self.embeddings,
                breakpoint_threshold_type = "percentile"
            )
            logger.info("DocumentProcessor initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing DocumentProcessor")
            raise e

    def process_pdf(self, file_path:str):
        try:
            logger.info(f"Processing file: {file_path}")
            
            # Read PDF
            loader = PyPDFLoader(file_path)
            raw_documents = loader.load()
            logger.info(f"Loaded {len(raw_documents)} pages from PDF.")
            
            # Split text
            chunks = self.text_splitter.split_documents(raw_documents)
            logger.info(f"Created {len(chunks)} semantic chunks.")
            
            return chunks

        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise e

    def process_documents(self, directory_path: str):
        try:
            import os
            logger.info(f"Processing documents from {directory_path}")
            
            if not os.path.exists(directory_path):
                logger.warning(f"Directory {directory_path} does not exist.")
                return []
            
            pdf_files = [f for f in os.listdir(directory_path) if f.endswith('.pdf')]
            
            all_chunks = []
            for pdf_file in pdf_files:
                file_path = os.path.join(directory_path, pdf_file)
                chunks = self.process_pdf(file_path)
                for chunk in chunks:
                    chunk.metadata['source'] = pdf_file
                all_chunks.extend(chunks)
            
            return all_chunks
            
        except Exception as e:
            logger.error(f"Error processing documents directory: {str(e)}")
            raise e