

# Level 4 - Search Area Generator

```mermaid
classDiagram
direction LR

class SearchAreaGenerator {
  +String shapefilePath
  +bool splitWithH3
  +loadMap() MapDataset
  +buildTargets() List~ExtractionTarget~
}

class MapDataset {
  +String sourcePath
  +String coordinateReferenceSystem
  +List~MapLocation~ locations
}

class MapLocation {
  +String locationId
  +String name
  +String locationType
  +Geometry geometry
}

class H3Splitter {
  +int resolution
  +split(Geometry geometry) List~H3Cell~
}

class H3Cell {
  +String h3Index
  +List~Coordinate~ boundary
}

class GeometryConverter {
  +toBoundingBox(H3Cell cell) BoundingBox
  +toGeometry(H3Cell cell) Geometry
}

class BoundingBox {
  +float minLatitude
  +float minLongitude
  +float maxLatitude
  +float maxLongitude
}

class ExtractionTarget {
  +String targetId
  +String locationId
  +String locationName
  +String locationType
  +String h3Index
  +BoundingBox boundingBox
  +Geometry geometry
  +Map values
  +Map metadata
}

class Geometry {
  +String type
  +List coordinates
}

SearchAreaGenerator --> MapDataset : loads shapefile
SearchAreaGenerator --> H3Splitter : optionally splits
SearchAreaGenerator --> GeometryConverter : converts cells
SearchAreaGenerator --> ExtractionTarget : creates
MapDataset "1" o-- "*" MapLocation : contains
MapLocation --> Geometry : defines
H3Splitter --> H3Cell : creates hexagons
GeometryConverter --> H3Cell : reads
GeometryConverter --> BoundingBox : creates rectangle
GeometryConverter --> Geometry : creates alternative shape
ExtractionTarget --> BoundingBox : uses for extraction
ExtractionTarget --> Geometry : keeps geometry context
```
