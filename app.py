import pycountry
from flask import Flask, render_template, request, jsonify
from google import genai  # Modern Google AI SDK

app = Flask(__name__)


GEMINI_API_KEY = "AIzaSyARQS_zDlxP8nIgtIEmaFSnMBM4onNB8gU"

# Initialize the Google Gen AI client
client = genai.Client(api_key=GEMINI_API_KEY)

@app.route('/')
def index():
    # Automatically fetch all official ISO world languages with 2-letter codes
    languages_list = sorted([
        {'code': lang.alpha_2, 'name': lang.name}
        for lang in pycountry.languages if hasattr(lang, 'alpha_2')
    ], key=lambda x: x['name'])
    return render_template('index.html', languages=languages_list)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    target_lang = data.get('target_lang')
    text = data.get('text')

    if not text or not target_lang:
        return jsonify({"error": "Missing input text or target language"}), 400

    # The prompt is designed to let the AI automatically detect the source language
    prompt = (
        f"Detect the source language of the text below and translate it into {target_lang}. "
        f"Output ONLY the translated text without any explanations: {text}"
    )

    try:
        # Using Gemini 2.0 Flash for high speed and accuracy
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return jsonify({"translated": response.text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run with debug=True to see errors during development
    app.run(debug=True)