import os
from dotenv import load_dotenv
from dotenv import find_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriver

print("Loading environment variables...")
print("dot env path...",find_dotenv())
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
   # print("Response from LLM:", result.content)
    # Uncomment the following lines to use OpenAI's ChatOpenAI

#llm = ChatOpenAI(api_key="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",temperature=0.0, model_name="gpt-4o")
#response = llm.invoke("Hello, world!")
#print(response.content)
