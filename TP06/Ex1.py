def format_http_request(method, url, version, headers, body):
    allowed_methods = ["GET", "POST", "PUT", "DELETE", "HEAD"]
    if method not in allowed_methods:
        raise ValueError("Méthode HTTP invalide")

    if version == 1:
        http_version = "HTTP/1.1"
    elif version == 2:
        http_version = "HTTP/2.0"
    else:
        raise ValueError("Version HTTP invalide")

    request = f"{method} {url} {http_version}\r\n"

    for key, value in headers.items():
        request += f"{key}: {value}\r\n"

    request += "\r\n"
    request += body

    return request

if __name__ == "__main__":
    req = format_http_request(
        "GET",
        "/index.html",
        1,
        {
            "Host": "localhost:8000",
            "User-Agent": "PythonClient",
            "Accept": "text/html"
        },
        ""
    )

    print(req)