from infrastructure.llm_client import OllamaClient
from infrastructure.logger import logger
from schemas.workflow import Intent
from typing import List, Dict
from config.settings import settings

class ResponseGenerator:
    def __init__(self):
        self.llm = OllamaClient()
        logger.info("ResponseGenerator initialized")

    async def generate(self, original_email: str, intents: List[Intent], collected_data: Dict) -> str:
        # Format intents for prompt
        intent_descriptions = [f"- {intent.department.value}: {intent.description}" for intent in intents]
        

        logger.info(f"Generating response for {len(intents)} intent(s)")
        logger.debug(f"Intents: {[i.department.value for i in intents]}")
        logger.debug(f"Collected data keys: {list(collected_data.keys())}")

        prompt = f"""You are a professional customer support agent. Write a helpful, empathetic response.

Customer email: {original_email}

Issues detected:
{chr(10).join(intent_descriptions)}

Information gathered from our systems:
{collected_data}

Write a response that:
1. Addresses EVERY issue the customer mentioned
2. Includes the specific information we found (order status, product info, refund policy)
3. Is polite, professional, and helpful
4. Ends with an offer to help further

Return ONLY the email text, no explanations or JSON."""

        try:
            response = await self.llm.generate(prompt, temperature=0.7)
            logger.info(f"Response generated successfully ({len(response)} characters)")
            logger.debug(f"Response preview: {response[:settings.max_email_preview]}...")
            return response.strip()
        except Exception as e:
            logger.error(f"Response generation failed: {str(e)}")
            return "Dear customer, we're experiencing technical issues. Please contact support directly. Thank you for your patience."