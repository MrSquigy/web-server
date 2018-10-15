import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from subprocess import Popen, PIPE

from cases import *

PORT = 80

class RequestHandler(BaseHTTPRequestHandler):

    error_page = "<html>\n<body>\n<h1>Error accessing {path}</h1>\n<p>{msg}</p>\n</body>\n</html>"
    listing_page = "<html>\n<body>\n<ul>\n{0}\n</ul>\n</body>\n</html>"
    Cases = [case_no_file(), case_cgi_file(), case_existing_file(), case_directory_index_file(), case_directory_no_index_file(), case_always_fail()]

    def do_GET(self):
        try:
            self.full_path = os.getcwd() + self.path

            for case in self.Cases:
                if case.test(self):
                    case.act(self)
                    break
        except Exception as msg:
            self.handle_error(msg)

    def handle_error(self, msg):
        content = self.error_page.format(path = self.path, msg = msg).encode()
        self.send_content(content, 404)
    
    def send_content(self, content, status = 200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def list_dir(self, full_path):
        try:
            entries = os.listdir(full_path)
            bullets = ['<li>%s</li>' % e for e in entries if not e.startswith('.')]
            page = self.listing_page.format('\n'.join(bullets)).encode()
            self.send_content(page)
        except OSError as msg:
            msg = "'%s' cannot be listed: %s" %(self.path, msg)
            self.handle_error(msg)

    def run_cgi(self, full_path):
        cmd = "python " + full_path
        with Popen(cmd, stdout = PIPE) as proc:
            data = proc.stdout.read()

        self.send_content(data)

if __name__ == '__main__':
    serverAddress = ('', PORT)
    server = HTTPServer(serverAddress, RequestHandler)

    print(time.asctime(), "Server Started")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    
    print(time.asctime(), "Server Stopped")
    server.server_close()