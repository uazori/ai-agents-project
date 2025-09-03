import os
import autogen
from dotenv import load_dotenv
from dotenv import find_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriver
from autogen import AssistantAgent, GroupChat, GroupChatManager, UserProxyAgent
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAI
from fileTools import list_files_recursive
from fileTools import read_file_as_text
from fileTools import create_test_file_from_code
from fileTools import remove_texts
from fileTools import remove_texts_with_line

print("Loading environment variables...")
load_dotenv(find_dotenv(),verbose=True)
print("Environment variables loaded.")

#Create agent that is going to write unit tests for the given project

llm = OllamaLLM(model="llama3.2", temperature=0.0)

llm_config33 = {
    "config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}],
}

#Create agent that is going to write unit tests for the given project 
file_path = "/Users/vadymo/code/chessrating/chess-rating-server/"

fileFormat = [".java"]
nameNotHasText = ["Test"]
name_has_text = ["Imp"]
filesList = list_files_recursive(file_path,fileFormat,nameNotHasText,name_has_text)
for file in filesList:
    print("file - ", file)

def create_store_data(filesList,vectorstore):
    for codeFilePath in filesList:
        print("codeFilePath - ", codeFilePath)
        fileCode = read_file_as_text(codeFilePath)
        loadFileInStore(codeFilePath,vectorstore)
        print(" file loaded:", codeFilePath)
        break # break after first file for testing purposes

def loadFileInStore(src,vectorstore):
    loaders = [ TextLoader(src) ]
    docs = []
    for l in loaders:
        docs.extend(l.load())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
    docs = text_splitter.split_documents(docs)

    vectorstore.add_documents(docs)

    print("Number of documents loaded:", len(docs))
    #return vectorstore
    
vectorstore = Chroma(
    collection_name="full_documents",
    embedding_function=OpenAIEmbeddings()
)

create_store_data(filesList,vectorstore)

qa = ConversationalRetrievalChain.from_llm(
    OpenAI(temperature=0),
    vectorstore.as_retriever(),
    memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True)
)


result = qa(({"question": """Please  generates architecture documentation about the project based on the source code and output it in the markdown format. 
    Document should consist of the following sections: 
Introduction 
Purpose & Scope 
System Overview 
- Key Functionalities 
- Overview of key features should in the format of feature name then up to 2-3 sentences on feature description 
* Technology Stack (Languages, Frameworks, Databases, CI/CD) 
* Programming language 
* Databases 
* Message Queues 
* Frameworks/Libaries 
* CI/CD (including build) 
• Codebase Structure 
* Repository Organization 
* Key packages 
* Key Modules & Entry Points (API) """}))

documentation = result['answer']
print("Response from Ollama LLM:", documentation)
create_test_file_from_code (file_path, documentation, "md")
