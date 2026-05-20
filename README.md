A simple chatbot using groq model to generate answer to a particular question from the uploaded pdf using the keyword search.

Groq_keyword search(1)
steps:
1)Groq API setup.
2)Pdf text extraction using fitz.
3)Text chunking 
4)Keyword search for relevant question.
5)Groq responses using the model and messages(role and content->promt) 
6)pdf will be already uploaded in the code.The question need to be asked in cosole and the output will be generated there itself

Groq_keyword search2(2)
steps 1-5 same as above 
6)Streamlit UI
-uploading the pdf file 
-Ask any questions from pdf 
-Generates the relevant answers from the pdf file 
