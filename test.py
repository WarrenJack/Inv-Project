from flask import Flask, request, render_template
import pdfplumber
import re
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":
        files = request.files.getlist("file[]")
        results = []
        for file in files:
            with pdfplumber.open(file) as pdf:
                first_page = pdf.pages[0]
                text = first_page.extract_text()
                invoice_number = re.search(r'# (\d+)', text).group(1)
                results.append(f"{file.filename}: Invoice Number = {invoice_number}")
        return "<br>".join(results)
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
