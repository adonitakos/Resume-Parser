# Import dependencies
from flask import Flask, render_template, request
from flask import Flask, render_template, request
import os
import re
import io
import boto3
import PyPDF2
from docx import Document
from dotenv import load_dotenv

# Banner
print("\n======== RESUME PARSER APPLICATION ========\n")

# Load environment variables
load_dotenv()
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
secret_access_key = os.environ.get('SECRET_ACCESS_KEY')
bucket_name = os.environ.get('BUCKET_NAME')

# Printing credentials (definitely don't want to do in demo lol)
print("\n=== Credentials ===")
print(f"AWS_ACCESS_KEY_ID: {aws_access_key_id}")
print(f"SECRET_ACCESS_KEY: {secret_access_key}")
print(f"BUCKET_NAME: {bucket_name}\n")

# Instantiate AWS client
client = boto3.client(
    's3',
    aws_access_key_id = aws_access_key_id,
    aws_secret_access_key = secret_access_key,
)

# Initialize Flask app
app = Flask(__name__)

# Define and render index.html home
@app.route('/')
def index():
    return render_template('index.html')

# UPLOAD route
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    object_name = file.filename
    client.upload_fileobj(file, bucket_name, object_name)
    return "File uploaded successfully"

# AWS S3 TEXT FILES IMPLMENTATION
def search_text_files(bucket_name, keyword, results):
    response = client.list_objects_v2(Bucket=bucket_name)
    for obj in response['Contents']:
        key = obj['Key']
        if key.endswith(".txt"):
            response = client.get_object(Bucket=bucket_name, Key=key)
            contents = response['Body'].read().decode('utf-8', 'ignore')
            matches = re.findall(keyword, contents, re.IGNORECASE)
            if matches:
                results.append(f"{key} contains the keyword {keyword} {len(matches)} times.")
            else:
                results.append(f"{key} does not contain the keyword {keyword}.")

# AWS S3 DOC/DOCX FILES IMPLEMENTATION
def search_doc_files(bucket_name, keyword, results):
    response = client.list_objects_v2(Bucket=bucket_name)
    for obj in response['Contents']:
        key = obj['Key']
        if key.endswith(".doc") or key.endswith(".docx"):
            response = client.get_object(Bucket=bucket_name, Key=key)
            doc_bytes = response['Body'].read()
            doc_file = io.BytesIO(doc_bytes)
            doc = Document(doc_file)
            doc_text = '\n'.join([para.text for para in doc.paragraphs])
            matches = re.findall(keyword, doc_text, re.IGNORECASE)
            if matches:
                results.append(f"{key} contains the keyword {keyword} {len(matches)} times.")
            else:
                results.append(f"{key} does not contain the keyword {keyword}.")

# AWS S3 PDF FILES IMPLEMENTATION
def search_pdf_files(bucket_name, keyword, results):
    response = client.list_objects_v2(Bucket=bucket_name)
    for obj in response['Contents']:
        key = obj['Key']
        if key.endswith(".pdf"):
            response = client.get_object(Bucket=bucket_name, Key=key)
            pdf_bytes = response['Body'].read()
            pdf_file = io.BytesIO(pdf_bytes)
            pdf = PyPDF2.PdfFileReader(pdf_file)
            pdf_text = ""
            for page in range(pdf.numPages):
                    pdf_text += pdf.getPage(page).extractText()
            matches = re.findall(keyword, pdf_text, re.IGNORECASE)
            if matches:
                results.append(f"{key} contains the keyword {keyword} {len(matches)} times.")
            else:
                results.append(f"{key} does not contain the keyword {keyword}.")
                
# SEARCH route
@app.route('/search', methods=['GET', 'POST'])
def search():
    keyword = request.form['keyword']
    results = []
    search_text_files(bucket_name, keyword, results)
    search_pdf_files(bucket_name, keyword, results)
    search_doc_files(bucket_name, keyword, results)
    return render_template('index.html', results=results)


# Running Flask web application
app.run(host='0.0.0.0', port=5000)