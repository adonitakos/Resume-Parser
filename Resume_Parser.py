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

s3 = boto3.resource(
    service_name = 's3',
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key = os.environ.get('SECRET_ACCESS_KEY'),
    #bucket_name = os.environ.get('BUCKET_NAME')
)

for bucket in s3.buckets.all():
    print(bucket.name)

directory = os.path.join(os.getcwd(), 'resumes')

app = Flask(__name__)

#file upload testing
#def upload_file1():
#    file = "D:\Downloads\matttestresume1.txt"
#    s3.Bucket(bucket.name).upload_file(Filename=file, Key=file)
#    return 'File uploaded successfully'

#print all objects found in the AWS server
#for obj in s3.Bucket(bucket.name).objects.all():
#    print(obj)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    s3.Bucket(bucket.name).upload_file(Filename=file, Key=file)
    return 'File uploaded successfully'