#!/usr/bin/env python3
"""Minimal HTTP server from scratch (socket-level) — zero deps."""
import socket, sys, os, mimetypes
from datetime import datetime

def handle_request(request):
    lines = request.split('\r\n')
    method, path, _ = lines[0].split(' ', 2)
    if path == '/': path = '/index.html'
    if method != 'GET':
        return "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
    # Serve from current dir
    fpath = '.' + path
    if os.path.isfile(fpath):
        mime = mimetypes.guess_type(fpath)[0] or 'application/octet-stream'
        with open(fpath, 'rb') as f: body = f.read()
        return f"HTTP/1.1 200 OK\r\nContent-Type: {mime}\r\nContent-Length: {len(body)}\r\n\r\n".encode() + body
    return "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n404 Not Found"

def serve(port=8080):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port)); sock.listen(5)
    print(f"Serving on http://localhost:{port}")
    while True:
        conn, addr = sock.accept()
        data = conn.recv(4096).decode('utf-8', errors='replace')
        if data:
            resp = handle_request(data)
            conn.sendall(resp if isinstance(resp, bytes) else resp.encode())
        conn.close()

def test():
    req = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
    resp = handle_request(req)
    assert "404" in str(resp) or "200" in str(resp)
    req2 = "POST /data HTTP/1.1\r\n\r\n"
    assert "405" in handle_request(req2)
    print("HTTP server handler tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
        serve(port)
    else: test()
