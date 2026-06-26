```mermaid
flowchart LR

    %% =====================================================
    %% SYSTEM BOUNDARY
    %% =====================================================

    subgraph VET_PLATFORM_BOUNDARY["Veterinary Search System"]

        direction LR

        %% =================================================
        %% ORCHESTRATION
        %% =================================================

        AIRFLOW["Pipeline Orchestrator<br/>[Container: Airflow]<br/>Schedules and orchestrates ingestion and processing pipelines"]

        %% =================================================
        %% INGESTION
        %% =================================================

        INGESTION["Data Ingestion<br/>[Container: Python + H3]<br/>Collects veterinary establishments data from Google Places API"]

        %% =================================================
        %% STORAGE
        %% =================================================

        STORAGE[("Data Lake<br/>[Container: MinIO]<br/>Stores raw and processed datasets")]

        %% =================================================
        %% PROCESSING
        %% =================================================

        PROCESSING["Data Processing<br/>[Container: Spark + Hudi]<br/>Transforms and curates analytical datasets"]

        %% =================================================
        %% METADATA
        %% =================================================

        CATALOG[("Data Catalog<br/>[Container: HUDI Metastore]<br/>Manages schemas and metadata from the data lake")]

    end

    %% =====================================================
    %% FLOWS
    %% =====================================================

    AIRFLOW -->|Orchestrates ingestion| INGESTION

    AIRFLOW -->|Orchestrates processing| PROCESSING

    INGESTION -->|Stores raw datasets| STORAGE
     
    STORAGE -->|Reads Raw datasets| PROCESSING

    PROCESSING -->|Writes Bronze, Silver and Gold datasets| STORAGE

    PROCESSING -->|Updates and consults table metadata| CATALOG

    %% =====================================================
    %% COLORS
    %% =====================================================

    %% Internal Containers
    classDef internal fill:#2563EB,stroke:#1D4ED8,color:#FFFFFF,stroke-width:2px;

    %% Storage
    classDef storage fill:#065F46,stroke:#047857,color:#FFFFFF,stroke-width:2px;

    %% Orchestration
    classDef orchestration fill:#B45309,stroke:#D97706,color:#FFFFFF,stroke-width:2px;

    %% Metadata
    classDef metadata fill:#0F766E,stroke:#14B8A6,color:#FFFFFF,stroke-width:2px;

    %% Boundary
    style VET_PLATFORM_BOUNDARY fill:none,stroke:#2563EB,stroke-width:2px,stroke-dasharray: 5 5

    %% =====================================================
    %% CLASS ASSIGNMENT
    %% =====================================================

    class INGESTION,PROCESSING internal;
    class STORAGE storage;
    class AIRFLOW orchestration;
    class CATALOG metadata;
```
