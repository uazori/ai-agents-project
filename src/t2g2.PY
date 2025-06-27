#- Implement agent that gathers all information from the repository and builds the document (beginner) (agent + tools) 
#- Ensure each section has 1-2 page of text and does not contain generic information and instead has concrete details such as: (med to high #complexity)  
#Endpoints with business logic 
#Database schema 
#Topics from message queue 
#How project can be built and packaged (use code evaluation) 
#Make full architecture document with 30+pages (advanced) 


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


file_path = "/Users/vadymo/code/chessrating/chess-rating-server"
llm = OllamaLLM(model="llama3.2", temperature=0.0)

language = "java"

templateCreateTest = """You are agent that gathers all information from the repository url: {url} and builds the document  
each section has 1-2 page of text and does not contain generic information and instead has concrete details
Document should consist of the following sections: 
Endpoints with business logic 
Database schema 
Topics from message queue 
How project can be built and packaged
return response as array of strings, each string is a section of the document"""

prompt = ChatPromptTemplate.from_template(templateCreateTest)

chainCreate = prompt | llm 

#reviews = retriver.invoke( question)
resultCreate = chainCreate.invoke({"url": file_path})

resultCreate
print("Response from Ollama LLM:", resultCreate)

