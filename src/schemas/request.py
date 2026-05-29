from pydantic import BaseModel, Field

class EmailRequest(BaseModel):
    email_text: str = Field(..., min_length=1, description="Customer email content")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email_text": "My order #ORD-1234 is late and my speaker won't connect. Can I get a refund?"
            }
        }