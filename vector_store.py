import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

load_dotenv()

def get_vector_store():
    client = chromadb.Client()
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-ada-002"
    )
    collection = client.get_or_create_collection(
        name="policy_guard",
        embedding_function=openai_ef
    )
    return collection

def store_circular(collection, circular_id, content, metadata):
    try:
        collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[circular_id]
        )
        return True
    except Exception as e:
        print(f"Storage error: {e}")
        return False

def search_similar(collection, query, n_results=3):
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
    except Exception as e:
        print(f"Search error: {e}")
        return None