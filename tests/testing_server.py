"""
Minimal anaconda.cloud implementation for testing.
"""
import threading
import wsgiref.simple_server
import wsgiref.util


class App:
    def __call__(self, environ, start_response):
        request_path = wsgiref.util.request_uri(environ, include_query=False)
        if "/t/" in request_path:
            status = "200 OK"
        else:
            status = "403 Forbidden"
        response_body = "Request method: %s" % environ["REQUEST_METHOD"]
        response_headers = [
            ("Content-Type", "text/plain"),
            ("Content-Length", str(len(response_body))),
        ]
        start_response(status, response_headers)
        return [response_body.encode()]


def run_server():
    app = App()  # wsgiref.types added in 3.11
    server = wsgiref.simple_server.make_server("127.0.0.1", 50565, app)  # type: ignore
    address, port = server.socket.getsockname()
    print("Serve at", server.socket.getsockname())
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return "http://%s:%s" % (address, port)


if __name__ == "__main__":
    run_server()
    import time

    time.sleep(300)
