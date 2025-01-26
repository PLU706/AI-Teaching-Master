from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import markdown
import os
from dotenv import load_dotenv
import google.generativeai as genai
import base64
from io import BytesIO
from PIL import Image
import PyPDF2

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Set the password here
PASSWORD = "study123!"

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Incorrect Password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

def process_uploaded_files(guidance_image, guidance_pdf):
    image_description = ""
    pdf_content = ""
    
    if guidance_image:
        image_data = base64.b64decode(guidance_image.split(',')[1])
        image = Image.open(BytesIO(image_data))
        image_description = "An uploaded image is provided as additional context."
    
    if guidance_pdf:
        pdf_data = base64.b64decode(guidance_pdf.split(',')[1])
        pdf_file = BytesIO(pdf_data)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        if len(pdf_reader.pages) > 1000:
            return None, "PDF exceeds 1000 pages limit."
        
        for page in pdf_reader.pages:
            pdf_content += page.extract_text() + "\n"
    
    return image_description, pdf_content

@app.route('/generate_lesson', methods=['POST'])
def generate_lesson():
    topic = request.form['topic']
    guidance_text = request.form.get('guidance_text', '')
    guidance_image = request.form.get('guidance_image', '')
    guidance_pdf = request.form.get('guidance_pdf', '')
    
    image_description, pdf_content = process_uploaded_files(guidance_image, guidance_pdf)
    if isinstance(image_description, str) and image_description.startswith("PDF exceeds"):
        return jsonify({'error': image_description}), 400
    
    lesson_prompt = f"Create a comprehensive lesson about {topic}. Include key points and explanations. Use markdown formatting."
    if guidance_text:
        lesson_prompt += f"\n\nUse the following text as additional guidance or course material:\n{guidance_text}"
    if image_description:
        lesson_prompt += f"\n\nAdditional context from an image: {image_description}"
    if pdf_content:
        lesson_prompt += f"\n\nAdditional context from a PDF:\n{pdf_content[:1000]}..."  # Truncate if too long
    
    lesson_response = model.generate_content(lesson_prompt)
    lesson_content = markdown.markdown(lesson_response.text)
    
    return jsonify({'lesson': lesson_content})

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    topic = request.form['topic']
    guidance_text = request.form.get('guidance_text', '')
    guidance_image = request.form.get('guidance_image', '')
    guidance_pdf = request.form.get('guidance_pdf', '')
    
    image_description, pdf_content = process_uploaded_files(guidance_image, guidance_pdf)
    if isinstance(image_description, str) and image_description.startswith("PDF exceeds"):
        return jsonify({'error': image_description}), 400
    
    questions_prompt = f"""Create 5 open-ended questions about {topic}. 
    Format each question on a new line, starting with 'Q1.', 'Q2.', etc.
    Make sure the questions encourage thoughtful and detailed responses."""
    
    if guidance_text:
        questions_prompt += f"\n\nUse the following text as additional guidance or course material:\n{guidance_text}"
    if image_description:
        questions_prompt += f"\n\nAdditional context from an image: {image_description}"
    if pdf_content:
        questions_prompt += f"\n\nAdditional context from a PDF:\n{pdf_content[:1000]}..."  # Truncate if too long
    
    questions_response = model.generate_content(questions_prompt)
    questions = questions_response.text
    
    return jsonify({'questions': questions})

@app.route('/answer_question', methods=['POST'])
def answer_question():
    question = request.form['question']
    topic = request.form['topic']
    guidance_text = request.form.get('guidance_text', '')
    guidance_image = request.form.get('guidance_image', '')
    guidance_pdf = request.form.get('guidance_pdf', '')
    
    image_description, pdf_content = process_uploaded_files(guidance_image, guidance_pdf)
    if isinstance(image_description, str) and image_description.startswith("PDF exceeds"):
        return jsonify({'error': image_description}), 400
    
    answer_prompt = f"Answer this question about {topic}: {question}"
    if guidance_text:
        answer_prompt += f"\n\nUse the following text as additional guidance or course material:\n{guidance_text}"
    if image_description:
        answer_prompt += f"\n\nAdditional context from an image: {image_description}"
    if pdf_content:
        answer_prompt += f"\n\nAdditional context from a PDF:\n{pdf_content[:1000]}..."  # Truncate if too long
    
    answer_response = model.generate_content(answer_prompt)
    answer = markdown.markdown(answer_response.text)
    
    return jsonify({'answer': answer})

@app.route('/grade_answers', methods=['POST'])
def grade_answers():
    topic = request.form['topic']
    user_answers = request.form['answers']
    questions = request.form['questions']
    guidance_text = request.form.get('guidance_text', '')
    guidance_image = request.form.get('guidance_image', '')
    guidance_pdf = request.form.get('guidance_pdf', '')
    
    image_description, pdf_content = process_uploaded_files(guidance_image, guidance_pdf)
    if isinstance(image_description, str) and image_description.startswith("PDF exceeds"):
        return jsonify({'error': image_description}), 400
    
    grading_prompt = f"""Grade the following answers for questions about {topic}. 
    Questions:
    {questions}
    
    User Answers:
    {user_answers}
    
    Provide a detailed evaluation for each answer, including strengths and areas for improvement.
    Give a score out of 10 for each answer, and an overall percentage score at the end.
    Use markdown formatting in your response."""
    
    if guidance_text:
        grading_prompt += f"\n\nUse the following text as additional guidance or course material:\n{guidance_text}"
    if image_description:
        grading_prompt += f"\n\nAdditional context from an image: {image_description}"
    if pdf_content:
        grading_prompt += f"\n\nAdditional context from a PDF:\n{pdf_content[:1000]}..."  # Truncate if too long
    
    grading_response = model.generate_content(grading_prompt)
    grading_result = markdown.markdown(grading_response.text)
    
    return jsonify({'grading_result': grading_result})

if __name__ == '__main__':
    app.run(debug=True)
