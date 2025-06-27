#- Usage of mocks and meaningful data (add context about dependencies) 


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

file_path = "/Users/vadymo/code/chessrating/chess-rating-server/src/main/java/com/millhouse/chessrating/service"


llm = OllamaLLM(model="llama3.2", temperature=0.0)

language = "java"

templateCreateTest = """You are expert in generating unit test for code , 
create unit tests for project, url: {url}
give response java file with tests, do not add any other text, just java code"""

modifyTest = """You are expert in modifiing test for code in language {language}, 
 tests for file, url: {url}
give response java file with tests, do not add any other text, just java code"""

prompt = ChatPromptTemplate.from_template(templateCreateTest)

promptModify = ChatPromptTemplate.from_template(modifyTest)

chain = prompt | llm

#reviews = retriver.invoke( question)
result = chain.invoke({"url": file_path})

print("Response from Ollama LLM:", result)

