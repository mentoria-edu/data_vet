# Level 4 Code POC

## Objetivo

Esta pasta descreve uma POC para a etapa **Code/UML** do C4 Model. Os arquivos mostram uma primeira ideia de organizacao de classes para a ingestao de dados, sem compromisso com a implementacao final.

As classes, metodos e tipos sao sugestoes. Eles servem para validar se o desenho geral faz sentido antes de criar codigo Python real.

## Fluxo simples

1. `SearchAreaGenerator` cria alvos de busca a partir de uma area geografica.
2. `DataExtractionExecutor` usa esses alvos para chamar APIs externas.
3. `RawDataGenerator` salva as respostas brutas.
4. `ExecutionLogger` registra eventos simples da execucao.

## Validacoes minimas

Para esta POC, basta validar:

- o diagrama usa `classDiagram`;
- o fluxo principal esta facil de entender;
- cada classe tem um nome minimamente claro;
- dependencias externas nao dominam o desenho;
- o arquivo deixa claro que a etapa e uma POC.

## Arquivos

- `data_ingestion/search_area_generator.md`
- `data_ingestion/data_extraction.md`
- `data_ingestion/execution_logger.md`
- `data_ingestion/raw_data_generator.md`

## Assumptions

- Nao existe implementacao Python real para essas classes ainda.
- As assinaturas dos metodos sao exemplos, nao contratos finais.
- Os diagramas podem ser simplificados, renomeados ou removidos durante a implementacao real.
