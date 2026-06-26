# Diagram Standardization

## Objective

Define a visual standard for data platform diagrams, ensuring:

- Consistency
    
- Readability
    
- Ease of maintenance
    
- Quick understanding of the architecture
    

Diagrams should follow the following standards:

- C4 Model
    
- Flowchart
    

---

# Element Standards

## 1. Entities (Rectangle)

Represent systems, services, applications, or processes.

### Example

```mermaid
flowchart LR

A["Data Ingestion</br>(Python)</br>Collects Data"]
```

## Storage (Cylinder)

Represents data storage units.

### Example

```mermaid
flowchart LR

HDFS[("Storage</br>(HDFS)")]
```

## Actors (Circle)

Represent users, consumers, or systems that interact with the platform.

### Example

```mermaid
flowchart LR

USER((End User<br/>Consumes data through APIs, dashboards, and related services))
```

---

## Solid Arrow

Represents:

- Data flow
    
- Communication
    
- Action execution
    
- Read/write operations
    
- Relationships
    

Recommended format:

```
Verb + object
```

Examples:

- Sends events
    
- Queries metrics
    
- Persists raw data
    
- Publishes metrics
    

Avoid:

- Data
    
- Flow
    
- Communication
    
- Integration
    

### Example

```mermaid
flowchart LR

A[Data Ingestion]
B[HDFS]

A --> | Stores data as CSV | B
```

## UML

Class Diagram

### Example

```mermaid
classDiagram

class DataIngestion {
+extract()
+validate()
+loadRaw()
}
```

---

# Boundary Definition

Boundaries should clearly separate:

- Internal systems
    
- External systems
    
- Architectural domains
    

## Boundary Definition Example

```mermaid
flowchart LR

subgraph EXTERNAL[External Systems]
    A[Google Places API]
end

subgraph INTERNAL[Data Platform]
    B[Data Ingestion]
    C[HDFS]
    D[Spark]
end

A -->|Data| B
B -->|CSV| C
C -->|Bronze| D

style INTERNAL stroke:#2563EB,stroke-width:2px,stroke-dasharray: 5 5,fill:none;
style EXTERNAL fill:none,stroke:none;
```

---

# Rules by Level

## Level 1 — Context

### Rule

Do not include technical implementation details.

### Format

```
Name
[Type]
Description
```

Standard:

- Real system or role name
    
- No technologies
    
- No generic terms
    

### Example

```mermaid
flowchart LR

USER(["Customer<br/>[Person]<br/>Accesses platform information"])

ERP["Corporate ERP<br/>[External System]<br/>Provides operational data"]

CRM["Sales CRM<br/>[External System]<br/>Provides customer data"]

BI["Analytics Portal<br/>[External System]<br/>Consumes analytical data"]

subgraph PLATFORM_BOUNDARY["Data Platform"]

    PLATFORM["Data Platform<br/>[System]<br/>Centralizes and provides processed data"]

end

USER -->|Views metrics| PLATFORM

ERP -->|Sends operational data| PLATFORM

CRM -->|Sends customer data| PLATFORM

PLATFORM -->|Provides datasets| BI

style PLATFORM_BOUNDARY fill:none,stroke:#777,stroke-width:2px,stroke-dasharray: 5 5
```

---

# Level 2 — Container

### Format

```
Name
[Container: Technology]
Description
```

### Rules

- Functional container name
    
- Technology is allowed
    
- Clear responsibility
    
- Avoid generic names
    

### Example

```mermaid
flowchart LR

subgraph PLATFORM_BOUNDARY["Data Platform"]

direction LR

AIRFLOW["Pipeline Orchestrator<br/>[Container: Airflow]<br/>Schedules and orchestrates platform pipelines"]

INGESTION["Ingestion Service<br/>[Container: Python]<br/>Collects and sends data to raw storage"]

PROCESSOR["Analytics Processing<br/>[Container: Spark]<br/>Transforms and processes analytical datasets"]

STORAGE[("Data Lake<br/>[Container: HDFS]<br/>Stores raw and processed data")]

METADATA[("Metadata Catalog<br/>[Container: PostgreSQL]<br/>Manages schemas and analytical tables")]

end

AIRFLOW -->|Orchestrates ingestion| INGESTION

AIRFLOW -->|Orchestrates processing| PROCESSOR

INGESTION -->|Writes raw data| STORAGE

PROCESSOR -->|Reads and transforms data| STORAGE

PROCESSOR -->|Updates metadata| METADATA

style PLATFORM_BOUNDARY fill:none,stroke:#777,stroke-width:2px,stroke-dasharray: 5 5
```

---

# Level 3 — Component

## Naming Convention

### Format

```
Name
[Component]
Description
```

### Rules

- Internal module name
    
- Functional focus
    
- Represents a specific responsibility
    
- Avoid implementation details
    

### Example

```mermaid
flowchart TB

subgraph PROCESSOR_BOUNDARY["Analytics Processing"]

direction TB

CLEANING["Data Cleaning<br/>[Component: Data Cleaning]<br/>Standardizes and removes data inconsistencies"]

ENRICHMENT["Data Enrichment<br/>[Component: Data Enrichment]<br/>Enhances datasets using business rules"]

VALIDATION["Data Quality Validation<br/>[Component: Data Validation]<br/>Verifies data integrity and quality"]

CURATION["Analytical Data Curation<br/>[Component: Data Curation]<br/>Prepares datasets for analytical consumption"]

end

CLEANING -->|Standardized data| ENRICHMENT

ENRICHMENT -->|Enriched data| VALIDATION

VALIDATION -->|Validated data| CURATION

style PROCESSOR_BOUNDARY fill:none,stroke:#777,stroke-width:2px,stroke-dasharray: 5 5
```

---

# Level 4 — Code / UML

## Rule

Show:

- Classes
    
- Interfaces
    
- Methods
    
- Attributes
    
- Relationships