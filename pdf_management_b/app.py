from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
import json
from werkzeug.utils import secure_filename
from auth import hash_password, verify_password, requires_admin
from file_manager import save_pdf, list_pdfs, get_pdf_metadata

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to check if file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET',', 'POST'])
def login():
    # Implement login logic here using auth.py
    pass

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Implement registration logic here
    pass

@app.route('/admin')
@requires_admin
def admin_dashboard():
    pdfs = list_pdfs()
    return render_template('admin_dashboard.html', pdfs=pdfs)

@app.route('/upload', methods=['POST'])
@requires_admin
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        save_pdf(filename, request.form.get('title', filename))
        return redirect(url_for('admin_dashboard'))
    return 'Invalid file type', 400

@app.route('/student')
def student_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    pdfs = list_pdfs()
    return render_template('student_dashboard.html', pdfs=pdfs)

@app.route('/view/<filename>')
def view_pdf(filename):
    if 'user_id' in session:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    return 'Unauthorized', 401

if __name__ == '__main__':
    app.run(debug=True)