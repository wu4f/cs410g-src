from langchain_google_genai import GoogleGenerativeAI
import readline

llm = GoogleGenerativeAI(model="gemini-1.5-pro",temperature=0)

while True:
    line = input("llm>> ")
    if line:
        for chunks in llm.stream(line):
            print(chunks,end="")
        print("")
    else:
        break
