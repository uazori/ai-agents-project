from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

f = open("src/amazon_reviews.csv")
print(f.readline())
f.close()

df = pd.read_csv("src/amazon_reviews.csv",header=None, names=["Title", "Body", "Rating", "date"])
embedings = OllamaEmbeddings(model="llama3.2", temperature=0.0)

db_location ="./chrome_langchain_db"
db_path_exist = os.path.exists(db_location)
add_documents = not db_path_exist
print("add docs boolean ",add_documents)
print("add docs path exist ",db_path_exist)
if add_documents:
    documents = []
    ids = []
    print("Preparing documents for the database...")

    for i, row in df.iterrows():
        document = Document(
            page_content=row['Title'] + " " + row['Body'],
            metadata={
                "rating": row['Rating'],
                "review_date": row['date'],
                "id": str(i),
            }
            
        )
        print(f"Adding document {i} with ID {document.metadata['id']}")
        documents.append(document)
        ids.append(str(i))
        print("Adding documents to the database...")
vector_store = Chroma(
    collection_name="amazon_reviews",
    persist_directory=db_location,
    embedding_function=embedings  
    )

if add_documents:
    print("Documents added to the database successfully.")
    vector_store.add_documents(documents = documents,ids=ids)

retriver = vector_store.as_retriever(
    search_kwargs={"k": 3}
)