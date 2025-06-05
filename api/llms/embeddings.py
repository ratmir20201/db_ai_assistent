from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from db_parsing.vertica_parse_v2 import parse_vertica_to_documents

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1100, chunk_overlap=100)
# text_splitter = CharacterTextSplitter(
#     chunk_size=1000,
#     chunk_overlap=30,
#     separator="\n",
# )
# docs = text_splitter.split_documents(documents=parse_vertica_to_documents())
docs = parse_vertica_to_documents(10)

local_embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectorstore = Chroma.from_documents(documents=docs, embedding=local_embeddings)

if __name__ == "__main__":
    # response = vectorstore.similarity_search(
    #     "Which field in L_DIRECT_REPO_CP can be used as a connection condition with H_LEGAL_ENTITY",
    #     50,
    # )
    response = vectorstore.similarity_search(
        "where are clients stored?",
        50,
    )
    print(response)
