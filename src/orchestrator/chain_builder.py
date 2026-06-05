from schemas.workflow import Intent
from schemas.response import ProcessingStep
from schemas.enums import Department, StepType
from intelligence.entity_extractor import EntityExtractor
from services.order_service import OrderService
from services.product_service import ProductService
from services.refund_service import RefundService
from typing import List, Dict
from infrastructure.logger import logger

class ChainBuilder:
    def __init__(self):
        self.entity_extractor = EntityExtractor()
        self.order_service = OrderService()
        self.product_service = ProductService()
        self.refund_service = RefundService()
        logger.info("ChainBuilder initialized")

    async def build_and_execute(self, intents: List[Intent], email_text: str) -> tuple[List[ProcessingStep], Dict]:
        processing_steps = []
        collected_data = {}
        step_id = 0
        
        logger.info(f"Building execution chain for {len(intents)} intent(s)")

        for intent in intents:
            logger.debug(f"Processing intent: {intent.department.value}")
            
            # Step 1: Extract entities
            step_id += 1
            extracted = await self.entity_extractor.extract(email_text, intent.required_info)
            processing_steps.append(ProcessingStep(
                step_id=step_id,
                step_type=StepType.ENTITY_EXTRACTION,
                department=intent.department,
                input_data={"email_preview": email_text[:200], "required_fields": intent.required_info},
                output_data=extracted
            ))

            logger.debug(f"intent is {intent}  --- Step ID  {step_id}  ---- And  {processing_steps}")
            
            # Step 2: Call appropriate service
            step_id += 1
            result = None
            
            if intent.department == Department.SALES:
                order_id = extracted.get("order_id", "unknown")
                result = await self.order_service.get_status(order_id)
            elif intent.department == Department.TECHNICAL:
                product_name = extracted.get("product_name", "product")
                result = await self.product_service.get_info(product_name)
            elif intent.department == Department.FINANCE:
                result = await self.refund_service.get_policy()
            
            if result:
                processing_steps.append(ProcessingStep(
                    step_id=step_id,
                    step_type=StepType.API_CALL,
                    department=intent.department,
                    input_data=extracted,
                    output_data=result
                ))
                collected_data[intent.department.value] = result
                logger.debug(f"API call success for {intent.department.value}")

        logger.info(f"Chain execution complete. Total steps: {len(processing_steps)}")
        
        return processing_steps, collected_data