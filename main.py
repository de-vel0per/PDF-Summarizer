from dotenv import load_dotenv
from pypdf import PdfReader
import ollama
import os

load_dotenv()

model = os.getenv("OLLAMA_MODEL")
#print(f"Using model : {model}")

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    pages = reader.pages
    text = [page.extract_text() for page in pages]
    return "".join(text)

def chat_with_ollama(text, question):
    message = f"You are a helpful assistant. Answer questions based only on this document, never copy paste all the content of the pdf. Also if you are not sure, ask for more clear question: {text} \n\nQuestion: {question}"
    response = ollama.chat(model=model, messages=[{"role": "user", "content": message}])
    return response.message.content
    
print("Welcome to PDF Chatbot")

pdf_file = input("Please type the pdf file name with .pdf extension")    
if os.path.exists(pdf_file) :
    text = extract_text_from_pdf(pdf_file)
else:
    print("File dosen't exist")
    exit()
#print(text[:500])
 
while True:
        question = input("Ask a question about your PDF (or type exit to end):")
        if question.lower() == 'exit':
            print("Thank You")
            break
        else:
            print(chat_with_ollama(text,question))

