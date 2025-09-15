from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Go up two levels
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path)

google_api_key = os.getenv("GEMINI_API_KEY")

# llm = ChatOllama(model="llama3.2:1b")

# Manually pull the environment key and provide it


if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)


class structuredExtraction(BaseModel):
    user_code: str = Field(description="The User's code in a proper form")
    baseline_code: str= Field(description="The Baseline code provided by user in a proper form.")
    code_language: str = Field(description="The language of the code")
    failing_tc: str = Field(description="Keep Empty if not provided else fill this with the failing test case user has provided")

structured_code_extraction = llm.with_structured_output(schema=structuredExtraction)

system = "You are an expert in code extraction task. Given user query extract the code and the language it's been written in. " \
"code key should contain properly indented code and code_language should consist the language like java, python etc."


answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "The query:- {query}")
    ]
)

code_extractor: RunnableSequence = answer_prompt | structured_code_extraction