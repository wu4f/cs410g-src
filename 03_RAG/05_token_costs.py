import readline
import os
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"))

def calculate_completion_cost(query):
    # Cost per million tokens
    INPUT_TOKEN_COST_PER_MILLION = 0.075
    OUTPUT_TOKEN_COST_PER_MILLION = 0.3

    # Cost per token
    per_token_input_cost = INPUT_TOKEN_COST_PER_MILLION / 1000000
    per_token_output_cost = OUTPUT_TOKEN_COST_PER_MILLION / 1000000

    prompt_tokens = llm.get_num_tokens(query)
    response = llm.invoke(query)
    output_tokens = llm.get_num_tokens(response.content)
    total_cost = prompt_tokens * per_token_input_cost + output_tokens * per_token_output_cost
    print(f"-----Output response-----\n {response.content}")
    print(f"-----Token estimation and cost calculation-----")
    print(f"The number of input tokens: {prompt_tokens} and the number of output tokens: {output_tokens}")
    print(f"${INPUT_TOKEN_COST_PER_MILLION} per 1m input tokens")
    print(f"${OUTPUT_TOKEN_COST_PER_MILLION} per 1m output tokens")
    print(f"Total cost is: ${total_cost:0.10f}")

print("Enter a text query and see how much it will cost based on the number of input")
print("tokens in the query and the number of output tokens generated by the model")
while True:
    line = input(">> ")
    if line:
        calculate_completion_cost(line)
    else:
        break
