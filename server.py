from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import urllib.parse as urlparse
import socket

import pyautogui


PORT_NUMBER = 50000
FILE_NAME = "screenshot.png"


# This class will handles any incoming request from
# the browser
class HTTPHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):

        parsed = urlparse.urlparse(self.path)
        args = urlparse.parse_qs(parsed.query)
        try:
            x = float(args['x'][0])
            y = float(args['y'][0])
            print("---Mouse at ({},{})---".format(x, y))
            pyautogui.moveTo(x, y)
        except KeyError:
            pass
        try:
            if args['click'][0] == "true":
                pyautogui.click()
        except KeyError:
            pass

        try:
            key = args['key'][0].lower()
            print("---{} pressed---".format(key))
            pyautogui.press(key)

        except KeyError:
            pass

        self.path = parsed.path
        mimetype = 'text/html'
        if self.path == "/" + FILE_NAME:
            take_ss()
            mimetype = 'image/png'
        else:
            if self.path == "/":
                self.path = "/index.html"
            self.path = "/client" + self.path
            if self.path.endswith(".html"):
                mimetype='text/html'
            if self.path.endswith(".css"):
                mimetype = 'text/css'
            if self.path.endswith(".js"):
                mimetype = 'application/javascript'
            if self.path.endswith(".png"):
                mimetype ='image/png'

        self.send_response(200)
        self.send_header('Content-type', mimetype)
        self.end_headers()
        f = open(curdir + sep + self.path, 'rb')
        self.wfile.write(f.read())
        f.close()
        return

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def take_ss():
    pyautogui.screenshot(FILE_NAME)


def main():
    server = None
    try:
        # Create a web server and define the handler to manage the
        # incoming request
        server = HTTPServer(('', PORT_NUMBER), HTTPHandler)
        print('---Current desktop is located at {}:{}---'.format(get_ip(), PORT_NUMBER))
        # Wait forever for incoming http requests
        server.serve_forever()

    except KeyboardInterrupt:
        print('---^C received, shutting down the web server---')
        running = False
        server.socket.close()


if __name__ == '__main__':
    main()
