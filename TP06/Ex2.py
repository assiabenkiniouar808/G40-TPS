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
if __name__ == "__main__":
    html = """<html>
<body>
<h1>Bonjour</h1>
</body>
</html>"""

    rep = format_http_response(
        1,
        200,
        "OK",
        {
            "Server": "PythonTPServer",
            "Content-Type": "text/html; charset=utf-8",
            "Content-Length": str(len(html.encode("utf-8")))
        },
        html
    )

    print(rep)