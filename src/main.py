import os
from dotenv import load_dotenv
from dotenv import find_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriver

print("Loading environment variables...")
load_dotenv(find_dotenv(),verbose=True)
print("Environment variables loaded.")

llm2 = OllamaLLM(model="llama3.2", temperature=0.0)

template = """You are expert is answering questions about a pizza restaurant 
some relevant reviews : {reviews}
Answer the following question: {question}"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | llm2 

while True:
    print("Type 'q' to quit.")
    question = input("Enter your question: q(to quit): ")
    if question.lower() == 'q':
        print("Exiting...")
        break 

    reviews = retriver.invoke( question)
    result = chain.invoke({"reviews": reviews,"question": "Does pizza taste?"})
    print("Response from Ollama LLM:", result)

