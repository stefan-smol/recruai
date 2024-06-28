from flask import Flask, request, render_template
from embeddings import screen_resumes
from PyPDF2 import PdfReader
import os
import io

app = Flask(__name__)


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/screen', methods=['POST'])
def screen():
    job_description_file = request.files['job_description']
    resume_file = request.files['resume']

    if not job_description_file or not resume_file:
        return render_template('index.html', error="Job description and resume are required.")

    job_description = extract_text_from_pdf(job_description_file)
    resume = extract_text_from_pdf(resume_file)

    results = screen_resumes(job_description, [resume])
    return render_template('results.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
