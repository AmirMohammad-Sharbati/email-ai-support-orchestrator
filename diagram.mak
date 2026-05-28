
graph TB
    A[Raw Email Input] --> B[Email Analyzer/Classifier]
    B --> C[Intent Extractor]
    C --> D[Entity Extractor]
    D --> E[AI Orchestrator/Router]
    E --> F1[Sales Tool: get_order_status]
    E --> F2[Technical Tool: get_product_info]
    E --> F3[Finance Tool: get_refund_policy]
    F1 --> G[Result Aggregator]
    F2 --> G
    F3 --> G
    G --> H[Response Generator]
    H --> I[Final JSON Output]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style I fill:#9f9,stroke:#333,stroke-width:2px
    style E fill:#ff9,stroke:#333,stroke-width:2px



graph TB
    A[Email Input] --> B[Classification]
    B --> C[Intent Detection]
    C --> D[Entity Extraction]
    D --> E[Tool Selection]
    E --> F[Execution]
    F --> G[Response]




sequenceDiagram
    User->>System: Send Email
    System->>LLM: Classify Intent
    LLM->>System: Intent List
    System->>MockAPI1: get_order_status
    System->>MockAPI2: get_product_info
    MockAPI1->>System: Order Data
    MockAPI2->>System: Product Data
    System->>LLM: Generate Response
    LLM->>System: Final Response
    System->>User: JSON Output




erDiagram
    EMAIL ||--o{ INTENT : contains
    INTENT ||--o{ ENTITY : has
    INTENT ||--|| DEPARTMENT : belongs_toP
    INTENT ||--|| TOOL_CALL : triggers
    TOOL_CALL ||--|| RESULT : produces
    RESULT ||--|| RESPONSE : builds