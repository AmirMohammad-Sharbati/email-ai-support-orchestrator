from fastapi import FastAPI, HTTPException
from schemas.request import EmailRequest
from schemas.response import EmailResponse
from orchestrator.workflow import WorkflowOrchestrator
from infrastructure.logger import logger

app = FastAPI(
    title="Email AI Support Orchestrator",
    description="Intelligent multi-intent email processing with Ollama",
    version="1.0.0"
)

orchestrator = WorkflowOrchestrator()

@app.post("/process", response_model=EmailResponse)
async def process_email(request: EmailRequest):
    logger.info(f"Processing email: {request.email_text[:100]}...")
    try:
        result = await orchestrator.process(request.email_text)
        logger.success(f"Email processed successfully. Response length: {len(result.final_response)}")
        return result
    except Exception as e:
        logger.error(f"Error processing email: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model": "llama3.2:3b",
        "ollama_endpoint": "http://localhost:11434"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)