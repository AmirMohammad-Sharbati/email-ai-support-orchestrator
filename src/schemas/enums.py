from enum import Enum

class Department(str, Enum):
    SALES = "sales"
    TECHNICAL = "technical"
    FINANCE = "finance"
    UNKNOWN = "unknown"

class StepType(str, Enum):
    INTENT_DETECTION = "intent_detection"
    ENTITY_EXTRACTION = "entity_extraction"
    API_CALL = "api_call"
    RESPONSE_GENERATION = "response_generation"