import datetime
import io
import socket
import Xlib.display
import mss
import pyautogui

import tornado.ioloop
import tornado.locks
import tornado.template
import tornado.web
import tornado.websocket
from PIL import Image

resolution = Xlib.display.Display().screen().root.get_geometry()
WIDTH = resolution.width
HEIGHT = resolution.height

PORT_NUMBER = 50000


def take_ss():
    with mss.mss() as sct:
        rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}
        sct_img = sct.grab(rect)

        byte_arr = io.BytesIO()
        img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

        img.save(byte_arr, format='PNG')
    return byte_arr.getvalue()


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(".")
        self.write(loader.load("client/index.html").generate())


class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('Connection opened...')
        self.write_message("size {} {}".format(WIDTH, HEIGHT))
        self.send_ss()

    def on_message(self, message):
        splitted = message.split(" ")
        if splitted[0] == "key":
            keys = splitted[1:]
            print("---{} pressed---".format(" ".join([item for item in keys])))
            pyautogui.hotkey(*keys)
        elif splitted[0] == "mouse":
            button = int(splitted[1].lower()) + 1
            print("---{} mouse button pressed ---".format(button))
            pyautogui.click(button=button)
        elif splitted[0] == 'move':
            x = float(splitted[1])
            y = float(splitted[2])
            print("---Mouse at ({},{})---".format(x, y))
            pyautogui.moveTo(x, y)

    def on_close(self):
        print('Connection closed...')


    def send_ss(self):
        self.write_message(take_ss(), binary=True)
        tornado.ioloop.IOLoop.current().add_timeout(datetime.timedelta(milliseconds=200), self.send_ss)


application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/', MainHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./client"}),
])

if __name__ == "__main__":
    print("{}:{}".format(get_ip(), PORT_NUMBER))
    application.listen(PORT_NUMBER)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()

