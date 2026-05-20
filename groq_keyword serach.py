import fitz  
from groq import Groq

# ---------------- GROQ API SETUP ----------------

API_KEY = "your api key"

client = Groq(api_key=API_KEY)

# ---------------- PDF TEXT EXTRACTION ----------------

def extract_text(pdf_path):

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    return text


# ---------------- KEYWORD SEARCH ----------------

def keyword_search(text, question):

    question_words = question.lower().split()

    paragraphs = text.split("\n")

    matched_paragraphs = []

    for para in paragraphs:

        para_lower = para.lower()

        for word in question_words:

            if word in para_lower:
                matched_paragraphs.append(para)

    return " ".join(matched_paragraphs[:20])


# ---------------- CHATBOT FUNCTION ----------------

def ask_pdf(question, pdf_text):

    relevant_text = keyword_search(pdf_text, question)

    if not relevant_text:
        return "No relevant information found in PDF."

    prompt = f"""
Answer the question only using the PDF content below.

PDF Content:
{relevant_text}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        # max_tokens=300
    )

    return response.choices[0].message.content


# ---------------- MAIN PROGRAM ----------------

pdf_path = "python_introduction_notes.pdf"

print("Reading PDF...")

pdf_text = extract_text(pdf_path)

print("PDF Loaded Successfully!")

while True:

    question = input("\nAsk Question (type exit to quit): ")

    if question.lower() == "exit":
        break

    answer = ask_pdf(question, pdf_text)

    print("\nAnswer:")
    print(answer)