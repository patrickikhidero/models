import os
import json
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

# Constants
USER_FILE = 'users.json'
UPLOAD_DIR = 'uploads'
METADATA_FILE = 'uploaded_files.json'

# Utility Functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

def load_metadata():
    if not os.path.exists(METADATA_FILE):
        return []
    with open(METADATA_FILE, 'r') as f:
        return json.load(f)

def save_metadata(metadata):
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f)

# Request Handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(open('templates/login.html', 'rb').read())
        elif parsed_path.path == '/register':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(open('templates/register.html', 'rb').read())
        elif parsed_path.path == '/admin_dashboard':
            self.handle_admin_dashboard()
        elif parsed_path.path == '/student_dashboard':
            self.handle_student_dashboard()
        elif parsed_path.path.startswith('/uploads/'):
            self.handle_pdf_request(parsed_path.path)
        else:
            self.send_error(404)

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/register':
            self.handle_registration()
        elif parsed_path.path == '/login':
            self.handle_login()
        elif parsed_path.path == '/upload':
            self.handle_file_upload()
        else:
            self.send_error(404)

    def handle_registration(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = parse_qs(post_data)
        username = data.get('username')[0]
        password = hash_password(data.get('password')[0])
        
        users = load_users()
        if username in users:
            self.send_error(400, "User already exists")
            return
        
        # Allow admin registration by a special username/password
        if username == "admin" and password == hash_password("admin_password"):  # Change for security
            role = 'admin'
        else:
            role = 'student'

        users[username] = {'password': password, 'role': role}
        save_users(users)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def handle_login(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = parse_qs(post_data)
        username = data.get('username')[0]
        password = hash_password(data.get('password')[0])
        
        users = load_users()
        if username in users and users[username]['password'] == password:
            self.send_response(302)
            self.send_header('Location', '/admin_dashboard' if users[username]['role'] == 'admin' else '/student_dashboard')
            self.end_headers()
        else:
            self.send_error(403, "Invalid credentials")

    def handle_admin_dashboard(self):
        uploaded_files = load_metadata()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = open('templates/admin_dashboard.html', 'rb').read().decode()
        html = html.replace('{% for file in uploaded_files %}', '\n'.join(
            f'<li><a href="/uploads/{file["title"]}">{file["title"]}</a></li>' for file in uploaded_files
        ))
        self.wfile.write(html.encode())

    def handle_student_dashboard(self):
        uploaded_files = load_metadata()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = open('templates/student_dashboard.html', 'rb').read().decode()
        html = html.replace('{% for file in uploaded_files %}', '\n'.join(
            f'<li><a href="/uploads/{file["title"]}">{file["title"]}</a></li>' for file in uploaded_files
        ))
        self.wfile.write(html.encode())

    def handle_file_upload(self):
        if self.headers['content-type'].startswith('multipart/form-data'):
            boundary = self.headers['content-type'].split('=')[1].encode()
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            parts = body.split(boundary)
            for part in parts:
                if b'filename="' in part:
                    filename = part.split(b'filename="')[1].split(b'"')[0].decode()
                    if not filename.endswith('.pdf'):
                        self.send_error(400, "Only PDF files are allowed.")
                        return
                    file_content = part.split(b'\r\n\r\n')[1].rsplit(b'\r\n', 1)[0]

                    with open(os.path.join(UPLOAD_DIR, filename), 'wb') as f:
                        f.write(file_content)

                    metadata = load_metadata()
                    metadata.append({'title': filename, 'upload_date': 'now'})  # Add relevant date handling
                    save_metadata(metadata)
                    
                    self.send_response(302)
                    self.send_header('Location', '/admin_dashboard')
                    self.end_headers()
                    return
        self.send_error(400, "Invalid file upload.")

    def handle_pdf_request(self, path):
        self.send_response(200)
        self.send_header('Content-type', 'application/pdf')
        self.end_headers()
        with open('.' + path, 'rb') as file:
            self.wfile.write(file.read())

# Main Function
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    run()