import streamlit as st
from llama_api import ask_llama
from course_matcher import match_courses
from load_docs import get_vectorstore

st.set_page_config(page_title="IFHE Chatbot", layout="wide")
st.title("🎓 IFHE College Chatbot (LLaMA 3.1 + PDFs)")
st.markdown("Ask anything about admission, eligibility, scholarships, hostel, or course suggestions.")

retriever = get_vectorstore()

def normalize_query(q):
    q = q.strip().lower()
    if "admission" in q:
        return "What is the admission process and important deadlines?"
    elif "fee" in q:
        return "What is the fee structure?"
    elif "calendar" in q:
        return "Show the academic calendar and schedule"
    elif "hostel" in q:
        return "What are the hostel and transport facilities?"
    elif "founder" in q:
        return "Who is the founder of IFHE?"
    return q

tab1, tab2 = st.tabs(["🤖 Ask the Chatbot", "🎓 Course Recommender"])

with tab1:
    question = st.text_input("Enter your question:")
    if st.button("Ask"):
        if question:
            with st.spinner("Reading documents and generating response..."):
                query = normalize_query(question)
                docs = retriever.invoke(query)
                context = "\n\n".join([d.page_content for d in docs])
                prompt = f"""You are an academic assistant for IFHE University. Use the context below to answer the question clearly and helpfully.

Context:
{context}

Question: {question}

Answer:"""
                answer = ask_llama(prompt)
                st.markdown("### 📌 Answer:")
                st.success(answer)
        else:
            st.warning("Please enter a question.")

with tab2:
    st.subheader("🎯 Get Course Recommendations")
    stream = st.selectbox("Select Your Stream", ["", "Science", "Commerce", "Arts"])
    interest = st.text_input("What is your area of interest? (e.g. AI, Law, Management)")
    english = st.selectbox("Are you comfortable in English?", ["", "Yes", "No"])

    if st.button("Recommend Courses"):
        if stream and interest and english:
            profile = {"stream": stream, "interest": interest, "english": english}
            recs = match_courses(profile)
            for course in recs:
                st.success(f"✅ {course}")
        else:
            st.warning("Please fill all fields to get recommendations.")
