import typer
from typing import Optional, List
from phi.assistant import Assistant
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.knowledge.json import JSONKnowledgeBase
from phi.vectordb.pgvector import PgVector
from sentence_transformers import SentenceTransformer
from phi.llm.groq import Groq


import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

class LocalSentenceEmbedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dimensions = self.model.get_sentence_embedding_dimension()  # <== Required


    def embed(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(texts).tolist()
    def get_embedding_and_usage(self, text):
        embedding = self.model.encode(text).tolist()
        usage = {"input_tokens": len(text.split())}  
        return embedding, usage
    
knowledge_base = JSONKnowledgeBase(
    path="ImmigrantAI_Data/updated_visa_data.json",
    vector_db=PgVector(
        table_name="visa_docs_de",     
        db_url = db_url,
        embedder=LocalSentenceEmbedder()
    ),
)

knowledge_base.load()
storage = PgAssistantStorage(table_name="assistant_memory",db_url=db_url)

assistant = Assistant(
    llm = Groq(model="llama3-70b-8192"),
    knowledge_base=knowledge_base,
    storage=storage,
    system_prompt=(
        "You are ImmigrantAI, an expert assistant specialized only in immigration-related topics. "
        "You must not answer any questions outside the domain of immigration, such as general knowledge, entertainment, programming, etc. "
        "If a question is irrelevant to immigration, politely respond: 'Sorry, I can only help with immigration-related queries.'"
)
)
