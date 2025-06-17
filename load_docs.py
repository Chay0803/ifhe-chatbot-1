import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer

def get_vectorstore(data_path="data"):
    documents = []

    # ✅ Load all PDFs from the data folder
    for filename in os.listdir(data_path):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(data_path, filename))
            documents.extend(loader.load())

    # ✅ Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    # ✅ Load model with CPU-only config to avoid .to() crash
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")

    # ✅ Use LangChain wrapper
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model=model
    )

    # ✅ Build vectorstore and return retriever
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 5})
