from langchain_google_genai import GoogleGenerativeAI, HarmCategory, HarmBlockThreshold
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.agent_toolkits.load_tools import load_tools
import readline
import sys

llm = GoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    temperature=0,
    safety_settings = { HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, }
    )

tools = load_tools(["terminal"], llm=llm, allow_dangerous_tools=True)
base_prompt = hub.pull("langchain-ai/react-agent-template")

# instructions = sys.argv[1]

# prompt = base_prompt.partial(instructions=instructions)

prompt = base_prompt.partial(instructions="Answer the user's request by running Linux commands via the Terminal tool.")
agent = create_react_agent(llm,tools,prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print(f"Welcome to my application.  I am configured with these tools")
for tool in tools:
  print(f'  Tool: {tool.name} = {tool.description}')

while True:
    try:
        line = input("llm>> ")
        if line:
            result = agent_executor.invoke({"input":line})
            print(result)
        else:
            break
    except Exception as e:
        print(e)
