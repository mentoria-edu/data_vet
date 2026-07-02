# Level 4 - Search Area Generator

Nota: `SearchAreaGenerator` é um componente específico deste projeto, porque a ingestão depende de áreas geográficas e células H3. Em outro contexto, os `ExtractionTarget` poderiam vir diretamente de configuração, IDs externos, filas, partições ou outro gerador de targets.

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
  +split(Geometry geometry) List~Geometry~
}

class ExtractionTarget {
  +String targetId
  +String locationId
  +float latitude
  +float longitude
  +Geometry geometry
}

class Geometry {
  +String type
  +List coordinates
}

SearchAreaGenerator --> MapDataset : loads shapefile
SearchAreaGenerator --> H3Splitter : optionally splits
SearchAreaGenerator --> ExtractionTarget : creates
MapDataset "1" o-- "*" MapLocation : contains
MapLocation --> Geometry : defines
H3Splitter --> Geometry : creates cells
```
