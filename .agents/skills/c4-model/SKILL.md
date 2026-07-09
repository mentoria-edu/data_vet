---
name: c4-model
description: Create, review, or update standardized C4 Model architecture diagrams in Mermaid for system context, containers, components, and code/UML. Use when Codex needs to document architecture, map actors or external systems, define system or domain boundaries, show runtime units and storage, describe component responsibilities, review C4 abstraction levels, or maintain Mermaid C4 documentation.
---

# C4 Model

Create and review C4 architecture documentation using the repository's Mermaid conventions.

## Required reference

Read [references/c4-mermaid-standard.md](references/c4-mermaid-standard.md) completely before creating or reviewing a diagram. Treat it as authoritative for notation, labels, boundaries, arrows, and level-specific constraints.

## Workflow

1. Inspect the relevant source code, configuration, existing diagrams, and documentation before inferring architecture.
2. Identify the system in focus and the audience or question the diagram must answer.
3. Select the smallest C4 level that answers that question.
4. Ask only for information that cannot be discovered and whose absence blocks a useful diagram. State non-blocking assumptions.
5. Keep one abstraction level per diagram. Split mixed views into separate diagrams.
6. Generate a Mermaid `flowchart` for levels 1–3 or `classDiagram` for level 4.
7. Review the result against the checklist before returning or saving it.

When updating documentation, preserve its established headings and explanatory context unless they violate the standard. Keep diagrams close to the architecture they describe.

## Select the C4 level

- Use **Level 1 — Context** for people, the system in focus, external systems, and high-level relationships. Exclude technologies and internal implementation.
- Use **Level 2 — Container** for applications, APIs, workers, databases, queues, object stores, and other runtime or deployable units. Include technology where useful.
- Use **Level 3 — Component** for responsibilities inside exactly one container, such as modules, services, repositories, adapters, or schedulers. Avoid classes and methods.
- Use **Level 4 — Code/UML** only when explicitly requested or when class-, interface-, method-, and relationship-level design is required.

## Produce the diagram

- Use stable, descriptive identifiers and functional names. Avoid generic labels such as `service`, `api`, `database`, or `processor` without domain context.
- Format each node exactly as required for its level.
- Represent storage with cylinders, actors with rounded/circular shapes, and systems or processes with rectangles.
- Delimit internal systems, external systems, architectural domains, ownership areas, or trust zones when the distinction matters.
- Label every relationship with a clear direction and `verb + object`, such as `Publishes metrics` or `Persists raw data`.
- Describe responsibilities rather than repeating technologies.
- Use `<br/>` for multiline labels and apply boundary styling consistently.

## Review checklist

Verify that:

- the system in focus and selected level are explicit;
- the diagram contains only concepts valid at that level;
- names are specific and descriptions explain responsibilities;
- every relationship has direction and purpose;
- external systems and architectural boundaries are visible;
- storage is not modeled as an actor;
- mediated or security-sensitive access is not shown as direct;
- Mermaid syntax follows the required `flowchart` or `classDiagram` form;
- the diagram remains readable without relying on surrounding prose.

## Response format

When creating a diagram:

1. State the selected C4 level in one sentence.
2. Provide the Mermaid fenced block.
3. List only material assumptions or missing information.

When reviewing a diagram, lead with findings ordered by severity, cite the affected elements, and provide specific corrections. Return a corrected diagram when requested.
