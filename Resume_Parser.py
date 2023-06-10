import flask
from flask import Flask, request, render_template, send_from_directory, redirect
import PyPDF2
from docx import Document
import io
import os
import time
import boto3
from dotenv import load_dotenv

load_dotenv()

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
secret_access_key = os.environ.get('SECRET_ACCESS_KEY')
bucket_name = os.environ.get('BUCKET_NAME')

print(bucket_name)

directory = os.path.join(os.getcwd(), 'resumes')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
