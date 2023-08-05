import http.server
import socketserver
import datetime


def start_server():
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            now = datetime.datetime.now()
            formatted_time = now.strftime("%I:%M:%S %p")
            self.wfile.write(bytes(f'The current time is {formatted_time}', 'utf-8'))

    PORT = 8080

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"serving at port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

    print("Server stopped.")
