# Competitive Code Failing Test Case Generator

An agentic workflow to generate and simplify failing test cases for competitive coding problems. This tool helps debug user code by comparing it against a baseline correct code using LLM-powered analysis with LangGraph, LangSmith tracing, and Gemini API.

## Features

- **Web UI**: Interactive demo frontend for inputting code and viewing results.
- **API Endpoint**: RESTful API (`/analyze`) for programmatic access.
- **Graph Workflow**: LangGraph-based state machine for processing code analysis.
- **Tracing**: Integrated LangSmith for workflow tracing and debugging.
- **LLM Integration**: Uses Gemini (Google Generative AI) for intelligent code analysis.
- **Containerized**: Docker support for easy deployment.

## Project Structure

```
.
├── api.py                 # FastAPI application
├── main.py                # Alternative entry point
├── Dockerfile             # Docker configuration
├── pyproject.toml         # Project metadata and dependencies (Poetry)
├── requirements.txt       # Python dependencies
├── langgraph.json         # LangGraph configuration
├── static/                # Static files (CSS)
├── templates/             # Jinja2 templates (HTML)
├── graph/                 # Core graph logic
│   ├── __init__.py
│   ├── graph.py           # Main graph definition
│   ├── state.py           # State management
│   ├── consts.py          # Constants
│   ├── chains/            # Processing chains
│   ├── nodes/             # Graph nodes
│   └── helpers/           # Utility functions
└── tests/                 # Test suite
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/competitive-code-debugger.git
   cd competitive-code-debugger
   ```

2. **Install dependencies**:
   - Using Poetry (recommended):
     ```bash
     poetry install
     ```
   - Or using pip:
     ```bash
     pip install -r requirements.txt
     ```

## Setup

### API Keys

This project requires API keys for external services. You must obtain and configure them before running the application.

1. **Gemini API Key** (Google Generative AI):
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey).
   - Create an account if you don't have one.
   - Generate an API key.
   - Note: Usage may incur costs based on token consumption.

2. **LangSmith API Key** (for tracing):
   - Sign up at [LangSmith](https://smith.langchain.com/).
   - Generate your API key.
   - This is used for workflow tracing and debugging.

3. **Set Environment Variables**:
   Create a `.env` file in the project root (copy from `.env.example` if available) or set variables directly:

   ```bash
   export GEMINI_API_KEY=your_gemini_api_key_here
   export LANGCHAIN_API_KEY=your_langsmith_api_key_here
   ```

   **Security Note**: Never commit your `.env` file or hardcode keys in the code. Add `.env` to your `.gitignore`.

## Usage

### Running Locally

Start the FastAPI server:

```bash
uvicorn api:api --host 0.0.0.0 --port 8000
```

- Open your browser to `http://localhost:8000` for the demo web interface.
- API documentation is available at `http://localhost:8000/docs` (Swagger UI) or `http://localhost:8000/redoc`.

### Using the API

Send a POST request to `/analyze` with JSON payload:

```json
{
  "question": "Solve this coding problem...",
  "user_code": "def solution():\n    # user's code",
  "baseline_code": "def solution():\n    # correct code",
  "failing_tc": "optional failing test case"
}
```

### Docker Deployment

Build and run the container:

```bash
docker build -t failing-tc-analyzer:latest .
docker run -p 8000:8000 --env-file .env failing-tc-analyzer:latest
```

## Dependencies

Key dependencies (from `requirements.txt` and `pyproject.toml`):

- `fastapi>=0.116.1` - Web framework
- `uvicorn[standard]>=0.35.0` - ASGI server
- `langgraph` - Graph-based workflows
- `langchain` - LLM framework
- `langchain-google-genai` - Gemini integration
- `langchain-chroma` - Vector storage
- `beautifulsoup4` - HTML parsing
- `python-dotenv` - Environment variable management
- `jinja2` - Templating
- `pytest` - Testing framework

Full list in `requirements.txt` and `pyproject.toml`.

## Version Control

This project uses Git for version control. The repository is hosted on GitHub.

- **Clone**: `git clone https://github.com/yourusername/competitive-code-debugger.git`
- **Contribute**: Fork, create a branch, make changes, submit a PR.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Add tests if applicable.
5. Submit a pull request.

## Support

- Open issues on GitHub for bugs or feature requests.
- Check the API documentation at `/documentation` for usage details.

