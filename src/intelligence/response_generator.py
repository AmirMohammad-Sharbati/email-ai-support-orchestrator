from infrastructure.llm_client import OllamaClient
from schemas.workflow import Intent
from typing import List, Dict

class ResponseGenerator:
    def __init__(self):
        self.llm = OllamaClient()
    
    async def generate(self, original_email: str, intents: List[Intent], collected_data: Dict) -> str:
        # Format intents for prompt
        intent_descriptions = [f"- {intent.department.value}: {intent.description}" for intent in intents]
        
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

        response = await self.llm.generate(prompt, temperature=0.7)
        return response.strip()