from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import Qdrant, RetrievalMode
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient

from db_parsing.vertica_parse import parse_vertica_to_documents

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
text_splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=30,
    separator="\n",
)
docs = text_splitter.split_documents(documents=parse_vertica_to_documents())

local_embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectorstore = Chroma.from_documents(documents=docs, embedding=local_embeddings)


if __name__ == "__main__":
    # print(docs)

    response = vectorstore.similarity_search("Where are the contracts?", 10)
    print(response)
