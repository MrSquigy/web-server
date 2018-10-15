import time
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 80

class RequestHandler(BaseHTTPRequestHandler):
    # Handle HTTP requests by returning a fixed 'page'

    # Page to send back - encode to convert string to bytes
    page = '<html>\n<body>\n<p>Hello, world!</p>\n</body>\n</html>'.encode()

    # Handle a GET request
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(self.page)))
        self.end_headers()
        self.wfile.write(self.page)

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