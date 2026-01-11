# K-Link 🔗

A versatile web application built with Flask that provides document conversion and translation services powered by Google's Gemini AI.

## Features

### 📄 File Converter
Convert between various file formats: 
- **PDF to DOCX** - Extract text from PDF files and convert to Word documents
- **DOCX to XLSX** - Extract tables from Word documents to Excel spreadsheets
- **Image to PDF** - Convert JPG, JPEG, and PNG images to PDF format

### 🌐 Translator
AI-powered translation service supporting multiple languages using Google's Gemini API. 

## Tech Stack

- **Backend**: Flask (Python)
- **AI Integration**: Google Gemini API
- **Document Processing**:
  - pypdf - PDF reading and processing
  - python-docx - Word document handling
  - pandas - Excel file operations
  - Pillow (PIL) - Image processing
- **Frontend**: HTML templates (in `/templates` directory)
- **Static Assets**: CSS/JS files (in `/static` directory)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Krishmal2004/K-Link.git
cd K-Link
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install flask google-generativeai pypdf python-docx pandas pillow pycountry
```

4. Set up your API key:
   - Get a Gemini API key from [Google AI Studio](https://aistudio.google.com)
   - Replace the API key in `app.py` with your own key

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to: 
```
http://localhost:5000
```

3. Choose your desired service:
   - **Translator** - `/translator` - Translate text between languages
   - **File Converter** - `/converter` - Convert documents between formats

## Project Structure

```
K-Link/
├── app.py              # Main Flask application
├── templates/          # HTML templates
│   ├── index.html
│   ├── translator.html
│   └── file_convertor.html
├── static/            # CSS, JavaScript, and static assets
├── uploads/           # Temporary storage for uploaded files
└── __pycache__/       # Python cache files
```

## API Endpoints

- `GET /` - Home page
- `GET /translator` - Translation interface
- `GET /converter` - File conversion interface
- `POST /convert` - Handle file conversion requests

## Supported Languages

The translator supports multiple languages using ISO 639-1 language codes, powered by the `pycountry` library.

## Security Notes

⚠️ **Important**: The API key in the current code is for demonstration purposes only. Make sure to: 
- Generate your own API key
- Use environment variables for sensitive data
- Never commit API keys to version control

## Future Enhancements

- [ ] Add more file format support
- [ ] Implement batch file processing
- [ ] Add user authentication
- [ ] Cloud storage integration
- [ ] Progress indicators for large files
- [ ] Download history tracking

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License. 

## Author

**Krishmal2004**
- GitHub: [@Krishmal2004](https://github.com/Krishmal2004)

## Acknowledgments

- Google Gemini API for AI-powered translation
- Flask framework for web application structure
- Open-source libraries for document processing
```
