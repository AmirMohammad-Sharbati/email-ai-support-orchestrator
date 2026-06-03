import re
from infrastructure.llm_client import OllamaClient

class EntityExtractor:
    def __init__(self):
        self.llm = OllamaClient()
    
    async def extract(self, email_text: str, required_fields: list) -> dict:
        """Extract entities using regex first, then LLM"""
        extracted = {}
        
        # Regex for order_id
        if "order_id" in required_fields or "order" in str(required_fields):
            patterns = [
                r'#?ORD[-\s]?(\d+)',
                r'order\s+#?(\d+)',
                r'#(\d{4,})'
            ]
            for pattern in patterns:
                match = re.search(pattern, email_text, re.IGNORECASE)
                if match:
                    extracted["order_id"] = match.group(1)
                    break
        
        # Regex for product_name
        if "product_name" in required_fields or "product" in str(required_fields):
            products = ["speaker", "headphone", "laptop", "charger", "cable", "mouse", "keyboard"]
            for product in products:
                if product in email_text.lower():
                    extracted["product_name"] = product
                    break
        
        # If still missing fields, use LLM
        missing_fields = [f for f in required_fields if f not in extracted]
        if missing_fields:
            llm_extracted = await self._llm_extract(email_text, missing_fields)
            extracted.update(llm_extracted)
        
        return extracted
    
    async def _llm_extract(self, email_text: str, fields: list) -> dict:
        prompt = f"""Extract these fields from the email. Return ONLY JSON.
Email: {email_text}
Fields needed: {fields}
Output example: {{"order_id": "1234", "product_name": "speaker"}}"""
        
        return await self.llm.get_json(prompt)