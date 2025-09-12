from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

# llm = ChatOllama(model="llama3.2:1b")

# Manually pull the environment key and provide it
google_api_key = "AIzaSyBD8l7uBiooJGzy0J4FCPtEl0jn9sfarAU"

if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)

@tool
def calculator(expression: str) -> str:
    " Evaluates a math expression and returns the result. The input should a simple string representation of the task you want to do. eg. input 3*4"
    return str(eval(expression))

# Initialize agent with a tool
agent = initialize_agent(
    tools=[calculator],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

response = agent.invoke("What is 3*4?")
print(response['output'])