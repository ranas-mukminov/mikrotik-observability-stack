# Contributing Guide

Thank you for helping improve the MikroTik Observability Stack. Please follow these guidelines to keep the project maintainable.

## Getting started

1. Fork the repository and create a feature branch (`feature/my-change`).
2. Install Python 3.11+ and the CLI dependencies via `pip install -e .[dev]`.
3. Run `scripts/lint.sh` and `pytest` before sending a pull request.

## Pull requests

- Keep PRs focused; split unrelated changes.
- Include tests for new features or bug fixes.
- Update documentation and examples when behavior changes.
- Use clear commit messages (Conventional Commits optional but appreciated).

## Code style

- Python: `ruff`/`flake8` lint, `black` formatting with default 88-column width.
- YAML/JSON: two spaces, lowercase keys unless protocol demands uppercase.
- Shell: POSIX shell (`/usr/bin/env bash` only when Bash-specific syntax is required).

## Security

- Never commit secrets, tokens, or production device addresses.
- Report security issues privately via email listed on [run-as-daemon.ru](https://run-as-daemon.ru).

## DCO / CLA

No CLA is required. If your company mandates a Developer Certificate of Origin, sign commits with `git commit -s`.

## Community expectations

Be respectful. Prefer constructive reviews and document edge cases. Follow the [Apache 2.0](LICENSE) terms for contributions.
