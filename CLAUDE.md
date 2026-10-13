# Project: Amazon Deal Hunter Pro

## Tech Stack
- Language: Python 3.12+
- Core: Telegram Bot API, Amazon Scraping Logic
- Config: JSON / Environment Variables (.env)
- Deployment: Docker / Docker Compose
- Infrastructure: Python-based Agents

## Architecture Rules
- Separation of Concerns: Scraping logic must be isolated from Bot delivery logic.
- Error Handling: Use specific exception classes for scraping failures vs. API failures.
- Configuration: All secrets and API keys must reside in .env; never hardcoded.
- Modularity: New scraping targets should be implemented as separate agent modules in `agents/`.
- Logging: Use structured logging for tracking deal discovery and delivery.

## File Structure
- `app.py`         → Main entry point for the application.
- `config.py`       → Configuration loader and validator.
- `agents/`         → Specialized AI agents for discovery and filtering.
- `amazon-deals-telegram-bot/` → Bot interface and messaging logic.
- `requirements.txt` → Dependency management.

## Commands
- `python app.py` — start the main application
- `pip install -r requirements.txt` — install dependencies
- `docker-compose up -d` — launch the project in containers
- `python -m pytest` — run tests (to be implemented)

## Conventions
- Naming: snake_case for functions/variables, PascalCase for classes.
- Commits: Conventional Commits (feat:, fix:, refactor:, docs:).
- Typing: Use type hints for all function signatures to ensure stability.
