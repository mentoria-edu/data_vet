# Level 4 - Search Area Generator

```mermaid
classDiagram

class SearchAreaGenerator {
  +String boundaryPath
  +int initialResolution
  +int maxResolution
  +generateInitialAreas() List~SearchArea~
  +subdivideDenseArea(SearchArea area) List~SearchArea~
  +buildProcessingQueue() SearchAreaProcessingQueue
}

class BoundaryLoader {
  <<interface>>
  +loadBoundary(String path) Geometry
}

class SaoPauloBoundaryLoader {
  +loadBoundary(String path) Geometry
}

class H3GridGenerator {
  +polyfill(Geometry boundary, int resolution) List~H3Cell~
  +children(H3Cell cell, int nextResolution) List~H3Cell~
}

class H3ResolutionPolicy {
  +int initialResolution
  +int maxResolution
  +canSubdivide(H3Cell cell) bool
  +nextResolution(H3Cell cell) int
}

class SearchAreaProcessingQueue {
  +enqueue(List~SearchArea~ areas) void
  +dequeue() SearchArea
  +isEmpty() bool
  +size() int
}

class SearchAreaMapper {
  +fromH3Cell(H3Cell cell) SearchArea
  +toRectangle(H3Cell cell) LocationRectangle
}

class SearchArea {
  +String areaId
  +int resolution
  +LocationRectangle locationRectangle
}

class H3Cell {
  +String index
  +int resolution
  +Geometry boundary
}

class Geometry {
  +String type
  +List coordinates
}

class LocationRectangle {
  +LatLng low
  +LatLng high
}

class LatLng {
  +float latitude
  +float longitude
}

SearchAreaGenerator --> BoundaryLoader : loads city boundary
SearchAreaGenerator --> H3GridGenerator : generates H3 cells
SearchAreaGenerator --> H3ResolutionPolicy : applies resolution rules
SearchAreaGenerator --> SearchAreaMapper : exposes request areas
SearchAreaGenerator --> SearchAreaProcessingQueue : creates processing queue

SaoPauloBoundaryLoader ..|> BoundaryLoader : implements
BoundaryLoader ..> Geometry : returns
H3GridGenerator ..> Geometry : reads polygon
H3GridGenerator ..> H3Cell : creates
H3ResolutionPolicy ..> H3Cell : evaluates
SearchAreaMapper ..> H3Cell : reads generated cell
SearchAreaMapper ..> SearchArea : creates request area
SearchAreaMapper ..> LocationRectangle : creates lat lon rectangle
SearchAreaProcessingQueue "1" o-- "*" SearchArea : stores pending areas
SearchArea --> LocationRectangle : provides request rectangle
LocationRectangle *-- LatLng : defines low and high points
H3Cell --> Geometry : contains boundary
```
