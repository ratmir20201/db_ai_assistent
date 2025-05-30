from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import Qdrant, RetrievalMode
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient

from db_parsing.vertica_parse import parse_vertica_to_documents

text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=60)
docs = text_splitter.split_documents(documents=parse_vertica_to_documents())

local_embeddings = OllamaEmbeddings(model="nomic-embed-text")

# vectorstore = Qdrant.from_documents(
#     docs,
#     local_embeddings,
#     path="../qdrant_data_2",
#     collection_name="my_collection",
#     retrieval_mode=RetrievalMode.DENSE,
# )

vectorstore = Chroma.from_documents(documents=docs, embedding=local_embeddings)


if __name__ == "__main__":
    # print(docs)
    response = vectorstore.similarity_search("where are clients stored", 5)
    print(response)
