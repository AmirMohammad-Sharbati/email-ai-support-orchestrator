import os
os.environ['NO_PROXY'] = 'localhost,127.0.0.1'
os.environ['no_proxy'] = 'localhost,127.0.0.1'


import httpx
import json
import asyncio
from loguru import logger
from config.settings import settings

class OllamaClient:
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
    
    async def generate(self, prompt: str, temperature: float = 0.1) -> str:
        """Send prompt to Ollama and get response"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": temperature}
                },
                timeout=300.0
            )
            if response.status_code == 200:
                return response.json()["response"]
            else:
                logger.error(f"Ollama error: {response.status_code}")
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