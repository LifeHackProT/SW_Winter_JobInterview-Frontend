from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.pinecone import PineconeIndexer


embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


def index_embeddings(embeddings, docs):
    indexer = PineconeIndexer(api_key='your-pinecone-api-key', index_name='your-index-name')
    indexer.index(embeddings, docs)


index_embeddings(embeddings, docs)