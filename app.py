from flask import Flask, request, send_file
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/convert-to-pdf', methods=['POST'])
def convert_to_pdf():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        # LibreOffice/unoconv kullanarak dönüştürme
        output_path = os.path.join(OUTPUT_FOLDER, os.path.splitext(file.filename)[0] + '.pdf')
        result = subprocess.run(['unoconv', '-f', 'pdf', '-o', output_path, filepath], capture_output=True, text=True)

        if result.returncode != 0:
            return f"Conversion failed:\n{result.stderr}", 500

        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return f"Exception occurred: {str(e)}", 500
