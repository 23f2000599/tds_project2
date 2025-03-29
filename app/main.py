# from fastapi import FastAPI, File, UploadFile, Form
# from pydantic import BaseModel
# import openai
# import zipfile
# import pandas as pd
# import io
# import os
# import subprocess

# app = FastAPI()

# # Load AI Proxy Token from Environment Variable
# aiproxy_token = os.getenv("AIPROXY_TOKEN")
# if not aiproxy_token:
#     raise ValueError("AIPROXY_TOKEN is not set. Please configure your environment variables.")

# # Configure OpenAI API to use AI Proxy
# openai.api_base = "https://api.aiproxy.io/v1"
# openai.api_key = aiproxy_token  # Set token

# class QuestionRequest(BaseModel):
#     question: str

# @app.post("/api/")
# async def answer_question(question: str = Form(...), file: UploadFile = File(None)):
#     answer = ""

#     # Handle Q1: Execute `code -s` and return output
#     if question.lower().strip() == "what is the output of code -s?":
#         try:
#             output = subprocess.check_output(["code", "-s"], stderr=subprocess.STDOUT, text=True)
#             return {"answer": output}
#         except subprocess.CalledProcessError as e:
#             return {"error": f"Failed to execute 'code -s': {e.output}"}

#     # If a file is uploaded, process it
#     if file:
#         try:
#             with zipfile.ZipFile(io.BytesIO(await file.read()), 'r') as zip_ref:
#                 extracted_files = zip_ref.namelist()
                
#                 # Ensure there is at least one file inside
#                 if not extracted_files:
#                     return {"error": "ZIP file is empty."}

#                 # Find the first CSV file
#                 csv_file = next((f for f in extracted_files if f.endswith('.csv')), None)
#                 if not csv_file:
#                     return {"error": "No CSV file found in ZIP."}

#                 # Extract and read CSV
#                 with zip_ref.open(csv_file) as f:
#                     df = pd.read_csv(f)
                
#                 # Ensure 'answer' column exists
#                 if "answer" not in df.columns:
#                     return {"error": "CSV file does not contain an 'answer' column."}

#                 answer = str(df['answer'].iloc[0])  # First row, 'answer' column
            
#         except Exception as e:
#             return {"error": f"File processing failed: {str(e)}"}

#     else:
#         # Use AI Proxy to answer any general question
#         try:
#             response = openai.ChatCompletion.create(
#                 model="gpt-4-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are an AI tutor for data science."},
#                     {"role": "user", "content": question}
#                 ]
#             )
#             answer = response['choices'][0]['message']['content']
#         except Exception as e:
#             return {"error": f"LLM processing failed: {str(e)}"}

#     return {"answer": answer}
from fastapi import FastAPI
from app.utils.file_handler import process_file
from app.utils.functions import execute_question
from app.utils.openai_client import get_openai_response
from pydantic import BaseModel
from fastapi import UploadFile, File, Form

app = FastAPI()
@app.get("/health")
async def health_check():
    return {"status": "ok"}

class QuestionRequest(BaseModel):
    question: str


@app.post("/api/")
async def answer_question(question: str = Form(...), file: UploadFile = File(None)):
    answer = ""

    # Execute predefined question logic
    predefined_answer = execute_question(question)
    if predefined_answer:
        answer = predefined_answer

    # Process uploaded file
    if file:
        file_answer = await process_file(file)
        if isinstance(file_answer, dict) and "error" in file_answer:
            return file_answer
        answer = file_answer if not answer else answer + "\n" + file_answer

    # Use OpenAI API if no predefined answer exists
    if not answer:
        answer = get_openai_response(question)

    return {"answer": answer}

# from fastapi import FastAPI, UploadFile, File, Form
# from app.utils.file_handler import process_file
# from app.utils.functions import execute_question
# from app.utils.openai_client import get_openai_response
# import numpy as np
# from pydantic import BaseModel
# app = FastAPI()
# class QuestionRequest(BaseModel):
#     question: str


# @app.post("/api/")
# async def answer_question(question: str = Form(...), file: UploadFile = File(None)):
#     answer = ""

#     # Execute predefined question logic
#     predefined_answer = execute_question(question)
#     if predefined_answer:
#         answer = predefined_answer

#     # Process uploaded file
#     if file:
#         file_answer = await process_file(file)
#         if isinstance(file_answer, dict) and "error" in file_answer:
#             return file_answer
#         answer = file_answer if not answer else answer + "\n" + file_answer

#     # Use OpenAI API if no predefined answer exists
#     if not answer:
#         answer = get_openai_response(question)

#     return {"answer": answer}
