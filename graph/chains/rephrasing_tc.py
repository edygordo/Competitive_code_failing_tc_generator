from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from langchain_core.runnables import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI

# llm = ChatOllama(model="llama3.2:1b")

# Manually pull the environment key and provide it
google_api_key = "AIzaSyBD8l7uBiooJGzy0J4FCPtEl0jn9sfarAU"

if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)

class structuredOutput(BaseModel):
    rephrased_tc: str = Field(description="Rephrased test case code string")

structuredResponse = llm.with_structured_output(structuredOutput)

system = """
    You are a code re writer.
    You will be given a code and a test case. You need to produce a code string with output being always printed on the 
    stdout stream with the testcase provided.
    E.g.:-
    code: def add(x,y): return x+y , test_case: (3,4)
    Output rephrased code: def add(x,y): print(x+y) \n add(3,4)

    Note:- This is just an example, If there are any other helper function which code contains do not change their return statement.
    Just make sure the main function's output should be printed in the stdout with the test case provided.
""" # Few shot prompting done

answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "The code string is:- {code_string} . The test case is:- {test_case}"),
    ]
)

rephrasing_tc: Runnable = answer_prompt | structuredResponse