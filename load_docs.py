import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def get_vectorstore(data_path="data"):
    documents = []

    for filename in os.listdir(data_path):
        if filename.endswith(".pdf"):
            try:
                loader = PyPDFLoader(os.path.join(data_path, filename))
                docs = loader.load()
                documents.extend(docs)
                print(f"✅ Loaded {len(docs)} pages from {filename}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")

    if not documents:
        raise ValueError("❌ No documents loaded from PDF files!")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 5})
