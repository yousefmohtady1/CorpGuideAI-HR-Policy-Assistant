import logging
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.schemas import ChatRequest, ChatResponse, UploadResponse
from core.rag_pipeline import RagPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pipeline_resources = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting CorpGuide AI API...")
    try:
        pipeline_resources["rag"] = RagPipeline()
        logger.info("CorpGuide AI API ready for queries")
    
    except Exception as e:
        logger.error(f"Failed to initialize CorpGuide AI API: {str(e)}")
        raise e

    yield

    pipeline_resources.clear()
    logger.info("API shut down.")

app = FastAPI(
    title="CorpGuide AI",
    description="AI-powered HR policy assistant",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="web_ui"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("web_ui/index.html")

@app.post("/reset")
async def reset_chat():
    try:
        if 'rag' in pipeline_resources and hasattr(pipeline_resources['rag'], 'clear_history'):
            pipeline_resources['rag'].clear_history()
        return {"message": "Chat history has been reset."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        if 'rag' not in pipeline_resources:
            raise HTTPException(status_code=503, detail="System is initializing, try again later")

        rag = pipeline_resources['rag']

        result = rag.process_query(
            question= request.question,
            chat_history=request.chat_history
        )

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            latency=result["latency"]
        )

    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))