# ---------------- IMPORT LIBRARIES ----------------

import streamlit as st
import fitz
from groq import Groq


# ---------------- GROQ API SETUP ----------------

API_KEY = "your groq  api key"

client = Groq(api_key=API_KEY)


# ---------------- PDF TEXT EXTRACTION ----------------

def extract_text(pdf_file):

    text = ""

    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")

    for page in pdf_document:

        text += page.get_text()

    return text


# ---------------- TEXT CHUNKING ----------------
def create_chunks(text, chunk_size=500, overlap=100):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks
# def create_chunks(text, chunk_size=500,overlap=100):

#     words = text.split()

#     chunks = []

#     for i in range(0, len(words), chunk_size):

#         chunk = " ".join(words[i:i + chunk_size])

#         chunks.append(chunk)

#     return chunks


# ---------------- KEYWORD SEARCH ----------------


def keyword_search(chunks, question):

    question_words = question.lower().split()

    matched_chunks = []

    for chunk in chunks:

        chunk_lower = chunk.lower()

        score = 0

        for word in question_words:

            if word in chunk_lower:
                score += 1

        if score > 0:
            matched_chunks.append((score, chunk))

    matched_chunks.sort(reverse=True)

    top_chunks = [chunk for score, chunk in matched_chunks[:3]]

    return "\n".join(top_chunks)


# ---------------- GROQ RESPONSE ----------------

def ask_pdf(question, chunks):

    relevant_text = keyword_search(chunks, question)

    if not relevant_text:

        return "No relevant information found in PDF."

    prompt = f"""
You are a PDF chatbot.

Answer the question only from the given PDF content.

PDF Content:
{relevant_text}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=300
    )

    return response.choices[0].message.content


# ---------------- STREAMLIT UI ----------------

st.title("PDF Chatbot using Groq")

uploaded_file = st.file_uploader(
    "Upload PDF File",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success("PDF Uploaded Successfully!")

    with st.spinner("Reading PDF..."):

        pdf_text = extract_text(uploaded_file)

        chunks = create_chunks(pdf_text)

    st.success("Chatbot Ready!")

    question = st.text_input("Ask a Question from PDF")

    if st.button("Get Answer"):

        if question:

            with st.spinner("Generating Answer..."):

                answer = ask_pdf(question, chunks)

            st.subheader("Answer")

            st.write(answer)

        else:

            st.warning("Please enter a question.")