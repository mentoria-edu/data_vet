# Level 4 - Raw Data Generator

```mermaid
classDiagram

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

class LocationRectangle {
  +LatLng low
  +LatLng high
}

class LatLng {
  +float latitude
  +float longitude
}

class RawApiResponse {
  +String endpoint
  +Map queryParams
  +Json payload
  +DateTime receivedAt
}

class SearchAction {
  <<enumeration>>
  IGNORE
  SEARCH
  SUBDIVIDE
}

class Place {
  +String placeId
  +String name
  +String address
  +float latitude
  +float longitude
}

RawWriter --> RawStorageRepository : persists raw records
RawWriter --> RawPathBuilder : resolves storage paths
RawWriter ..> RawRecord : builds
RawWriter ..> AggregateResult : receives aggregate result
RawWriter ..> TextSearchPage : receives text search page

FileRawStorageRepository ..|> RawStorageRepository : implements
RawStorageRepository ..> RawRecord : saves

RawRecord *-- RawMetadata : includes metadata
RawRecord *-- RawApiResponse : includes original response
AggregateResult --> SearchArea : references generated area
AggregateResult --> SearchAction : defines action
AggregateResult --> RawApiResponse : preserves payload
TextSearchPage --> SearchArea : references generated area
TextSearchPage "1" o-- "*" Place : contains places
TextSearchPage --> RawApiResponse : preserves payload
RawMetadata --> LocationRectangle : records request rectangle
RawPathBuilder ..> SearchArea : reads area id
SearchArea --> LocationRectangle : provides lat lon rectangle
LocationRectangle *-- LatLng : defines low and high points
```
