# Contributing to `pape`

`pape` is a small, personal utility package maintained solely by [Carter Pape](https://carterpape.com). This file documents the development setup and the release process.

## Development setup

The project uses [uv](https://docs.astral.sh/uv/) for Python and dependency management. After cloning:

```sh
uv sync
```

That installs the runtime dependencies plus the dev tooling (ruff, pyright, pytest, pytest-cov) into a managed virtualenv.

## Layout

- `src/pape/` — the package source (`src` layout; the import name is `pape`).
- `tests/pape/` — the test suite, mirroring the package structure.

## Checks

Run the same checks CI runs before pushing:

```sh
uv run ruff check          # lint
uv run ruff format --check # formatting
uv run pyright             # type checking
uv run pytest              # tests + coverage
```

Coverage is ratcheted: `[tool.coverage.report] fail_under` in `pyproject.toml` is the floor, and it only ever goes up. After a green run that raises overall coverage, bump `fail_under` to the new `floor(percent_covered)` so the gain can't regress.

CI (`.github/workflows/ci.yml`) runs all four checks on every push to `master` and on every pull request.

## Releasing 🚀

Releases publish to [PyPI](https://pypi.org/project/pape/) automatically via a **PyPI Trusted Publisher** (GitHub Actions OIDC — no stored token). The trusted publisher is already registered on the PyPI project, so a release is just:

1. Bump `version` in `pyproject.toml`.
2. Commit the bump.
3. Tag the commit `v<version>` (e.g. `v0.1.2`) and push the tag.
4. Cut a [GitHub Release](https://github.com/CarterPape/pape-python-package/releases) for that tag (`gh release create v<version> --generate-notes` works).

Publishing the Release triggers `.github/workflows/publish.yml`, which runs `uv build` and `uv publish --trusted-publishing always` to upload the wheel and sdist.

### Gotchas ⚠️

- **PyPI uploads are immutable** — a version can never be re-uploaded or truly deleted. Let the Action be the source of truth; don't hand-publish a version CI will also push.
- The version tag must point at a commit that contains `publish.yml` (i.e. tag after merging release changes to `master`), or there's no workflow to trigger.
- `requires-python` only constrains the version being published; bumping it never rewrites the metadata of versions already on PyPI.
