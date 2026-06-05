from fastapi import FastAPI, HTTPException
from schemas.request import EmailRequest
from schemas.response import EmailResponse
from orchestrator.workflow import WorkflowOrchestrator
from infrastructure.logger import logger
from infrastructure.llm_client import OllamaClient
from config.settings import settings

MAX_EMAIL_PREVIEW_LENGTH = settings.max_email_preview
MAX_EMAIL_LENGTH = settings.max_email_length

app = FastAPI(
    title="Email AI Support Orchestrator",
    description="Intelligent multi-intent email processing with Ollama",
    version="1.0.0"
)

orchestrator = WorkflowOrchestrator()

@app.post("/process", response_model=EmailResponse)
async def process_email(request: EmailRequest):
    if len(request.email_text) > MAX_EMAIL_LENGTH:
        logger.warning(f"Email rejected: too long ({len(request.email_text)} chars)")    
        raise HTTPException(status_code=400, detail=f"Email too long. Max {MAX_EMAIL_LENGTH} characters")
        
    logger.info(f"Processing email: {request.email_text[:MAX_EMAIL_PREVIEW_LENGTH]}...")
    try:
        result = await orchestrator.process(request.email_text)
        logger.success(f"Email processed successfully. Response length: {len(result.final_response)}")
        return result
    except Exception as e:
        logger.error(f"Error processing email: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    # Test Ollama connection
    try:
        test_client = OllamaClient()
        test_response = await test_client.generate("ping", temperature=0.0)
        ollama_status = "connected" if test_response else "error"
        logger.debug(f"Ollama connection: {ollama_status}")    
    except Exception as e:
        ollama_status = f"error: {str(e)}"
        logger.warning(f"Ollama health check failed: {str(e)}")

    return {
        "status": "healthy",
        "model": settings.ollama_model,
        "ollama_endpoint": settings.ollama_base_url,
        "ollama_connection": ollama_status
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on port 8000 (env: {settings.environment})")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)