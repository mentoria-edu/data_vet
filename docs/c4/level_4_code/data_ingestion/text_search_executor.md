# Level 4 - Text Search Executor

```mermaid
classDiagram
direction TB

class TextSearchExecutor {
  +searchArea(SearchArea area) List~TextSearchPage~
  +fetchPage(TextSearchRequest request) TextSearchPage
  +hasNextPage(TextSearchPage page) bool
}

class GooglePlacesRequestBuilder {
  +String category
  +int pageSize
  +buildAggregateRequest(SearchArea area) AggregateRequest
  +buildTextSearchRequest(SearchArea area, String pageToken) TextSearchRequest
}

class GooglePlacesClient {
  <<interface>>
  +aggregate(AggregateRequest request) RawApiResponse
  +textSearch(TextSearchRequest request) RawApiResponse
}

class GooglePlacesApiClient {
  +aggregate(AggregateRequest request) RawApiResponse
  +textSearch(TextSearchRequest request) RawApiResponse
}

class GooglePlacesApiConfig {
  +String apiKey
  +String baseUrl
  +String aggregateEndpoint
  +String textSearchEndpoint
}

class ApiRequestPolicy {
  +int maxAttempts
  +int backoffSeconds
  +int requestsPerMinute
  +waitForPermit() void
  +shouldRetry(Exception error, int attempt) bool
}

class TextSearchResponseParser {
  +parsePlaces(RawApiResponse response) List~Place~
  +extractNextPageToken(RawApiResponse response) String
}

class TextSearchRequest {
  +String areaId
  +LocationRectangle locationRestriction
  +String category
  +String pageToken
  +Map queryParams
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

class Place {
  +String placeId
  +String name
  +String address
  +float latitude
  +float longitude
}

class RawApiResponse {
  +String endpoint
  +Map queryParams
  +Json payload
  +DateTime receivedAt
}

TextSearchExecutor --> GooglePlacesRequestBuilder : builds
TextSearchExecutor --> GooglePlacesClient : calls
TextSearchExecutor --> ApiRequestPolicy : limits
TextSearchExecutor --> TextSearchResponseParser : parses
TextSearchExecutor ..> TextSearchPage : returns

GooglePlacesRequestBuilder --> SearchArea : reads
GooglePlacesRequestBuilder ..> TextSearchRequest : creates

GooglePlacesApiClient ..|> GooglePlacesClient : implements
GooglePlacesApiClient --> GooglePlacesApiConfig : config
TextSearchResponseParser ..> RawApiResponse : reads
TextSearchResponseParser ..> Place : creates
```
