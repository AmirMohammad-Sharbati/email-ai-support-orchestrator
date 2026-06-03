from orchestrator.router import OrchestratorRouter
from orchestrator.chain_builder import ChainBuilder
from intelligence.response_generator import ResponseGenerator
from schemas.response import EmailResponse
from schemas.enums import StepType
from datetime import datetime

class WorkflowOrchestrator:
    def __init__(self):
        self.router = OrchestratorRouter()
        self.chain_builder = ChainBuilder()
        self.response_generator = ResponseGenerator()
    
    async def process(self, email_text: str) -> EmailResponse:
        # Step 1: Detect intents
        intents = await self.router.route(email_text)
        
        # Step 2: Build execution chain and collect data
        processing_steps, collected_data = await self.chain_builder.build_and_execute(
            intents, email_text
        )
        
        # Step 3: Generate final response
        final_response = await self.response_generator.generate(
            email_text, intents, collected_data
        )
        
        # Add response generation step to processing steps
        processing_steps.append({
            "step_id": len(processing_steps) + 1,
            "step_type": StepType.RESPONSE_GENERATION,
            "department": None,
            "input_data": {"intent_count": len(intents)},
            "output_data": {"response_length": len(final_response)},
            "timestamp": datetime.now()
        })
        
        return EmailResponse(
            original_text=email_text,
            processing_steps=processing_steps,
            final_response=final_response,
            metadata={
                "intent_count": len(intents),
                "model_used": "llama3.2:3b",
                "departments_involved": [i.department.value for i in intents],
                "success": True
            }
        )