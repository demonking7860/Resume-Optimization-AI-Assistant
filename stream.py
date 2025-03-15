import streamlit as st
import fitz
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,

)




st.title("Made by:red[ Tom Marvolo Riddle]")
st.subheader(":blue[Resume Optimization Assistant]")
st.write("This tool helps you optimize your resume based on a job description.")



def extract_text(upload):

    if upload is not None:
       text=""
       doc=fitz.open(stream=upload.read(), filetype="pdf")
       for page in doc:
           text+=page.get_text("text") + "\n"
       
       return text
    else:
        return "No File is Uploaded Yet"

upload= st.file_uploader("Upload your resume (PDF Only)", type=["pdf"])
data=extract_text(upload)
  


job_description = st.text_area(":blue[Enter Job Description]")




# ✅ Define the LangChain prompt template
resume_prompt = PromptTemplate(
    input_variables=["resume", "job_description"],
    template="""
    You are an AI-powered resume optimization assistant.
    Your task is to analyze the given resume and optimize it according to the job description.

    **Instructions:**
    1️⃣ Identify missing **skills** and **keywords** that are relevant to the job description.
    2️⃣ Rewrite **bullet points** to make them **stronger, more impactful, and action-driven**.
    3️⃣ Improve wording to ensure the resume is **ATS (Applicant Tracking System) compatible**.
    4️⃣ Highlight **most relevant experience** while keeping it **concise and professional**.
    5️⃣ Format suggestions properly so they are ready to be added to the resume.

    **Resume:**
    {resume}

    **Job Description:**
    {job_description}

    🔍 Provide a structured response with clear resume improvements.
    """
)

if st.button("Optimize Resume"):
    if data == ""  :
        st.warning("Please upload a resume first.")
        st.stop()
    elif job_description == "":
        st.warning("Please enter a job description.")
    else:
     resume_chain = LLMChain(llm=llm, prompt=resume_prompt)
     response = resume_chain.run(resume=data, job_description=job_description)
     st.write(response)


