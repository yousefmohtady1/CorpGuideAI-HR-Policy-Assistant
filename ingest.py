import os 
import logging
import shutil
from services.document_processor import DocumentProcessor
from services.vector_store import VectorStore
from config.settings import Settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s- %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting document ingestion process")

    if os.path.exists(Settings.CHROMA_PERSIST_DIR):
        logger.warning(f"Removing existing database at {Settings.CHROMA_PERSIST_DIR}")
        shutil.rmtree(Settings.CHROMA_PERSIST_DIR)
    
    processor = DocumentProcessor()
    vector_store = VectorStore()
    
    if not os.path.exists(Settings.DATA_DIR):
        os.makedirs(Settings.DATA_DIR)
        logger.info(f"Data directory '{Settings.DATA_DIR}' not found. Created it. Please add PDFs there.")
        return

    pdf_files = [f for f in os.listdir(Settings.DATA_DIR) if f.endswith('.pdf')]

    if not pdf_files:
        logger.warning("No PDF files found in the data directory. Please add PDFs there.")
        return

    total_chunks = 0

    for pdf_file in pdf_files:
        file_path = os.path.join(Settings.DATA_DIR, pdf_file)
        logger.info(f"Processing: {pdf_file}...")

        try:
            chunks = processor.process_pdf(file_path)

            for chunk in chunks:
                chunk.metadata['source'] = pdf_file
            
            vector_store.add_documents(chunks)
            total_chunks += len(chunks)
            logger.info(f"Processed {len(chunks)} chunks from {pdf_file}")

        except Exception as e:
            logger .error(f"Failed to process {pdf_file}: {str(e)}")
            continue

    logger.info(f"Ingestion Completed. Total chunks stored: {total_chunks}")

if __name__ == "__main__":
    main()
    