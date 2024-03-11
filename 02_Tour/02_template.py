from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

llm = GoogleGenerativeAI(model="gemini-pro")

prompt_template = """Classify the following e-mail snippet as either Malicious or Benign.
Some examples include:

Message: "Unclaimed winning ticket.  View attachment for instructions to claim."
Answer: Malicious

Message: "Thanks for your interest in Generative AI"
Answer: Benign

Message: {message}
Answer: """

# create a prompt example from above template
spam_detect_prompt = PromptTemplate(
    input_variables=["message"],
    template=prompt_template
)

message = "Warning. Malicous activity on your account detected.  Click here to remediate."
print(llm.invoke(spam_detect_prompt.format(message=message)))