from http.server import BaseHTTPRequestHandler, HTTPServer


INDEX_HTML = """<!DOCTYPE html>
<html>
<body>

<p>Bonjour</p>
<p style="font-size:50px;">C'est notre premier serveur</p>

</body>
</html>"""

ERROR_404_HTML = """<!DOCTYPE html>
<html>
<body>
<h1>404 Not Found</h1>
<p>La page demandee n'existe pas.</p>
</body>
</html>"""


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/index.html":
            body = INDEX_HTML
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
        else:
            body = ERROR_404_HTML
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))


HOST = "127.0.0.1"
PORT = 9090

server = HTTPServer((HOST, PORT), MyHandler)
print(f"Serveur en ecoute sur http://{HOST}:{PORT}")
server.serve_forever()