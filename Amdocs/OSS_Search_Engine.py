from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
import os
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF for PDF generation

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

# Load Excel data
sr_df = pd.read_excel("Abhi_SE_V1.xlsx", sheet_name="SR", engine="openpyxl")
defect_df = pd.read_excel("Abhi_SE_V1.xlsx", sheet_name="Defect", engine="openpyxl")

# Workaround inventory storage
workarounds = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sr_data')
def sr_data():
    return sr_df.to_json(orient='records')

@app.route('/defect_data')
def defect_data():
    return defect_df.to_json(orient='records')

@app.route('/workarounds')
def get_workarounds():
    return jsonify(workarounds)

@app.route('/add_workaround', methods=['POST'])
def add_workaround():
    data = request.form.to_dict()
    image = request.files.get('image')
    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        data['image'] = image_path
    workarounds.append(data)
    return jsonify({'status': 'success', 'message': 'Workaround added'})

@app.route('/download_pdf/<int:index>')
def download_pdf(index):
    if index >= len(workarounds):
        return "Invalid index", 404
    wa = workarounds[index]
    pdf_path = f"workaround_{index}.pdf"
    doc = fitz.open()
    page = doc.new_page()
    text = f"Name: {wa.get('Name', '')}\nIssue: {wa.get('Issue', '')}\nCategory: {wa.get('Category', '')}\n\nDescription:\n{wa.get('Description', '')}"
    page.insert_text((72, 72), text)
    if 'image' in wa:
        rect = fitz.Rect(72, 300, 400, 500)
        page.insert_image(rect, filename=wa['image'])
    doc.save(pdf_path)
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
