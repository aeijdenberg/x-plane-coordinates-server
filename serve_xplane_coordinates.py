#!/usr/bin/env python3

import http.server
import json
import socket
import struct
import threading
import time


class XPlaneCoordsServer(http.server.HTTPServer):
    def __init__(self, xplane_addr, listen_addr, refresh_timeout_seconds):
        self._xplane_addr = xplane_addr
        self._refresh_timeout_seconds = refresh_timeout_seconds
        self.state = {'coordinates': [0.0, 0.0]}
        threading.Thread(target=self._update_positions_forever, daemon=True).start()
        super().__init__(listen_addr, XPlaneHTTPHandler)

    def _update_positions_forever(self):
        last_recv = 0
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self._refresh_timeout_seconds)
        while True:
            # if we haven't received anything for the past N seconds
            if time.time() > (last_recv + self._refresh_timeout_seconds):
                # then re-register with x-plane
                print('No coords seen in a while, re-registering with x-plane...')
                sock.sendto(struct.pack('<4sx10s', b'RPOS', b'1'), self._xplane_addr)
            try:
                (_, dat_lon, dat_lat) = struct.unpack("<5sdd", sock.recvfrom(21)[0])
                self.state = {'coordinates': [dat_lat, dat_lon]}
                print('Received:', self.state)
                last_recv = time.time()
            except (socket.timeout):
                pass # handled in code


class XPlaneHTTPHandler(http.server.BaseHTTPRequestHandler):

    def _add_cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Max-Age', '300')
        self.send_header('Access-Control-Allow-Private-Network', 'true')

    def do_OPTIONS(self):
        self.send_response(200)
        self._add_cors()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self._add_cors()
        self.end_headers()
        self.wfile.write(json.dumps(self.server.state).encode('utf8'))


XPlaneCoordsServer(
    xplane_addr=('127.0.0.1', 49000), # where x-plane is
    listen_addr=('', 8001), # port to listen on
    refresh_timeout_seconds=5 # how often to ping x-plane until ready
).serve_forever()