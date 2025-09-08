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
    simplified_tc: str = Field(description="Ensure this test case is simplified. Simplified means you should remove " \
    "the unnecessary part of test cases which are repetitive and are there just to increase the test case size." \
    "Try to target which pattern or section of test case is causing failure in user's code logic and just keep that.")

    reasoning: str = Field(description="Why you performed the certain action to simplify the test case")


structured_response = llm.with_structured_output(structuredOutput)

system = """
    You are a veteran competitive programmer. Who is aware of all CP concepts like two-pointer, greedy, dp, sliding window techniques.
    Range jumping and other techniques that are common in CP world. Your role is to provide user with a minimalistic test case that he can easily 
    dry run. The test case that has been provided to you is a large one but look for the core problem with user's code and then simplify
    the provided test case. 

    Note:- If failed on first attempt to provide a correct simplified version of test case then use some robust stratergy to simplify it.
"""

answer_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", "The question is:-{question}. The user's code is:-{user_code}. Test case which failed is:-{failing_tc}")    
])

simplify_tc_system: Runnable = answer_prompt | structured_response