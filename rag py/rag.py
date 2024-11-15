# rag_api.py

from flask import Flask, request, jsonify
import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Initialize Flask app
app = Flask(__name__)

# Load Google API key from environment variable (replace with actual key if necessary)
GOOGLE_API_KEY = "AIzaSyCuzHQdgJZBvpja3rHTPdIONY_a4PwUJZE"

# Initialize Gemini LLM and HuggingFace Embeddings
llm = Gemini(model="models/gemini-1.5-flash", api_key=GOOGLE_API_KEY)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

# Configure global settings to use our models
Settings.llm = llm
Settings.embed_model = embed_model

# Directory for persistence
PERSIST_DIR = "./storage"

# Function to load or create the index
def load_rag_index():
    if not os.path.exists(PERSIST_DIR):
        if not os.path.exists("data"):
            raise FileNotFoundError("Data directory not found")

        documents = SimpleDirectoryReader("data").load_data()
        if not documents:
            raise ValueError("No documents found in data directory")

        index = VectorStoreIndex.from_documents(
            documents,
            llm=llm,
            embed_model=embed_model
        )
        os.makedirs(PERSIST_DIR, exist_ok=True)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(
            storage_context,
            llm=llm,
            embed_model=embed_model
        )
    return index

# Initialize or load the RAG index
index = load_rag_index()

# API endpoint to handle queries
@app.route("/query", methods=["POST"])
def query_rag():
    data = request.get_json()
    print(data)

    if not data or "query" not in data:
        return jsonify({"error": "No query provided"}), 400

    try:
        query = data["query"]
        query_engine = index.as_query_engine()
        response = query_engine.query(query)
        # print(dir(response))
          # Try extracting the actual response content
        if hasattr(response, 'response'):
            answer = response.response  # Adjust this based on the actual attribute
        else:
            answer = str(response)

        # Return the answer in the JSON response
        return jsonify({"answer": answer})
    except Exception as e:
        # This will catch any errors that occur while processing the query
        print(e)
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
