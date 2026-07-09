# Raw Data Generator - POC Code Model

Este diagrama sugere uma estrutura minima para transformar respostas de API em dados brutos persistidos. A POC busca preservar o payload recebido sem modelar todos os metadados finais.

```mermaid
classDiagram
    class RawDataGenerator {
        +buildDataset(pages: List~ApiResponsePage~) RawDataset
        +writeBatch(pages: List~ApiResponsePage~) void
    }

    class RawDataset {
        +sourceName: String
        +records: List~RawRecord~
    }

    class RawRecord {
        +targetId: String
        +payload: Json
    }

    class RawStorageRepository {
        <<interface>>
        +save(path: String, dataset: RawDataset) void
    }

    class RawStoragePath {
        +datasetPath(sourceName: String) String
    }

    RawDataGenerator --> ApiResponsePage : reads pages
    RawDataGenerator --> RawDataset : creates dataset
    RawDataset --> RawRecord : contains records
    RawDataGenerator --> RawStoragePath : resolves path
    RawDataGenerator --> RawStorageRepository : saves dataset
```

## Classes principais

- `RawDataGenerator`: monta e salva o dataset bruto.
- `RawDataset`: pacote simples de registros brutos.
- `RawRecord`: payload bruto associado a um alvo.
- `RawStorageRepository`: destino abstrato de persistencia.
- `RawStoragePath`: regra simples para montar o caminho de saida.

## Assumptions

- O formato fisico do arquivo ainda nao esta definido.
- Metadados completos podem ser adicionados depois.
- `ApiResponsePage` vem do bloco `DataExtractionExecutor`.
