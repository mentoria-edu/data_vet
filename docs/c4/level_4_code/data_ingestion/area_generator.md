# Level 4 - Search Area Generator

Este diagrama de Level 4 Code/UML sugere uma estrutura minima para transformar uma area geografica em alvos de busca H3 com `bounding_box`. A resolucao H3 pode ser informada na execucao ou usar um valor padrao do `SearchAreaGenerator`.

```mermaid
classDiagram
    direction LR

    class SearchAreaGenerator {
        +default_h3_resolution: int
        +load_map() MapDataset
        +build_initial_targets(h3_resolution: int) List~ExtractionTarget~
    }

    class MapDataset {
        +source_path: String
        +locations: List~String~
    }

    class BoundingBox {
        +min_latitude: float
        +min_longitude: float
        +max_latitude: float
        +max_longitude: float
    }

    class ExtractionTarget {
        +target_id: String
        +h3_indexes: List~String~
        +bounding_box: BoundingBox
    }

    SearchAreaGenerator --> MapDataset : loads map
    SearchAreaGenerator --> ExtractionTarget : creates targets
    ExtractionTarget --> BoundingBox : uses bounds
```

## Assumptions

- O formato real do mapa ainda sera definido.
- `default_h3_resolution` e usado quando a chamada nao informar uma resolucao H3 especifica.
- As assinaturas sao exemplos para discutir o desenho.
