
from flask import Flask, request, send_file, abort
import subprocess
import os
import tempfile

app = Flask(__name__)

@app.route('/convert-to-pdf', methods=['POST'])
def convert_to_pdf():
    if 'file' not in request.files:
        return abort(400, "No file part")

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return abort(400, "No selected file")

    with tempfile.TemporaryDirectory() as tmpdirname:
        input_path = os.path.join(tmpdirname, uploaded_file.filename)
        uploaded_file.save(input_path)

        output_path = os.path.join(tmpdirname, "output.pdf")

        try:
            subprocess.run(['unoconv', '-f', 'pdf', '-o', output_path, input_path], check=True)
        except subprocess.CalledProcessError:
            return abort(500, "Conversion failed")

        return send_file(output_path, as_attachment=True, download_name="converted.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
