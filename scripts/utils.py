from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.llms.mistralai import MistralAI
from qdrant_client import QdrantClient
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_cloud_services import LlamaParse
from dotenv import load_dotenv
from typing import List
import torch
import os


load_dotenv()


qdrant_client = QdrantClient("http://localhost:6333")
device = "cuda" if torch.cuda.is_available() else "cpu" 
embedder = HuggingFaceEmbedding(model_name="nomic-ai/modernbert-embed-base", device=device)
Settings.embed_model = embedder

def ingest_documents(files: List[str], collection_name: str, llamaparse: True):
    vector_store = QdrantVectorStore(client=qdrant_client, collection_name=collection_name, enable_hybrid=True)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    if llamaparse: 
        parser = LlamaParse(
            result_type="markdown",
            api_key=os.getenv("llamacloud_api_key")
        )
        file_extractor = {".pdf": parser}
        documents = SimpleDirectoryReader(input_files=files, file_extractor=file_extractor).load_data()
    else:
        documents = SimpleDirectoryReader(input_files=files).load_data()
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
    )
    return index

load_dotenv()
