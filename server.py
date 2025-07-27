from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import os

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        cookies = self.headers.get('Cookie', '')
        is_logged_in = 'is_logged_in=true' in cookies

        if self.path == '/' or self.path == '/index.html':
            if not is_logged_in:
                self.send_response(302)
                self.send_header('Location', '/login')
                self.end_headers()
                return
            else:
                self.path = '/index.html'

        elif self.path == '/logout':
            self.send_response(302)
            self.send_header('Set-Cookie', 'is_logged_in=false; Max-Age=0')
            self.send_header('Location', '/login')
            self.end_headers()
            return

        elif self.path == '/login':
            self.path = '/login.html'

        return super().do_GET()

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = parse_qs(post_data)

            username = data.get('username', [''])[0]
            password = data.get('password', [''])[0]

            akun_valid = {
                'admin': '123',
                'user1': 'abc'
            }

            if username in akun_valid and akun_valid[username] == password:
                self.send_response(302)
                self.send_header('Set-Cookie', 'is_logged_in=true')
                self.send_header('Location', '/')
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<h1>Login Gagal</h1><p>Username atau password salah.</p>')
        else:
            self.send_error(404, "Halaman tidak ditemukan")

# Jalankan server
port = 8000
server_address = ('', port)
httpd = HTTPServer(server_address, MyHandler)
print(f"Server berjalan di http://localhost:{port}")
httpd.serve_forever()
