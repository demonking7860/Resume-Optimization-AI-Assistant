import streamlit as st
import fitz  # PyMuPDF for PDF processing
import docx
import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# ✅ Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("⚠️ Gemini API Key not found! Please set it in the .env file.")
    st.stop()

# ✅ Configure LangChain with Gemini API
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

# ✅ Define a LangChain prompt template
resume_prompt = PromptTemplate(
    input_variables=["resume", "job_description"],
    template="""
    You are an AI resume expert. Optimize the given resume based on the job description.

    - Identify missing keywords and skills.
    - Improve bullet points.
    - Adjust wording for better ATS (Applicant Tracking System) compatibility.
    
    **Resume:**  
    {resume}

    **Job Description:**  
    {job_description}

    Provide structured suggestions for improvement.
    """
)

# ✅ Create LangChain LLM Chain
resume_chain = LLMChain(llm=llm, prompt=resume_prompt)

# ✅ Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    doc = fitz.open(pdf_file)
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

# ✅ Function to extract text from DOCX
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# ✅ Function to optimize resume using LangChain & Gemini
def optimize_resume(resume_text, job_description):
    response = resume_chain.run(resume=resume_text, job_description=job_description)
    return response

# ✅ Streamlit UI
st.title("📄 AI Resume Optimizer (LangChain + Gemini)")
st.write("Upload your resume and enter a job description to get AI-driven suggestions!")

# ✅ File Upload
uploaded_file = st.file_uploader("Upload your resume (PDF/DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Paste the Job Description")

if uploaded_file and job_description:
    file_extension = uploaded_file.name.split(".")[-1]

    # Extract text from resume
    if file_extension == "pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    elif file_extension == "docx":
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file format. Please upload a PDF or DOCX file.")
        resume_text = None

    if resume_text:
        st.subheader("📌 Resume Analysis & Suggested Improvements")
        suggestions = optimize_resume(resume_text, job_description)
        st.write(suggestions)
