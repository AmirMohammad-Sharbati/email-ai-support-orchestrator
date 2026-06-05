import httpx
import json
import asyncio
from loguru import logger
from config.settings import settings

class OllamaClient:
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.temp = settings.ollama_temperature
        self.timeout = settings.ollama_timeout
        self.retries = settings.ollama_retries

    async def generate(self, prompt: str, temperature: float = None, retries: int = None) -> str:
        temperature = self.temp
        retries = self.retries

        for attempt in range(retries):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.base_url}/api/generate",
                        json={
                            "model": self.model,
                            "prompt": prompt,
                            "stream": False,
                            "options": {"temperature": temperature}
                        },
                        timeout=self.timeout
                    )
                    if response.status_code == 200:
                        return response.json()["response"]
                    else:
                        logger.warning(f"Attempt {attempt+1} failed: {response.status_code}")
                        if attempt == retries - 1:
                            return ""
                        await asyncio.sleep(1 * (attempt + 1))  # Exponential backoff
            except Exception as e:
                logger.error(f"Attempt {attempt+1} error: {str(e)}")
                if attempt == retries - 1:
                    return ""
                await asyncio.sleep(1 * (attempt + 1))
        return ""


    async def get_json(self, prompt: str) -> dict:
      """Get and parse JSON response from Ollama"""
      response = await self.generate(prompt, temperature=0.1)
      
      # Better cleaning - find first { and last }
      start = response.find('{')
      end = response.rfind('}') + 1
      
      if start != -1 and end != 0:
            response = response[start:end]
      
      try:
            return json.loads(response)
      except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}\nResponse: {response[:500]}")
            return {"intents": []}  # Return empty instead of failing