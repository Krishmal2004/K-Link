import os
import pycountry
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file
from google import genai
from pypdf import PdfReader
from docx import Document

app = Flask(__name__)

# SECURITY: Replace this with your actual key from Google AI Studio
GEMINI_API_KEY = "YOUR_NEW_API_KEY_HERE"
client = genai.Client(api_key=GEMINI_API_KEY)

# Ensure upload folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_languages():
    """Helper function to get sorted language list"""
    return sorted([
        {'code': lang.alpha_2, 'name': lang.name}
        for lang in pycountry.languages if hasattr(lang, 'alpha_2')
    ], key=lambda x: x['name'])


def convert_pdf_to_docx(input_path):
    """Pure Python PDF to Word conversion (No compiler needed)"""
    output_path = input_path.replace('.pdf', '.docx')
    reader = PdfReader(input_path)
    doc = Document()

    for page in reader.pages:
        text = page.extract_text()
        if text:
            doc.add_paragraph(text)

    doc.save(output_path)
    return output_path


def extract_word_to_excel(input_path):
    """Extracts tables from Word and saves to Excel"""
    output_path = input_path.replace('.docx', '.xlsx')
    doc = Document(input_path)
    all_data = []

    for table in doc.tables:
        for row in table.rows:
            all_data.append([cell.text.strip() for cell in row.cells])

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_excel(output_path, index=False, header=False)
        return output_path
    return None


@app.route('/')
def index():
    return render_template('index.html', languages=get_languages())


@app.route('/translator')
def translator():
    return render_template('translator.html', languages=get_languages())


@app.route('/converter')
def converter():
    return render_template('file_convertor.html')


@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    extension = file.filename.split('.')[-1].lower()

    try:
        if extension == 'pdf':
            output_file = convert_pdf_to_docx(file_path)
        elif extension == 'docx':
            # Defaulting Word to Excel for this specific route
            output_file = extract_word_to_excel(file_path)
            if not output_file:
                return "No tables found in Word document to convert to Excel.", 400
        else:
            return f"Conversion for .{extension} not yet implemented.", 400

        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    target_lang = data.get('target_lang')
    text = data.get('text')

    if not text or not target_lang:
        return jsonify({"error": "Missing input text"}), 400

    prompt = f"Translate the following text to {target_lang}. Output ONLY the translation: {text}"

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',  # Corrected model name
            contents=prompt
        )
        return jsonify({"translated": response.text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)