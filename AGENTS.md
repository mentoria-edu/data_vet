# Repository Guidelines

## Project Structure

Place Python source in `src/data_vet/`; geographic-domain modules belong in `src/data_vet/geo/`. Mirror that layout under `tests/`, such as `tests/geo/test_area_generator.py`. Store source datasets or fixtures in `data/base_files/`, and keep generated, sensitive, or large files out of Git. Architecture documentation lives in `docs/c4/`; diagrams must follow `docs/c4/standards/c4_mermaid_diagram_standard.md`.

Prefer small, focused modules with predictable paths. Each module should have one responsibility; avoid “god” files and keep files below 500 lines.

## Development Commands

This repository does not yet define packaging, formatting, or test commands. Do not invent substitutes. When tooling is added, document one canonical command for each workflow in both `README.md` and this guide. Until then, use:

- `git status --short` to review the working tree.
- `rg 'TODO|FIXME' src tests docs` to find unfinished work.
- `git diff --check` to detect whitespace errors before committing.

## Code Style and Documentation

Use four-space indentation and the Python default formatter once configured. Keep functions focused, normally 4–20 lines, and limit nesting to two levels by using early returns. Eliminate duplication by extracting shared behavior.

Use explicit types everywhere: no `Any`, bare `Dict`, or untyped functions. Choose specific, searchable names; avoid generic terms such as `data`, `handler`, and `Manager`. Exception messages must include the offending value and expected shape.

Preserve existing comments during refactors. Comments explain *why*, not what the code already states. Public functions require docstrings describing intent and one usage example. Cite an issue or commit when code exists because of a specific defect or upstream constraint.

## Dependencies and Logging

Inject dependencies through constructors or parameters instead of globals. Hide third-party libraries behind thin project-owned interfaces. Emit structured JSON for diagnostic and observability logs; reserve plain text for user-facing CLI output.

## Testing Guidelines

Every new function requires a test, and every bug fix requires a regression test. Tests must be fast, independent, repeatable, self-validating, and timely. Replace API, database, and filesystem I/O with named fake classes rather than inline stubs. Name files `test_<behavior>.py` and functions `test_<expected_outcome>`. Add the official test command here once a runner is configured.

## Commits and Pull Requests

Use short, imperative messages consistent with the history, preferably Conventional Commit prefixes: `docs: atualiza diagrama C4` or `feat(geo): adiciona gerador de áreas`. Keep pull requests narrowly scoped, explain the change and validation, and link relevant issues. Include rendered screenshots for visual documentation changes and satisfy `.github/CODEOWNERS` reviews.
