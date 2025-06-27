#Make sure code is compilable and runnable (medium complexity) 
# (should be done inside of the agent and use feedback loop concept with code evaluation) 

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

#Create agent that is going to write unit tests for the given project 

file_path = "/Users/vadymo/code/chessrating/chess-rating-server/src/main/java/com/millhouse/chessrating/controller"


llm = OllamaLLM(model="llama3.2", temperature=0.0)

language = "java"

templateCreateTest = """You are expert in code , 
check that project is completable and runnable, url: {url}
"""

modifyTest = """You are expert in code,validate that code is runnable : {url}
"""

prompt = ChatPromptTemplate.from_template(templateCreateTest)

promptModify = ChatPromptTemplate.from_template(modifyTest)

chain = prompt | llm  | promptModify | llm

#reviews = retriver.invoke( question)
result = chain.invoke({"url": file_path})

print("Response from Ollama LLM:", result)