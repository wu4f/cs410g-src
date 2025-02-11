from langchain_google_genai import GoogleGenerativeAI, HarmCategory, HarmBlockThreshold
from langchain.agents import AgentExecutor, create_sql_agent
from langchain.tools import tool
from pydantic import BaseModel, Field, model_validator
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
import readline
import ast
import json
import sys

class FetchUsersPassInput(BaseModel):
    username: str = Field(description="Should be an alphanumeric string")
    @model_validator(mode="before")
    def is_alphanumeric(cls, values: dict[str,any]) -> dict[str,any]:
        if values.get("username").isalnum():
            return values
        raise ValueError("Malformed username")

@tool("fetch_users_pass", args_schema=FetchUsersPassInput, return_direct=True)
def fetch_users_pass(username):
   """Useful when you want to fetch a password hash for a particular user.  Takes a username as an argument.  Returns a JSON string"""
   res = db.run(f"SELECT passhash FROM users WHERE username = '{username}';")
   result = [el for sub in ast.literal_eval(res) for el in sub]
   return json.dumps(result)

@tool
def fetch_users(query):
   """Useful when you want to fetch the users in the database.  Returns a list of usernames in JSON."""
   res = db.run("SELECT username FROM users;")
   result = [el for sub in ast.literal_eval(res) for el in sub]
   return json.dumps(result)

database = sys.argv[1]
llm = GoogleGenerativeAI(
             model="gemini-1.5-pro-latest",
             temperature=0,
             safety_settings = {
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
             }
      )
db = SQLDatabase.from_uri(f"sqlite:///{database}")
toolkit = SQLDatabaseToolkit(db=db,llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    extra_tools=[fetch_users, fetch_users_pass],
    verbose=True
)

print(f"Welcome to my database querying application.  I've loaded your database at {database} and I am configured with these tools:")
for tool in agent_executor.tools:
  print(f'  Tool: {tool.name} = {tool.description}')

while True:
    line = input("llm>> ")
    if line:
        try:
            result = agent_executor.invoke(line)
            print(result)
        except Exception as e:
            print(e)
    else:
        break
