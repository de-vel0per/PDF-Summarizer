import streamlit as st
from pypdf import PdfReader
from groq import Groq
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()
st.set_page_config(page_title="PDF Summarizer")

def extract_text_from_pdf(file_upload):
    reader = PdfReader(file_upload)
    pages = reader.pages
    text = [page.extract_text() or "" for page in pages]
    return "".join(text)
    
def chat_with_grok(text, question):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    clean_text = text.encode('utf-16', errors='surrogatepass').decode('utf-16', errors='ignore')
    clean_text = clean_text.encode('utf-8', errors='ignore').decode('utf-8')
    message = f"You are a helpful assistant. Answer questions based only on this document, never copy paste all the content of the pdf. Also if you are not sure, ask for more clear question: {clean_text} \n\nQuestion: {question}"
    response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL"),
            messages=[{"role": "user", "content": message}]
            )
    return response.choices[0].message.content

def send_error_email(error, context=""):
    email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    error_msg = MIMEText(f"""Error in PDF Summarizer:\n\n Context: {context} \nError:{error}""")
    error_msg['Subject'] = "PDF Summarizer Error"
    error_msg['From'] = email
    error_msg['To'] = email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, password)
        smtp.sendmail(email, email, error_msg.as_string())
    
    
header = st.header("Ask questions about your PDF")
file_upload = st.file_uploader("Upload a text based pdf file", type=["pdf"])

if "messages" not in st.session_state:
    st.session_state.messages = []
question = None  
try:
    if file_upload is not None:
       text = extract_text_from_pdf(file_upload)
       if text:
           st.success("PDF uploaded successfully!")
       
           for message in st.session_state.messages:
               #st.write(message["role"] + ": " + message["content"])
               with st.chat_message(message["role"]):
                   st.write(message["content"])
               
           question = st.chat_input("Ask a question about your PDF")
           if question is not None:
               with st.chat_message("user"):
                   st.write(question)
               if len(text) > 8000:
                   st.warning("PDF is large — showing answers based on first portion only.")
               with st.spinner("Thinking..."):
                   text = text[:8000]
                   answer = chat_with_grok(text, question)
               st.session_state.messages.append({"role": "user", "content": question})
               st.session_state.messages.append({"role": "bot", "content": answer})
               st.rerun()
       else:
          st.error("Scanned PDFs cannot be read. Please upload text based PDFs")
except Exception as e:
    if "Stream has ended" in str(e) or "PdfStream" in str(e):
        st.error("This file is not a valid PDF. Please upload a real PDF file.")
    else:
        st.error("Something went wrong. Please contact pyth0nc0der.199@gmail.com")
    send_error_email(str(e), context=f"File: {file_upload.name if file_upload else 'No file'}\nQuestion: {question if question else 'No question asked'}")
    st.stop()
   
       
      # st.write("Bot: " + answer)