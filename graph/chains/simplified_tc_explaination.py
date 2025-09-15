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
    simplified_tc_explaination: str = Field(description="Dry run the test case provided and provide the explaination of why user's code failed")


structured_response = llm.with_structured_output(structuredOutput)

system = """
    You are a veteran competitive programmer. Who is aware of all CP concepts like two-pointer, greedy, dp, sliding window techniques.
    Range jumping and other techniques that are common in CP world. You would be given question, user's code and a test case over which 
    user code failed.
    Your role is to provide user with a dry run of the PROVIDED test case and tell why his code failed for the question provided.

    NOTE:- Strictly dry run over the PROVIDED test case only.
"""

answer_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", "The question is:-{question}. The user's code is:-{user_code}. Test case which failed is:-{simplified_failing_tc}")    
])

simplify_tc_explanation: Runnable = answer_prompt | structured_response