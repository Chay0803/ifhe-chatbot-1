import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def get_vectorstore():
    index_path = "faiss_index"

    if not os.path.exists(index_path):
        raise FileNotFoundError(f"❌ FAISS index not found at {index_path}. Run `build_faiss.py` to generate it.")

    # ✅ Load the embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

    # ✅ Load FAISS index from disk
    vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    print("✅ FAISS index loaded successfully.")

    return vectorstore.as_retriever(search_kwargs={"k": 5})
