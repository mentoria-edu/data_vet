# Level 4 - Raw Data Generator

```mermaid
classDiagram
direction TB

class RawWriter {
  +String storagePath
  +writeAggregate(AggregateResult result) void
  +writeTextSearch(TextSearchPage page) void
  +buildRecord(SearchArea area, RawApiResponse response, int pageNumber) RawRecord
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
  +aggregatePath(SearchArea area, DateTime timestamp) String
  +textSearchPath(SearchArea area, int pageNumber, DateTime timestamp) String
}

class RawRecord {
  +RawMetadata metadata
  +RawApiResponse response
}

class RawMetadata {
  +String areaId
  +DateTime timestamp
  +Map queryParams
  +int pageNumber
  +String endpoint
  +LocationRectangle locationRectangle
}

class AggregateResult {
  +SearchArea area
  +int establishmentCount
  +SearchAction action
  +RawApiResponse rawResponse
}

class TextSearchPage {
  +SearchArea area
  +int pageNumber
  +String nextPageToken
  +List~Place~ places
  +RawApiResponse rawResponse
}

class SearchArea {
  +String areaId
  +int resolution
  +LocationRectangle locationRectangle
}

class RawApiResponse {
  +String endpoint
  +Map queryParams
  +Json payload
  +DateTime receivedAt
}

RawWriter --> RawStorageRepository : persists
RawWriter --> RawPathBuilder : paths
RawWriter ..> RawRecord : builds
RawWriter ..> AggregateResult : reads
RawWriter ..> TextSearchPage : reads

FileRawStorageRepository ..|> RawStorageRepository : implements
RawStorageRepository ..> RawRecord : saves
RawPathBuilder ..> SearchArea : reads
```
