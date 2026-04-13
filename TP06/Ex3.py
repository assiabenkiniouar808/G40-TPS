import socket


def format_http_response(version, status_code, status_message, headers, body):
    if version == 1:
        http_version = "HTTP/1.1"
    elif version == 2:
        http_version = "HTTP/2.0"
    else:
        raise ValueError("Version HTTP invalide")

    response = f"{http_version} {status_code} {status_message}\r\n"

    for key, value in headers.items():
        response += f"{key}: {value}\r\n"

    response += "\r\n"
    response += body

    return response


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


HOST = "127.0.0.1"
PORT = 80


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Serveur en ecoute sur http://{HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print("Connexion recue de :", client_address)

    try:
        request_data = client_socket.recv(4096).decode("utf-8", errors="ignore")
        print("Requete recue :")
        print(request_data)

        lines = request_data.splitlines()

        if len(lines) == 0:
            body = ERROR_404_HTML
            response = format_http_response(
                1,
                404,
                "Not Found",
                {
                    "Server": "PythonTPServer",
                    "Content-Type": "text/html; charset=utf-8",
                    "Content-Length": str(len(body.encode("utf-8"))),
                    "Connection": "close"
                },
                body
            )
        else:
            first_line = lines[0].split()

            if len(first_line) >= 3:
                method = first_line[0]
                path = first_line[1]

                if method == "GET" and path == "/index.html":
                    body = INDEX_HTML
                    response = format_http_response(
                        1,
                        200,
                        "OK",
                        {
                            "Server": "PythonTPServer",
                            "Content-Type": "text/html; charset=utf-8",
                            "Content-Length": str(len(body.encode("utf-8"))),
                            "Connection": "close"
                        },
                        body
                    )
                else:
                    body = ERROR_404_HTML
                    response = format_http_response(
                        1,
                        404,
                        "Not Found",
                        {
                            "Server": "PythonTPServer",
                            "Content-Type": "text/html; charset=utf-8",
                            "Content-Length": str(len(body.encode("utf-8"))),
                            "Connection": "close"
                        },
                        body
                    )
            else:
                body = ERROR_404_HTML
                response = format_http_response(
                    1,
                    404,
                    "Not Found",
                    {
                        "Server": "PythonTPServer",
                        "Content-Type": "text/html; charset=utf-8",
                        "Content-Length": str(len(body.encode("utf-8"))),
                        "Connection": "close"
                    },
                    body
                )

        client_socket.sendall(response.encode("utf-8"))

    except Exception as e:
        print("Erreur :", e)

    finally:
        client_socket.close()