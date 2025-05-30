from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/convert-to-pdf', methods=['POST'])
def convert_to_pdf():
    uploaded_file = request.files['file']
    if not uploaded_file:
        return 'No file uploaded', 400

    input_path = f"/tmp/{uploaded_file.filename}"
    output_path = input_path.rsplit('.', 1)[0] + ".pdf"

    uploaded_file.save(input_path)

    subprocess.run(["unoconv", "-f", "pdf", input_path], check=True)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
