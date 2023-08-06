def say_hello_class():
    import http.server
    import socketserver
    import time

    PORT = 8080

    class MyHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('<html><body>', 'utf-8'))
            self.wfile.write(bytes(f'<p>The current time is: {time.strftime("%H:%M:%S")}</p>', 'utf-8'))
            self.wfile.write(bytes('</body></html>', 'utf-8'))

    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Server started at localhost:{PORT}")
        httpd.serve_forever()
