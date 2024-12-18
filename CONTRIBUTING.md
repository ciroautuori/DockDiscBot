# Contributing to Discord Bot

Thank you for your interest in contributing to our Discord Bot project!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/discord-bot.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`

## Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in your values:
```bash
cp docker/.env.example docker/.env
```

4. Run with Docker:
```bash
docker-compose up -d
```

## Pull Request Process

1. Update documentation if needed
2. Update the README.md if needed
3. Follow the existing code style
4. Write meaningful commit messages
5. Create a Pull Request with a clear description

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused

## License

By contributing, you agree that your contributions will be licensed under the MIT License. 