# Level 4 - Raw Data Generator

```mermaid
classDiagram
direction LR

class RawDataGenerator {
  +String storagePath
  +write(ApiResponsePage page) void
  +buildRecord(ApiResponsePage page) RawRecord
}

class RawStorageRepository {
  <<interface>>
  +save(String path, RawRecord record) void
}

class FileRawStorageRepository {
  +save(String path, RawRecord record) void
}

class RawPathBuilder {
  +String basePath
  +buildPath(String sourceName, String targetId, int pageNumber, DateTime timestamp) String
}

class RawRecord {
  +RawMetadata metadata
  +RawApiResponse response
}

class RawMetadata {
  +String sourceName
  +String targetId
  +DateTime timestamp
  +int pageNumber
  +String endpoint
  +Map queryParams
}

class ApiResponsePage {
  +String sourceName
  +String targetId
  +int pageNumber
  +RawApiResponse rawResponse
}

class RawApiResponse {
  +int statusCode
  +String endpoint
  +Map queryParams
  +Json payload
}

RawDataGenerator --> RawPathBuilder : builds path
RawDataGenerator --> RawStorageRepository : persists
RawDataGenerator ..> RawRecord : creates
RawDataGenerator ..> ApiResponsePage : reads
FileRawStorageRepository ..|> RawStorageRepository : implements
RawRecord --> RawMetadata : includes
RawRecord --> RawApiResponse : includes
```
