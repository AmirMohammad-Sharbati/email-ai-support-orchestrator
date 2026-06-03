from intelligence.classifier import IntentClassifier
from schemas.workflow import Intent
from typing import List

class OrchestratorRouter:
    def __init__(self):
        self.classifier = IntentClassifier()
    
    async def route(self, email_text: str) -> List[Intent]:
        """Main routing logic - detect what to do"""
        intents = await self.classifier.classify(email_text)
        return intents