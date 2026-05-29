from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.schemas.enums import Department, StepType

class ProcessingStep(BaseModel):
    step_id: int
    step_type: StepType
    department: Department
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]]
    timestamp: datetime = Field(default_factory=datetime.now)

class EmailResponse(BaseModel):
    original_text: str
    processing_steps: List[ProcessingStep]
    final_response: str
    metadata: Dict[str, Any]