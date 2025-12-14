import logging
import time
import os
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from config.settings import Settings
from services.llm_client import LLMClient
from services.vector_store import VectorStore
from services.document_processor import DocumentProcessor
from core.prompts import get_chat_prompt, get_contextualize_prompt

logger = logging.getLogger(__name__)

class RagPipeline:
    def __init__(self):
        try:
            self.llm = LLMClient().get_llm()
            self.vector_store = VectorStore()

            try:
                logger.info("Checking Vector Database integrity...")
                test_retriever = self.vector_store.get_retriever(k=1)
                test_retriever.invoke("test") 
                logger.info("Vector Database is healthy and ready.")
                
            except Exception as e:
                logger.warning(f"Database seems empty or corrupt ({str(e)}). Rebuilding from PDF...")
                
                try:
                    processor = DocumentProcessor()
                    docs = processor.process_documents("./data")
                    
                    if not docs:
                        logger.error("No documents found in ./data folder to ingest!")
                    else:
                        self.vector_store.add_documents(docs)
                        logger.info(f"Successfully rebuilt database with {len(docs)} chunks.")
                except Exception as build_error:
                    logger.error(f"Failed to rebuild database: {str(build_error)}")
            
            self.retriever = self.vector_store.get_retriever(k=5)
            self.prompt = get_chat_prompt()
            self.history_aware_retriever = create_history_aware_retriever(
                self.llm,
                self.retriever,
                get_contextualize_prompt()
            )
            self.question_answer_chain = create_stuff_documents_chain(
                self.llm,
                get_chat_prompt()
            )
            self.rag_chain = create_retrieval_chain(
                self.history_aware_retriever,
                self.question_answer_chain
            )
            logger.info("RAG pipeline initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing RAG pipeline: {str(e)}")
            raise e

    def clear_history(self):
        pass

    def process_query(self, question:str, chat_history: list = []):
        start_time = time.time()
        try:
            logger.info(f"Processing query: {question}")
            langchain_history = []
            for msg in chat_history:
                if msg[0] == "human":
                    langchain_history.append(HumanMessage(content=msg[1]))
                elif msg[0] == "ai":
                    langchain_history.append(AIMessage(content=msg[1]))
            
            response = self.rag_chain.invoke({
                "input": question,
                "chat_history": langchain_history
                })

            latency = time.time() - start_time

            source_files = list(set(
                [doc.metadata.get("source", "Unknown") for doc in response["context"]]
            ))

            return{
                "answer": response["answer"],
                "sources": source_files,
                "latency": latency
            }

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise e