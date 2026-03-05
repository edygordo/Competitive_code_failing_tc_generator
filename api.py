from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json

from graph.graph import app as graph_app
from graph.helpers.explanation_parser import parse_explanation

# create the FastAPI instance
api = FastAPI(
    title="Failing Test Case Analyzer",
    description="API for generating and simplifying failing test cases using an LLM-backed workflow",
    version="1.0.0",
)

# mount static directory and templates
api.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class AnalyzeRequest(BaseModel):
    question: str
    user_code: str
    baseline_code: str
    # optional failing_tc could be passed by clients if they already have one
    failing_tc: str | None = None


@api.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Render the homepage with the demo form."""
    return templates.TemplateResponse("index.html", {"request": request})


@api.get("/documentation", response_class=HTMLResponse)
def docs_page(request: Request):
    """Serve a static documentation page describing the API."""
    return templates.TemplateResponse("docs.html", {"request": request})


@api.post("/analyze")
def analyze(req: AnalyzeRequest):
    """Run the graph workflow with Python code validation and return results."""
    
    # Validate that both user_code and baseline_code are valid Python
    validation_error = validate_python_code(req.user_code)
    if validation_error:
        return JSONResponse(
            status_code=400,
            content={
                "error": f"User code is not valid Python: {validation_error}",
                "message": "Only Python code debugging is available for now."
            }
        )
    
    validation_error = validate_python_code(req.baseline_code)
    if validation_error:
        return JSONResponse(
            status_code=400,
            content={
                "error": f"Baseline code is not valid Python: {validation_error}",
                "message": "Only Python code debugging is available for now."
            }
        )
    
    # convert pydantic model to dict and invoke graph
    raw_state = graph_app.invoke(req.dict())

    # Ensure we work with a plain dict
    try:
        state = dict(raw_state)
    except Exception:
        # fallback: if the object has attributes, build dict
        state = {k: getattr(raw_state, k) for k in dir(raw_state) if not k.startswith('_')}

    # Parse final_explanation into structured blocks for richer frontend rendering
    final_expl = state.get('final_explanation') or state.get('simplified_tc_explanation') or ''
    if final_expl:
        try:
            state['parsed_explanation'] = parse_explanation(final_expl)
        except Exception:
            state['parsed_explanation'] = []

    return JSONResponse(content=state)


def validate_python_code(code: str) -> str | None:
    """
    Validate if the given code is valid Python.
    Returns None if valid, otherwise returns error message.
    """
    try:
        compile(code, '<string>', 'exec')
        return None
    except SyntaxError as e:
        return f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return f"Compilation error: {str(e)}"


# allow simple uvicorn launch via `python api.py`
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:api", host="0.0.0.0", port=8000, reload=True)
