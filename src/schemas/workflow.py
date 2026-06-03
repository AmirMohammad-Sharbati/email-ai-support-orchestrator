from pydantic import BaseModel, Field
from typing import List
from schemas.enums import Department

class Intent(BaseModel):
    department: Department
    description: str
    required_info: List[str]
    confidence: float = Field(ge=0, le=1, default=0.9)

class WorkflowPlan(BaseModel):
    intents: List[Intent]
    execution_order: List[str]