# Search Area Generator - POC Code Model

Este diagrama sugere uma estrutura minima para transformar uma area geografica em alvos de busca. A ideia e validar o fluxo, nao fechar a implementacao final.

```mermaid
classDiagram
    class SearchAreaGenerator {
        +loadMap() MapDataset
        +buildTargets() List~ExtractionTarget~
    }

    class MapDataset {
        +sourcePath: String
        +locations: List~String~
    }

    class H3Splitter {
        +split(area: MapDataset) List~String~
    }

    class BoundingBox {
        +minLatitude: float
        +minLongitude: float
        +maxLatitude: float
        +maxLongitude: float
    }

    class ExtractionTarget {
        +targetId: String
        +h3Index: String
        +boundingBox: BoundingBox
    }

    SearchAreaGenerator --> MapDataset : loads map
    SearchAreaGenerator --> H3Splitter : splits area
    SearchAreaGenerator --> ExtractionTarget : creates targets
    ExtractionTarget --> BoundingBox : uses bounds
```

## Classes principais

- `SearchAreaGenerator`: ponto de entrada da POC para ler o mapa e criar alvos.
- `MapDataset`: representacao simples do mapa carregado.
- `H3Splitter`: ideia inicial para quebrar areas grandes em celulas menores.
- `BoundingBox`: recorte geografico simples usado por APIs.
- `ExtractionTarget`: alvo que sera enviado para a etapa de extracao.

## Assumptions

- O formato real do mapa ainda sera definido.
- A divisao H3 pode ser removida se a POC mostrar que nao e necessaria.
- As assinaturas sao exemplos para discutir o desenho.
