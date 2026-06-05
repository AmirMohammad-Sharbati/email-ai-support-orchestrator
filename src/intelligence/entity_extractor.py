import re
from infrastructure.logger import logger
from infrastructure.llm_client import OllamaClient

class EntityExtractor:
    def __init__(self):
        self.llm = OllamaClient()
        logger.info("EntityExtractor initialized")

    async def extract(self, email_text: str, required_fields: list) -> dict:
        """Extract entities using regex first, then LLM"""

        logger.debug(f"Extracting fields: {required_fields}")
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
                    logger.debug(f"Extracted order_id via regex: {extracted['order_id']}")
                    break
        
        # Regex for product_name
        if "product_name" in required_fields or "product" in str(required_fields):
            products = ["speaker", "headphone", "laptop", "charger", "cable", "mouse", "keyboard"]
            for product in products:
                if product in email_text.lower():
                    extracted["product_name"] = product
                    logger.debug(f"Extracted product_name via regex: {extracted['product_name']}")                    
                    break
        
        # If still missing fields, use LLM
        missing_fields = [f for f in required_fields if f not in extracted]
        if missing_fields:
            logger.debug(f"Missing fields, using LLM for: {missing_fields}")            
            llm_extracted = await self._llm_extract(email_text, missing_fields)
            extracted.update(llm_extracted)
            logger.debug(f"LLM extracted: {llm_extracted}")


        logger.info(f"Extraction complete: {extracted}")
        return extracted
    
    async def _llm_extract(self, email_text: str, fields: list) -> dict:
        """Use LLM as fallback for entity extraction"""
        
        logger.debug(f"Calling LLM to extract: {fields}")
        
        prompt = f"""Extract these fields from the email. Return ONLY JSON.
Email: {email_text}
Fields needed: {fields}
Output example: {{"order_id": "1234", "product_name": "speaker"}}"""
        
        try:
            result = await self.llm.get_json(prompt)
            logger.debug(f"LLM extraction result: {result}")
            return result
        except Exception as e:
            logger.error(f"LLM extraction failed: {e}")
            return {}