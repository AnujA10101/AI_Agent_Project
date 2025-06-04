from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import wiki_tool, search_tool

load_dotenv()

# this class is for structuring the output of the agent and so that we can get data from it easily.
class ResearchResponse(BaseModel):
    insights: str
    risk_factors: list[str]

# the LLM we are setting up to use with the agent.
llm = ChatOpenAI(model="gpt-4.1")

# this is the output parser that will parse the output of the agent and convert it to a pydantic object.
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# This prompt is used to instruct the agent on how to respond to the user query.

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a financial analyst. Analyze the following summary and provide key insights and risk factors.\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [wiki_tool, search_tool]

# This agent will use the LLM and the prompt to generate a response to the user query.
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools = tools
)


agent_executor = AgentExecutor(agent = agent, tools = [], verbose = True)



def analyze(query:str) -> ResearchResponse: 
    raw_response = agent_executor.invoke({"query":query, "name": "Anuj"})
    try:
        structured_response = parser.parse(raw_response.get("output"))
        return structured_response
    except Exception as e:
        print("Error parsing reponse", e, raw_response)
        return None
