# Competitive_code_failing_tc_generator
An agentic workflow to generate a simplified failing test case for a given question given the correct(Baseline Code), User code and Failing Test Case(Optional)

## Production API & Demo Frontend

This repository now includes a FastAPI application that exposes the graph workflow as a REST
endpoint and a simple demo web page for customers to try out.

### How it works
1. POST `/analyze` with JSON containing `question`, `user_code`, `baseline_code` (optionally
   `failing_tc`).
2. The server runs the state graph (`graph_app.invoke`) and returns the state object containing
   the generated/simplified test case and explanation.
3. The root (`/`) serves an HTML form allowing users to input their code and see results inline.

### Running locally
```bash
# ensure dependencies are installed (poetry is used in this project)
poetry install
# start the server (or `python api.py` directly)
uvicorn api:api --reload --host 0.0.0.0 --port 8000
```
Then browse to `http://localhost:8000` to see the demo page.

