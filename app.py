import os
import streamlit as st
import pypdf
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text_from_pdf(pdf_file):
    """Reads an uploaded PDF file and extracts all visible text."""
    reader = pypdf.PdfReader(pdf_file)
    extracted_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            extracted_text += page_text + "\n"
    return extracted_text



def analyze_resume(resume_text, job_description):
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) optimizer. 
    Analyze the following resume against the job description.
    Provide an ATS compatibility score (0-100), identify missing keywords, 
    and give specific advice to tailor the resume bullet points.
    
    Resume:
    {resume_text}
    
    Job Description:
    {job_description}
    """
    
  
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text

st.set_page_config(page_title="AI Resume Tailor", page_icon="🤖", layout="wide")
st.title("🤖 AI Resume Tailor & ATS Optimizer")
st.write("Make your resume irresistible to recruiters by aligning it with the job description.")
st.markdown("---")


uploaded_file = st.file_uploader(" Please , upload your current Resume ( in PDF format)", type=["pdf"])
job_desc = st.text_area("📋 Please, Paste the Job Description here", height=300, placeholder="Copy Paste the full job posting details here...")


if st.button("🚀 Analyze & Optimize Resume", use_container_width=True):
    if not uploaded_file:
        st.error("Please upload your resume PDF first!")
    elif not job_desc.strip():
        st.error("Please paste a job description to compare against!")
    else:
        with st.spinner("Analyzing data and generating tailored bullet points..."):
            try:
                text_from_resume = extract_text_from_pdf(uploaded_file)
                ai_feedback = analyze_resume(text_from_resume, job_desc)
                st.success("Congratulations🎉: Analysis Complete!")
                st.markdown(ai_feedback)
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")





# source ../venv/bin/activate
# streamlit run app.py