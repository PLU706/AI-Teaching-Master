# AI Teaching Program

## Overview
An interactive AI-powered educational platform that generates lessons, questions, and provides personalized learning experiences using advanced language models.

## Features
- Generate comprehensive lessons on any topic
- Create adaptive quiz questions
- AI-powered answer generation
- Interactive learning experience
- Guidance text and image support

## Prerequisites
- Python 3.8+
- Flask
- Google Gemini API Key
- pip (Python package manager)

## Installation
### For Everyone Else:
1. Clone the repository (Requires Git)
```
git clone https://github.com/PLU706/ai-teaching-program.git
cd ai-teaching-program
```

2. Run auto-open shortcut
Find the shortcut named `AI Teaching Master` and open it.
At first the web will say the website is unavaliable. Wait for a few moments and it will open.

### For Experts:
1. Clone the repository (Requires Git)
```
git clone https://github.com/PLU706/ai-teaching-program.git
cd ai-teaching-program
```

2. Create virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Set up environment variables
- Create a `.env` file
- Add your Gemini API key: `GEMINI_API_KEY=your_api_key_here`

#### Running the Application
```
python app.py
```
Navigate to `http://localhost:5000/login`

## Technologies Used
- Python
- Flask
- Google Gemini AI
- JavaScript
- jQuery
