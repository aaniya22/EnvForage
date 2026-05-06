# Contributing to EnvForge

First off, thank you for considering contributing to EnvForge! It's people like you that make this tool better for everyone.

Please read the [Code of Conduct](./CODE_OF_CONDUCT.md) to keep our community approachable and respectable.

## How Can I Contribute?

### Reporting Bugs
- Ensure the bug was not already reported by searching on GitHub under [Issues](https://github.com/rishabh0510rishabh/EnvForage/issues).
- If you're unable to find an open issue addressing the problem, open a new one. Be sure to include a title and clear description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior that is not occurring.

### Suggesting Enhancements
- Open a new issue with the `enhancement` label.
- Provide a clear and detailed explanation of the feature you want and why it's important to add.

### Pull Requests
1. **Fork** the repository and create your branch from `main`.
2. If you've added code that should be tested, **add tests**.
3. If you've changed APIs, **update the documentation**.
4. Ensure the test suite passes (`pytest tests/`).
5. Format your code with `black` and `ruff`.
6. Make sure your code passes the type checker (`mypy app/`).
7. Create a PR, filling out the PR template.

## Development Setup

See the [Workflow Documentation](./docs/WORKFLOW.md#contributor-workflow) for detailed instructions on setting up the local development environment using Docker Compose or local Python tools.

### Branching Strategy
- `main` is the primary development branch.
- Feature branches should be named `feat/your-feature-name`.
- Bugfix branches should be named `fix/your-bug-name`.

### Commit Messages
We follow [Conventional Commits](https://www.conventionalcommits.org/).

Examples:
- `feat(api): add new profile endpoint`
- `fix(agent): handle missing WMI gracefully on Windows`
- `docs: update ROADMAP.md for phase 2`
- `test(core): add edge cases for CompatibilityResolver`

### Adding a New Profile
To add a new ML environment profile:
1. Add the profile definition to `backend/seeds/profiles.yaml`.
2. Run `python -m app.services.seed_service` locally to load it into your dev DB.
3. Verify it works using the API or CLI agent.
4. Update `docs/FEATURES.md` to list the new profile.

### Adding a New Template
If you add a new output script format:
1. Create the template in `backend/app/templates/jinja/`.
2. Register it in `TEMPLATE_MAP` in `backend/app/templates/engine.py`.
3. Add a test in `backend/tests/unit/templates/`.
4. Document it in `docs/features/script-generation.md`.

## Getting Help
If you need help, please open an issue with the `question` label, or check out [SUPPORT.md](./SUPPORT.md).
