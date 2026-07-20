# Level 4 - Data Extraction

Este diagrama de Level 4 Code/UML sugere uma estrutura minima para enviar chamadas genericas para APIs HTTP externas. `ApiDataExtraction` expoe os atributos basicos da chamada, `ApiClient` executa o envio e `ApiResponse` representa o retorno.

```mermaid
classDiagram
    direction LR

    class ApiDataExtraction {
        +source_config: Map~String, String~
        +base_url: String
        +endpoint: String
        +method: String
        +headers: Map~String, String~
        +query_params: Map~String, String~
    }

    class ApiClient {
        +send(extraction: ApiDataExtraction) ApiResponse
    }

    class ApiResponse {
        +status_code: int
        +headers: Map~String, String~
        +body: Json
    }

    ApiClient --> ApiDataExtraction : reads API configuration
    ApiClient --> ApiResponse : returns API response
```

## Assumptions

- "Qualquer API" significa qualquer API HTTP.
- `ApiDataExtraction` concentra a configuracao basica da chamada HTTP para esta POC.
- `ApiClient` recebe a extracao configurada e retorna `ApiResponse`.
- `headers` e `query_params` podem ficar vazios para APIs que nao exigem esses valores.
- Autenticacao, timeout, retry e paginacao automatica ficam fora desta POC.
