"""
Minimal anaconda.cloud implementation for testing.
"""

import threading
import wsgiref.simple_server
import wsgiref.util
import io

MESSAGES = io.StringIO()


class QuietHandler(wsgiref.simple_server.WSGIRequestHandler):
    def log_message(self, format, *args):
        """Log an arbitrary message (don't confuse test's stdout/stderr capture)."""
        message = format % args
        MESSAGES.write(
            "%s - - [%s] %s\n"
            % (
                self.address_string(),
                self.log_date_time_string(),
                message.translate(self._control_char_table),
            )
        )


class App:
    def __call__(self, environ, start_response):
        request_path = wsgiref.util.request_uri(environ, include_query=False)
        # require token, but disallow the invalid token
        if "/t/" in request_path and "/t/SECRET/" not in request_path:
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
    server = wsgiref.simple_server.make_server(
        "127.0.0.1", 0, app, handler_class=QuietHandler
    )  # type: ignore
    address, port = server.socket.getsockname()
    print("Serve at", server.socket.getsockname())
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return "http://%s:%s" % (address, port)


if __name__ == "__main__":
    run_server()
    import time

    time.sleep(300)
