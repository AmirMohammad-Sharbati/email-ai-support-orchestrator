from infrastructure.llm_client import OllamaClient
from infrastructure.logger import logger
from schemas.workflow import Intent
from schemas.enums import Department
from config.settings import settings
from typing import List

class IntentClassifier:
    def __init__(self):
        self.llm = OllamaClient()
        logger.info("IntentClassifier initialized")
    
    async def classify(self, email_text: str) -> List[Intent]:
        logger.debug(f"Classifying email: {email_text[:settings.max_email_preview]}...")

        prompt = f"""
        Analyze this customer support email. Return ONLY valid JSON.
        Email: {email_text}
        
        Output format:
        {{"intents": [
            {{"department": "sales", "description": "Order status check", "required_info": ["order_id"]}},
            {{"department": "technical", "description": "Product issue", "required_info": ["product_name"]}},
            {{"department": "finance", "description": "Refund request", "required_info": []}}
        ]}}

        Valid departments: sales, technical, finance"""

        result = await self.llm.get_json(prompt)
        intents = []
        
        for intent_data in result.get("intents", []):
            # Convert string to enum
            dept_str = intent_data.get("department", "unknown")
            try:
                department = Department(dept_str)
            except ValueError:
                department = Department.UNKNOWN
            
            intents.append(Intent(
                department=department,
                description=intent_data.get("description", ""),
                required_info=intent_data.get("required_info", []),
                confidence=intent_data.get("confidence", 0.8)
            ))
        
        # Fallback if no intents detected
        if not intents:
            logger.warning("No intents detected by LLM, using fallback")
            intents = self._fallback_classify(email_text)
                
        logger.info(f"Detected {len(intents)} intent(s): {[i.department.value for i in intents]}")
        return intents
    
    def _fallback_classify(self, email_text: str) -> List[Intent]:
        """Rule-based fallback when LLM fails"""
        
        logger.debug("Using rule-based fallback classifier")
        
        text_lower = email_text.lower()
        intents = []
        
        # Detect order/sales intent
        if any(word in text_lower for word in ["order", "shipping", "delivery", "track", "where is"]):
            intents.append(Intent(
                department=Department.SALES,
                description="Order status inquiry",
                required_info=["order_id"],
                confidence=0.7
            ))
        
        # Detect refund/finance intent
        if any(word in text_lower for word in ["refund", "return", "money back", "reimburs"]):
            intents.append(Intent(
                department=Department.FINANCE,
                description="Refund request",
                required_info=[],
                confidence=0.7
            ))
        
        # Detect technical intent
        if any(word in text_lower for word in ["broken", "connect", "not working", "error", "crash", "freeze"]):
            intents.append(Intent(
                department=Department.TECHNICAL,
                description="Technical support needed",
                required_info=["product_name"],
                confidence=0.7
            ))
        
        return intents