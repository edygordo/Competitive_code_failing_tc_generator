from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
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

if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)

class structuredExtraction(BaseModel):
    
    edge_case:str
    reasoning:str

structured_tc_extraction = llm.with_structured_output(structuredExtraction) # Structure the output as per the pydantic class

system = """
    You are a competitor coding judge. Your job is to find edge cases where the user might have missed the logic. Your focus is to generate
    a test case where user's code can break using the question description provided. You will be provided with the question ,basline code
    (which is the ground truth), user code(which has some bugs) and the past attempts of edge cases.
    Referring to these paramters generate a valid failing edge case that the user's code might have missed.
"""

answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human","The Question: {question}. User's code:{user_code}. Baseline code:{baseline_code}. The past attempts: {all_messages}"),
    ]
)

failing_tc_extractor: RunnableSequence = answer_prompt | structured_tc_extraction