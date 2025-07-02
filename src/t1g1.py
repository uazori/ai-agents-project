#Create agent that is going to write unit tests for the given project 
import os
from dotenv import load_dotenv
from dotenv import find_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriver
from typing import List, Optional
from tools import list_files_recursive
from tools import read_file_as_text
from tools import create_test_file_from_code
from tools import remove_texts
from tools import remove_texts_with_line

print("Loading environment variables...")
load_dotenv(find_dotenv(),verbose=True)
print("Environment variables loaded.")

#Create agent that is going to write unit tests for the given project 
file_path = "/Users/vadymo/code/chessrating/chess-rating-server/"

fileFormat = [".java"]
nameNotHasText = ["Test"]
name_has_text = ["Imp"]
filesList = list_files_recursive(file_path,fileFormat,nameNotHasText,name_has_text)
for file in filesList:
    print("file - ", file)



llm = OllamaLLM(model="llama3.2", temperature=0.0)
templateCreateTest = """You are expert in generating unit test for code , 
create unit tests for code: {code}
give response as code, do not add any other text or symbols"""

prompt = ChatPromptTemplate.from_template(templateCreateTest)
for codeFilePath in filesList:
    print("codeFilePath - ", codeFilePath)
    fileCode = read_file_as_text(codeFilePath)
    chain = prompt | llm
    aiResultCode = chain.invoke({"code": fileCode})

    resCleanCode = remove_texts_with_line(aiResultCode,["```java","```"])
    create_test_file_from_code (codeFilePath,resCleanCode,"java")
    print("test file generated:")
    break # break after first file for testing purposes




