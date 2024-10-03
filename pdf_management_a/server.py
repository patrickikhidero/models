import http.server
import socketserver
import urllib.parse
import json
import os
import hashlib
from http import HTTPStatus

PORT = 8000
USERS_FILE = 'users.json'
PDFS_FILE = 'pdfs.json'

# Simple in-memory session for demonstration
sessions = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/':
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(open('templates/login.html', 'rb').read())
        elif parsed_path.path == '/register':
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(open('templates/register.html', 'rb').read())
        elif parsed_path.path.startswith('/static/'):
            super().do_GET()
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "File Not Found")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        form_data = urllib.parse.parse_qs(body.decode())
        
        if self.path == '/login':
            username = form_data['username'][0]
            password = form_data['password'][0]
            if self.authenticate(username, password):
                session_id = os.urandom(16).hex()
                sessions[session_id] = username
                self.send_response(HTTPStatus.OK)
                self.send_header('Set-Cookie', f'session_id={session_id}')
                self.end_headers()
                self.redirect_to_dashboard(username)
            else:
                self.send_error(HTTPStatus.UNAUTHORIZED, "Invalid credentials")
        
        elif self.path == '/register':
            username = form_data['username'][0]
            password = form_data['password'][0]
            role = 'admin'  # Default role
            if self.register_user(username, password, role):
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"Registered successfully. Please login.")
            else:
                self.send_error(HTTPStatus.CONFLICT, "Username already exists")

        elif self.path == '/upload':
            if self.is_admin():
                self.handle_pdf_upload(form_data)
            else:
                self.send_error(HTTPStatus.FORBIDDEN, "Access denied")

    def authenticate(self, username, password):
        with open(USERS_FILE, 'r') as file:
            users = json.load(file)
        hashed_password = hash_password(password)
        return username in users and users[username]['password'] == hashed_password

    def register_user(self, username, password, role):
        with open(USERS_FILE, 'r+') as file:
            users = json.load(file)
            if username not in users:
                users[username] = {'password': hash_password(password), 'role': role}
                file.seek(0)
                json.dump(users, file)
                return True
        return False

    def is_admin(self):
        session_id = self.get_cookie('session_id')
        if session_id and session_id in sessions:
            username = sessions[session_id]
            with open(USERS_FILE, 'r') as file:
                users = json.load(file)
            return users.get(username, {}).get('role') == 'admin'
        return False

    def handle_pdf_upload(self, form_data):
        # Simplified PDF upload handling
        file_item = form_data['pdf'][0]
        if file_item.filename:
            filename = os.path.basename(file_item.filename)
            with open(os.path.join('pdfs', filename), 'wb') as f:
                f.write(file_item.file.read())
            self.update_pdfs_json(filename, form_data['title'][0])
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"PDF uploaded successfully.")
        else:
            self.send_error(HTTPStatus.BAD_REQUEST, "No file uploaded")

    def update_pdfs_json(self, filename, title):
        pdf_entry = {"filename": filename, "title": title, "upload_date": str(datetime.date.today())}
        with open(PDFS_FILE, 'r+') as file:
            data = json.load(file)
            data.append(pdf_entry)
            file.seek(0)
            json.dump(data, file)

    def redirect_to_dashboard(self, username):
        # Assuming user role check for dashboard redirection
        with open(USERS_FILE, 'r') as file:
            users = json.load(file)
        if users[username]['role'] == 'admin':
            self.path = '/admin_dashboard.html'
        else:
            self.path = '/student_dashboard.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def get_cookie(self, name):
        cookies = self.headers.get('Cookie')
        if cookies:
            for cookie in cookies.split(';'):
                key, value = cookie.strip().split('=')
                if key == name:
                    return value
        return None

Handler = SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()