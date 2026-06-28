# `pape` — project notes for Claude

`pape` is a small, single-author utility package published on [PyPI](https://pypi.org/project/pape/). The global Python conventions apply as-is; this file only captures what's specific to this repo.

## Layout & tooling

- `src/pape/` is the package (`src` layout, import name `pape`); `tests/pape/` mirrors it. Pure, deterministic utilities — table-driven tests are the right style.
- Build backend is `uv_build`; `requires-python = ">=3.13"`.
- Coverage is ratcheted at 100% (`fail_under` in `pyproject.toml`). Keep it there: new code needs tests in the same change.

## Releasing

Releases go to PyPI automatically via a GitHub Actions **trusted publisher** (OIDC, no stored token); a tagged `v<version>` GitHub Release triggers `publish.yml`. The full runbook and its gotchas (immutable uploads, tag-after-merge) live in [`CONTRIBUTING.md`](CONTRIBUTING.md#releasing-) — follow it rather than hand-publishing.

## pape-docs

See `pape-docs/0000 index.md` for the (currently empty) live-doc roster; the executed publishing + modernization write-ups sit in `pape-docs/archive/`.
