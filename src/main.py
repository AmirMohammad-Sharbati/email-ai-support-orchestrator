from fastapi import FastAPI, HTTPException
from src.models.schemas import OrchestratorRequest, OrchestratorResponse, ProcessingStep
from src.orchestrator.router import AIRouter
from src.orchestrator.chain_builder import ChainBuilder
from src.agents.composer_agent import ResponseComposer
from loguru import logger
import uuid

app = FastAPI(title="Intelligent Email Support Orchestrator")

router = AIRouter()
chain_builder = ChainBuilder()
composer = ResponseComposer()

@app.post("/process-email", response_model=OrchestratorResponse)
async def process_email(request: OrchestratorRequest):
    try:
        logger.info(f"Processing email: {request.email_text[:100]}...")
        
        # Step 1: AI Router detects intents
        intents = await router.route(request.email_text)
        logger.info(f"Detected {len(intents)} intents: {[i.department for i in intents]}")
        
        # Step 2: Build and execute chain
        processing_steps, collected_data = await chain_builder.build_and_execute(
            intents, request.email_text
        )
        
        # Step 3: Compose final response
        final_response = await composer.compose(
            original_email=request.email_text,
            intents=intents,
            collected_data=collected_data
        )
        
        return OrchestratorResponse(
            original_text=request.email_text,
            processing_steps=processing_steps,
            final_response=final_response,
            metadata={
                "intent_count": len(intents),
                "model_used": "groq/llama3-70b",
                "request_id": str(uuid.uuid4())
            }
        )
    
    except Exception as e:
        logger.error(f"Error processing email: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "orchestrator": "ready"}