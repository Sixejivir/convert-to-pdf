from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/convert-to-pdf', methods=['POST'])
def convert_to_pdf():
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return 'No file uploaded', 400

    input_path = f"/tmp/{uploaded_file.filename}"
    output_path = input_path.rsplit('.', 1)[0] + ".pdf"

    uploaded_file.save(input_path)

    try:
        result = subprocess.run(
            ["unoconv", "-f", "pdf", input_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print("Unoconv output:", result.stdout)
        print("Unoconv error (if any):", result.stderr)

        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            return "PDF conversion failed or resulted in empty file.", 500

        return send_file(output_path, as_attachment=True)

    except subprocess.CalledProcessError as e:
        print("Error during conversion:", e.stderr)
        return f"Conversion failed: {e.stderr}", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
