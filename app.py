import os
import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
from dotenv import load_dotenv
load_dotenv()
st.title("AI RESUME ANALYZER")
client = Groq(
   api_key=os.getenv("GROQ_API_KEY")
)
uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)
job_description = st.text_area(
    "Paste Job Description Here",
    height=200
)
analyze_button = st.button("Analyze Resume")
if job_description:
   st.write(job_description)
if uploaded_file:
    st.success("Resume Uploaded Successfully")
    
    if uploaded_file:

     pdf = PdfReader(uploaded_file)

     resume_text = ""

     for page in pdf.pages:
         resume_text += page.extract_text()

if uploaded_file and job_description and analyze_button:

    prompt = f"""
Analyze the following resume against the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Provide:

1. ATS Score out of 100
2. Missing Skills
3. Strengths
4. Suggestions for Improvement
"""

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.3-70b-versatile"
    )

    analysis = response.choices[0].message.content

    st.subheader("Analysis Result")
    st.write(analysis)
