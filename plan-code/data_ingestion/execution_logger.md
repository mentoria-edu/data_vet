# Execution Logger - POC Code Model

Este diagrama sugere uma estrutura minima para registrar eventos simples da execucao. A POC nao tenta definir uma solucao completa de observabilidade.

```mermaid
classDiagram
    class ExecutionLogger {
        +record(event: LogEvent) void
        +finish() ExecutionSummary
    }

    class LogEvent {
        +component: String
        +level: String
        +message: String
    }

    class LogSink {
        <<interface>>
        +write(event: LogEvent) void
    }

    class ExecutionSummary {
        +status: String
        +failures: int
    }

    ExecutionLogger --> LogEvent : records event
    ExecutionLogger --> LogSink : writes event
    ExecutionLogger --> ExecutionSummary : creates summary
```

## Classes principais

- `ExecutionLogger`: interface simples para registrar eventos.
- `LogEvent`: evento estruturado minimo.
- `LogSink`: destino abstrato de log.
- `ExecutionSummary`: resumo basico da execucao.

## Assumptions

- Logs estruturados completos podem ser definidos depois.
- Sanitizacao, metricas e multiplos destinos ficam fora da POC.
- O objetivo inicial e apenas saber se o fluxo executou e onde falhou.
