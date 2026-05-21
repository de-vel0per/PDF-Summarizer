import streamlit as st
from pypdf import PdfReader
import ollama
import os
from dotenv import load_dotenv

load_dotenv()
model = os.getenv("OLLAMA_MODEL")
st.set_page_config(page_title="PDF Summarizer")

def extract_text_from_pdf(file_upload):
    reader = PdfReader(file_upload)
    pages = reader.pages
    text = [page.extract_text() for page in pages]
    return "".join(text)
    
def chat_with_ollama(text, question):
    message = f"You are a helpful assistant. Answer questions based only on this document, never copy paste all the content of the pdf. Also if you are not sure, ask for more clear question: {text} \n\nQuestion: {question}"
    response = ollama.chat(model=model, messages=[{"role": "user", "content": message}])
    return response.message.content
    
header = st.header("Ask questions about your PDF")
file_upload = st.file_uploader("Upload a text based pdf file", type=["pdf"])

if "messages" not in st.session_state:
    st.session_state.messages = []
    

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
           with st.spinner("Thinking..."):
               answer = chat_with_ollama(text, question)
           st.session_state.messages.append({"role": "user", "content": question})
           st.session_state.messages.append({"role": "bot", "content": answer})
           st.rerun()
   else:
      st.error("Scanned PDFs cannot be read. Please upload text based PDFs")
   
       
      # st.write("Bot: " + answer)