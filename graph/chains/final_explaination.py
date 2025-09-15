from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from langchain_core.runnables import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Go up two levels
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path)

google_api_key = os.getenv("GEMINI_API_KEY")


if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)

class structuredOutput(BaseModel):
    explanation: str = Field(description="Explanation of the failing test case")

structuredResponse = llm.with_structured_output(structuredOutput)

system = """
    You are a competitive code teacher. You will be given a code ,a failing test case and the question. You need to provide information
    to user that why your code  didn't work by explaining him over the provided failing test case. Do a Dry run of the test case
    over the given code and explain where the user's logic broke.
""" # Few shot prompting done

answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "The user code is:- {code_string} . The test case is:- {test_case}. Question is:- {question}"),
    ]
)

explaning_failing_tc: Runnable = answer_prompt | structuredResponse