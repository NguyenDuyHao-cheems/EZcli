# AGENTS.md

Compact guide for AI agents working in this repository. Verify against current
config before relying on anything here.

## Stack

- Python 3.12+, managed by **uv**. Build backend: `uv_build`.
- TUI: **Textual**; CLI: **Typer** (`ezcli = "ezcli.cli:app"`).
- Local LLM via **Ollama** (default `qwen2.5-coder:3b` at `http://localhost:11434`).
- Tests: **pytest**; lint/format: **Ruff**; types: **mypy strict**; Markdown: **rumdl**; docs: **MkDocs**.

## Commands

Install (CI uses `--locked`; use the same locally):

```bash
uv sync --locked --group dev
```

If you change dependencies, regenerate the lockfile with `uv lock` (or `uv add`),
or CI's `uv sync --locked` will fail.

Run the app (launches the Textual TUI):

```bash
uv run ezcli
```

Full verification — run in this order, matching `.github/workflows/ci.yml`:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest --cov=ezcli --cov-report=term-missing
uv run mypy
uv build --no-sources
```

Focused checks:

```bash
uv run pytest tests/test_safety.py::test_safe_command   # single test
uv run pytest tests/unit/                              # offline/mock unit tests
uv run ruff format .                                   # auto-format
uv run pre-commit run --all-files                      # all hooks, manual
```

## Architecture

Single package under `src/ezcli/`. Entry point `cli.py` → `tui.run()`.

- `application/CommandService` orchestrates generate → safety → history.
- `llm/`: `LLMClient` is a **Protocol** (client.py); `OllamaClient` and
  `MockLLMProvider` implement it. Swap `MockLLMProvider` for tests/offline.
- `context/` collects `{current_directory, shell, operating_system}` and injects
  it into the prompt.
- `safety/` is pure-regex classification (SAFE/WARNING/BLOCKED).
- `execution/` runs everything through `bash -c`; target platform is **Linux + Bash only**.
- `domain/models.py` holds the shared dataclasses/enums (`SafetyLevel`, `ExecutionStatus`, `HistoryEntry`).

Safety is checked twice: once at generation (application) and again at execution
(execution). `WARNING` only changes the label, not the confirmation flow.

## Gotchas

- **All tests run offline** — no real Ollama required. Unit tests patch
  `ezcli.llm.urlopen`.
- `tests/test_markdown_links.py` scans every `*.md` under root, `docs/`, and
  `.github/` and fails on broken links/anchors. Adding or renaming docs can
  break the suite even when no code changed.
- Pre-commit hooks auto-fix and **abort the commit** when they rewrite files.
  Re-stage (`git add -u`) and commit again. Install once with
  `uv run pre-commit install`.
- `mypy` is `strict = true` over `src` and `tests`.
- Coverage has `fail_under = 0`; a low coverage number does not fail CI.
- Build artifacts `dist/` and `site/` are gitignored.

## Conventions

- Branch names and commit subjects: `<type>/<short-description>` and
  `<type>: <short description>`. Types: `docs`, `chore`, `feat`, `test`, `fix`, `ci`, `refactor`.
- PR target: the PR template requires opening against **`dev`** (not `main`);
  `CONTRIBUTING.md` describes `main` as primary — confirm the base before opening.

## TUI

- Prefer `no mouse` design. Prior using only keyboard when working with TUI
