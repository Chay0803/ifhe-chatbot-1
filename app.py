import streamlit as st
import pandas as pd
from llama_api import ask_llama
from course_matcher import match_courses
from load_docs import get_vectorstore

st.set_page_config(page_title="IFHE Chatbot", layout="wide")
st.title("IFHE College Chatbot")
st.markdown("Ask anything about admission, eligibility, scholarships, hostel, or course suggestions.")

# Load FAISS retriever
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

tab1, tab2, tab3 = st.tabs(["Ask the Chatbot", "Course Recommender", "Employee Details"])

# ─────────────────────────
# Tab 1: Chatbot
# ─────────────────────────
with tab1:
    question = st.text_input("Enter your question:")
    if st.button("Ask"):
        if question:
            with st.spinner("Reading documents and generating response..."):
                query = normalize_query(question)
                docs = retriever.invoke(query)
                context = "\n\n".join([d.page_content for d in docs[:10]])  # top 10 docs
                prompt = f"""You are an academic assistant for IFHE University. Use the context below to answer the question clearly and helpfully.

Context:
{context}

Question: {question}

Answer:"""
                answer = ask_llama(prompt)
                st.markdown("### Answer:")
                st.success(answer)
        else:
            st.warning("Please enter a question.")

# ─────────────────────────
# Tab 2: Course Recommender
# ─────────────────────────
with tab2:
    st.subheader("Course Recommendations")

    stream = st.selectbox("Select Your Stream", ["", "Science", "Commerce", "Arts"])
    interest = st.selectbox("Select Your Area of Interest", ["", "Tech", "Law", "Management"])
    english = st.selectbox("Are you comfortable in English?", ["", "Yes", "No"])
    tenth = st.number_input("Enter your 10th percentage", min_value=0.0, max_value=100.0, step=0.1)
    twelfth = st.number_input("Enter your 12th percentage", min_value=0.0, max_value=100.0, step=0.1)

    if st.button("Recommend Courses"):
        if stream and interest and english:
            if tenth < 60 or twelfth < 60:
                st.error("You are not eligible. Minimum 60% required in both 10th and 12th.")
            else:
                profile = {
                    "stream": stream,
                    "interest": interest,
                    "english": english,
                    "10th": tenth,
                    "12th": twelfth
                }
                recs = match_courses(profile)
                if recs:
                    for course in recs:
                        st.success(f"{course}")
                    if st.button("Apply Now"):
                        st.markdown("[Click here to apply](https://ifheapplicationpage.example.com)", unsafe_allow_html=True)
                else:
                    st.info("No matching courses found.")
        else:
            st.warning("Please fill all fields to get recommendations.")

# ─────────────────────────
# Tab 3: Employee Lookup
# ─────────────────────────
with tab3:
    st.subheader("Employee Details Lookup")

    try:
        df = pd.read_csv("employees.csv")  # Must contain: empid, name, salary, experience, date_of_joining
        search_type = st.radio("Search by:", ["Employee ID", "Salary ≥", "Experience ≥"])

        if search_type == "Employee ID":
            empid_input = st.text_input("Enter Employee ID")
            if st.button("Get Employee by ID"):
                if empid_input.strip():
                    match = df[df["empid"].astype(str) == empid_input.strip()]
                    if not match.empty:
                        st.dataframe(match)
                    else:
                        st.error("Employee not found.")
                else:
                    st.warning("Please enter a valid Employee ID.")

        elif search_type == "Salary ≥":
            salary_input = st.number_input("Enter Minimum Salary", min_value=0)
            if st.button("Get Employees by Salary"):
                filtered = df[df["salary"] >= salary_input]
                if not filtered.empty:
                    st.dataframe(filtered)
                else:
                    st.warning("No employees found with that salary or more.")

        elif search_type == "Experience ≥":
            exp_input = st.number_input("Enter Minimum Experience (in years)", min_value=0)
            if st.button("Get Employees by Experience"):
                filtered = df[df["experience"] >= exp_input]
                if not filtered.empty:
                    st.dataframe(filtered)
                else:
                    st.warning("No employees found with that experience or more.")
    except FileNotFoundError:
        st.error("employees.csv not found. Please upload it to use this feature.")
    except Exception as e:
        st.error(f"Error reading employee data: {e}")
