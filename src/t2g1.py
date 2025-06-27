#Create agent that generates architecture documentation about the project based on the source code and output it in the markdown format. 
 
#Document should consist of the following sections: 
#Introduction 
#Purpose & Scope 
#System Overview 
#• Key Functionalities 
#* Overview of key features should in the format of feature name then up to 2-3 sentences on feature description 
#* Technology Stack (Languages, Frameworks, Databases, CI/CD) 
#* Programming language 
#* Databases 
#* Message Queues 
#* Frameworks/Libaries 
#* CI/CD (including build) 
#• Codebase Structure 
#* Repository Organization 
#* Key packages 
#* Key Modules & Entry Points (API) 


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

templateCreateTest = """You agent that generates architecture documentation about the project based on the source code and output it in the markdown format., 
 url: {url}
 Document should consist of the following sections: 
Introduction 
Purpose & Scope 
System Overview 
• Key Functionalities 
* Overview of key features should in the format of feature name then up to 2-3 sentences on feature description 
* Technology Stack (Languages, Frameworks, Databases, CI/CD) 
* Programming language 
* Databases 
* Message Queues 
* Frameworks/Libaries 
* CI/CD (including build) 
• Codebase Structure 
* Repository Organization 
* Key packages 
* Key Modules & Entry Points (API) """

prompt = ChatPromptTemplate.from_template(templateCreateTest)

chainCreate = prompt | llm 

#reviews = retriver.invoke( question)
resultCreate = chainCreate.invoke({"url": file_path})

print("Response from Ollama LLM:", resultCreate)

