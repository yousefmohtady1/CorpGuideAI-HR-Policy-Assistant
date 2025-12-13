import logging
import time
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from config.settings import Settings
from services.llm_client import LLMClient
from services.vector_store import VectorStore
from core.prompts import get_chat_prompt, get_contextualize_prompt

logger = logging.getLogger(__name__)

class RagPipeline:
    def __init__(self):
        try:
            self.llm = LLMClient().get_llm()
            self.vector_store = VectorStore()
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
            self.chat_history = []
            logger.info("RAG pipeline initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing RAG pipeline: {str(e)}")
            raise e

    def clear_history(self):
        self.chat_history = []
        logger.info("Chat history cleared")

    def process_query(self, question:str, chat_history: list = []):
        start_time = time.time()
        try:
            logger.info(f"Processing query: {question}")
            response = self.rag_chain.invoke({
                "input": question,
                "chat_history": self.chat_history
                })
            
            self.chat_history.extend([
                HumanMessage(content=question),
                AIMessage(content=response["answer"])
            ])

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