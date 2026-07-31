#!/usr/bin/env python3

"""A simple HTTP server with upload, download and directory listing.

Compatible with Python 3.12.

Features
--------
* Browse directories (auto-generated listing).
* Download / view files.
* Upload files through a small HTML form (multipart/form-data).

It is built on top of :class:`http.server.SimpleHTTPRequestHandler`, so the
GET / HEAD behaviour (directory listing and file downloading) is inherited
from the standard library and only the POST (upload) part is added here.

Usage
-----
    python3 http_server_with_upload.py [port] [directory]

    # examples
    python3 http_server_with_upload.py            # port 8000, current dir
    python3 http_server_with_upload.py 8080       # port 8080, current dir
    python3 http_server_with_upload.py 8080 /tmp  # port 8080, serve /tmp
"""

import argparse
import html
import http.server
import io
import os
import socketserver
import sys
from email.parser import BytesParser
from email.policy import default as default_policy

__version__ = "1.0"
__all__ = ["UploadHTTPRequestHandler"]
__author__ = "smilejay"
__home_page__ = "https://smilejay.cn/"


class UploadHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Serve a directory and accept file uploads.

    GET/HEAD are handled by the parent class (directory listing + file
    download).  POST accepts ``multipart/form-data`` uploads and stores the
    files into the directory that the URL points to.
    """

    server_version = "SimpleUploadHTTP/" + __version__

    # ------------------------------------------------------------------ #
    # Directory listing: reuse the parent implementation but inject a
    # small upload form at the top so uploading is possible from any page.
    # ------------------------------------------------------------------ #
    def list_directory(self, path):
        try:
            file_list = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None
        file_list.sort(key=lambda a: a.lower())

        displaypath = html.escape(self.path, quote=False)
        enc = sys.getfilesystemencoding()

        parts = [
            "<!DOCTYPE html>",
            "<html>\n<head>",
            '<meta charset="%s">' % enc,
            "<title>Directory listing for %s</title>" % displaypath,
            "</head>\n<body>",
            "<h2>Directory listing for %s</h2>" % displaypath,
            "<hr>",
            # upload form
            '<form ENCTYPE="multipart/form-data" method="post">',
            '<input name="file" type="file" multiple/>',
            '<input type="submit" value="Upload"/>',
            "</form>",
            "<hr>\n<ul>",
        ]
        for name in file_list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
            parts.append(
                '<li><a href="%s">%s</a></li>'
                % (
                    html.escape(self._quote(linkname), quote=True),
                    html.escape(displayname, quote=False),
                )
            )
        parts.append("</ul>\n<hr>")
        parts.append(
            '<small>Powered by <a href="%s">%s</a></small>'
            % (html.escape(__home_page__), html.escape(__author__))
        )
        parts.append("</body>\n</html>")

        encoded = ("\n".join(parts) + "\n").encode(enc, "surrogateescape")
        f = io.BytesIO(encoded)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f

    @staticmethod
    def _quote(text):
        # Local import keeps the top clean; urllib.parse.quote handles the
        # percent-encoding of link targets.
        from urllib.parse import quote

        return quote(text)

    # ------------------------------------------------------------------ #
    # Upload handling
    # ------------------------------------------------------------------ #
    def do_POST(self):
        ok, message = self._handle_upload()
        body = self._render_result_page(ok, message).encode("utf-8",
                                                            "surrogateescape")
        self.send_response(200 if ok else 400)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_upload(self):
        ctype = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in ctype:
            return False, "Content-Type must be multipart/form-data."

        try:
            length = int(self.headers.get("Content-Length", 0))
        except (TypeError, ValueError):
            return False, "Invalid Content-Length."
        if length <= 0:
            return False, "Empty request body."

        # Rebuild a minimal MIME message (headers + body) and let the
        # standard email parser deal with the multipart boundaries. This is
        # far more robust than parsing the boundary stream by hand.
        raw = b"Content-Type: " + ctype.encode("utf-8") + b"\r\n\r\n"
        raw += self.rfile.read(length)

        msg = BytesParser(policy=default_policy).parsebytes(raw)
        if not msg.is_multipart():
            return False, "Malformed multipart body."

        target_dir = self.translate_path(self.path)
        if not os.path.isdir(target_dir):
            target_dir = os.path.dirname(target_dir)

        saved = []
        for part in msg.iter_parts():
            filename = part.get_filename()
            if not filename:
                continue
            filename = os.path.basename(filename)
            if not filename:
                continue
            payload = part.get_payload(decode=True)
            if payload is None:
                continue
            dest = self._unique_path(os.path.join(target_dir, filename))
            try:
                with open(dest, "wb") as out:
                    out.write(payload)
            except OSError as exc:
                return False, "Cannot write file: %s" % exc
            saved.append(os.path.basename(dest))

        if not saved:
            return False, "No file field found in the upload."
        return True, "Uploaded: %s" % ", ".join(saved)

    @staticmethod
    def _unique_path(path):
        """Avoid overwriting: append a numeric suffix if the file exists."""
        if not os.path.exists(path):
            return path
        base, ext = os.path.splitext(path)
        i = 1
        while True:
            candidate = "%s_%d%s" % (base, i, ext)
            if not os.path.exists(candidate):
                return candidate
            i += 1

    def _render_result_page(self, ok, message):
        status = "Success" if ok else "Failed"
        back = self.headers.get("Referer", "/")
        return (
            "<!DOCTYPE html>\n<html>\n<head><meta charset=\"utf-8\">"
            "<title>Upload Result</title></head>\n<body>\n"
            "<h2>Upload Result</h2>\n<hr>\n"
            "<p><strong>%s:</strong> %s</p>\n"
            '<p><a href="%s">Back</a></p>\n<hr>\n'
            '<small>Powered by <a href="%s">%s</a></small>\n'
            "</body>\n</html>\n"
            % (
                status,
                html.escape(message),
                html.escape(back),
                html.escape(__home_page__),
                html.escape(__author__),
            )
        )


class ThreadingHTTPServer(socketserver.ThreadingMixIn,
                          http.server.HTTPServer):
    """Handle each request in a new thread."""

    daemon_threads = True


def run(port=8000, directory=None):
    handler_class = UploadHTTPRequestHandler
    if directory:
        # Python 3.7+ supports the `directory` kwarg via functools.partial.
        import functools

        handler_class = functools.partial(UploadHTTPRequestHandler,
                                           directory=directory)

    server_address = ("", port)
    httpd = ThreadingHTTPServer(server_address, handler_class)
    sa = httpd.socket.getsockname()
    serve_dir = directory or os.getcwd()
    print("Serving HTTP on %s port %d (http://%s:%d/) ..."
          % (sa[0], sa[1], sa[0], sa[1]))
    print("Serving directory: %s" % serve_dir)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, shutting down.")
    finally:
        httpd.server_close()


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="A simple HTTP server with upload/download support.")
    parser.add_argument("port", nargs="?", default=8000, type=int,
                        help="port to listen on (default: 8000)")
    parser.add_argument("directory", nargs="?", default=None,
                        help="directory to serve (default: current directory)")
    args = parser.parse_args(argv)
    run(port=args.port, directory=args.directory)


if __name__ == "__main__":
    main()
