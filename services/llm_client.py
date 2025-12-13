import logging
from langchain_groq import ChatGroq
from config.settings import Settings

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        try:
            logger.info(f"Initializing Groq LLM with model: {Settings.LLM_MODEL}")

            self.llm = ChatGroq(
                api_key = Settings.GROQ_API_KEY,
                model_name = Settings.LLM_MODEL,
                temperature = 0.0,
                max_retries = 2,
                streaming = True
            )
            logger.info("LLM initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize LLM Client: {str(e)}")
            raise e

    def get_llm(self):
        return self.llm