from orchestrator.router import OrchestratorRouter
from orchestrator.chain_builder import ChainBuilder
from intelligence.response_generator import ResponseGenerator
from schemas.response import EmailResponse, ProcessingStep
from schemas.enums import StepType
from config.settings import settings
from infrastructure.logger import logger

class WorkflowOrchestrator:
    def __init__(self):
        self.router = OrchestratorRouter()
        self.chain_builder = ChainBuilder()
        self.response_generator = ResponseGenerator()
        logger.info("WorkflowOrchestrator initialized")

    async def process(self, email_text: str) -> EmailResponse:
        """
        Process customer email through multi-intent orchestration.
        
        Args:
            email_text: Raw customer email content
            
        Returns:
            EmailResponse with processing steps and final response
            
        Raises:
            Exception: If any step fails (caught by FastAPI)
        """
        
        logger.info(f"Starting email processing: {email_text[:settings.max_email_preview]}...")

        processing_steps = []
        step_id = 0
        
        # Step 1: Detect intents
        step_id += 1
        intents = await self.router.route(email_text)
        processing_steps.append(ProcessingStep(
            step_id=step_id,
            step_type=StepType.INTENT_DETECTION,
            department=None,
            input_data={"email_preview": email_text[:200]},
            output_data={"intents": len(intents)}
        ))

        # Step 2: Build execution chain and collect data
        chain_steps, collected_data = await self.chain_builder.build_and_execute(
            intents, email_text
        )
        processing_steps.extend(chain_steps)
        
        # Step 3: Generate final response
        step_id = len(processing_steps) + 1
        final_response = await self.response_generator.generate(
            email_text, intents, collected_data
        )
        
        # Add response generation step to processing steps
        processing_steps.append(ProcessingStep(
            step_id=step_id,
            step_type=StepType.RESPONSE_GENERATION,
            department=None,
            input_data={"intent_count": len(intents)},
            output_data={"response_length": len(final_response)}
        ))
        
        logger.info(f"Processing complete. Response length: {len(final_response)} characters")

        return EmailResponse(
            original_text=email_text,
            processing_steps=processing_steps,
            final_response=final_response,
            metadata={
                "intent_count": len(intents),
                "model_used": settings.ollama_model,
                "departments_involved": [i.department.value for i in intents],
                "success": True
            }
        )