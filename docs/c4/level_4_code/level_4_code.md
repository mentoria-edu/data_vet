# Level 4 - Estrutura de Codigo como POC

## Visao geral

Esta etapa de **Code/UML** deve ser tratada como uma POC. O objetivo nao e definir a implementacao final, mas testar uma primeira ideia de como os componentes de ingestao poderiam ser organizados em classes, metodos e relacionamentos.

As classes e metodos dos diagramas sao sugestoes iniciais. Eles ajudam a conversar sobre o desenho, mas podem mudar quando o codigo Python real for criado.

Diagramas relacionados:

- `docs/c4/level_4_code/data_ingestion/area_generator.md`
- `docs/c4/level_4_code/data_ingestion/data_extraction.md`
- `docs/c4/level_4_code/data_ingestion/logger.md`
- `docs/c4/level_4_code/data_ingestion/raw_data_generator.md`

## Objetivo da POC

A POC existe para responder perguntas simples:

- quais classes principais podem existir;
- qual papel cada classe teria;
- como uma classe conversa com outra;
- quais dados basicos precisam passar entre as etapas.

Ela nao precisa cobrir todos os detalhes de validacao, auditoria, erros, tipagem final, performance ou seguranca. Esses pontos podem ser refinados depois, quando houver implementacao real.

## Blocos principais

### SearchAreaGenerator

Transforma uma area geografica em alvos de busca.

Na POC, ele representa a ideia de ler um mapa, opcionalmente quebrar a area em celulas H3 e gerar `ExtractionTarget`. Esses alvos serao usados depois pela extracao.

Classes auxiliares como `MapDataset`, `MapLocation`, `H3Splitter`, `H3Cell`, `GeometryConverter`, `BoundingBox` e `Geometry` existem apenas para mostrar os dados minimos que podem circular nessa etapa.

### DataExtractionExecutor

Monta e executa chamadas para APIs externas.

Na POC, ele recebe uma configuracao de fonte (`ApiSourceConfig`) e um alvo de busca (`ExtractionTarget`), cria uma requisicao (`ApiRequest`) e retorna paginas de resposta (`ApiResponsePage`).

`ApiClient` aparece como interface para deixar claro que a chamada HTTP real pode ser trocada ou simulada. `HttpApiClient`, `RawApiResponse` e `PaginationState` completam o fluxo basico de chamada e resposta.

### ExecutionLogger

Registra eventos basicos da execucao.

Na POC, ele serve para mostrar onde logs, metricas simples e resumo final poderiam ser tratados. Nao e necessario detalhar todas as regras de observabilidade agora.

`LogEvent`, `ExecutionContext`, `LogEventSanitizer`, `ExecutionMetricsCollector`, `LogSink`, `JsonLinesFileLogSink` e `ExecutionSummary` representam uma primeira ideia de organizacao para logs estruturados.

### RawDataGenerator

Salva as respostas brutas para uso posterior.

Na POC, ele recebe paginas de API (`ApiResponsePage`), monta um `RawDataset` e usa um repositorio (`RawStorageRepository`) para persistir o resultado.

`RawDatasetMetadata`, `RawRecord`, `RawMetadata`, `RawStoragePath` e `FileRawStorageRepository` mostram apenas o minimo necessario para entender como os dados brutos poderiam ser agrupados e salvos.

## Fluxo simples

O fluxo esperado da POC e:

1. `SearchAreaGenerator` cria alvos de busca.
2. `DataExtractionExecutor` usa esses alvos para chamar APIs.
3. `RawDataGenerator` salva as respostas brutas.
4. `ExecutionLogger` registra eventos simples durante o processo.

Esse fluxo deve ser entendido como uma proposta inicial. A implementacao real pode juntar, remover ou renomear classes se isso deixar o codigo mais simples.

## Validacoes minimas

Para esta etapa de POC, basta validar:

- o diagrama usa `classDiagram`;
- o fluxo principal esta facil de entender;
- cada classe tem um nome minimamente claro;
- dependencias externas nao dominam o desenho;
- o arquivo deixa claro que a etapa e uma POC.

Evite adicionar validacoes complexas neste momento. O foco e aprender rapidamente se a estrutura faz sentido.

## Assumptions

- Nao existe implementacao Python real para essas classes ainda.
- As assinaturas dos metodos sao exemplos, nao contratos finais.
- Tipos como `Map`, `Json`, `DateTime`, `RunStatus` e `PipelineConfig` podem ser ajustados depois.
- Os diagramas atuais continuam sendo apenas uma referencia visual para a POC.
