import tornado.ioloop
import tornado.web
import tornado.websocket
import json


class ActiveConnections:
    def __init__(self):
        self.connections = []

    def add(self, connection):
        if connection not in self.connections:
            self.connections.append(connection)

    def remove(self, connection):
        if connection in self.connections:
            self.connections.remove(connection)

    def write_message(self, message):
        for c in self.connections:
            c.write_message(json.dumps(message))


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
        self.application.active_connections.write_message({'key': 'value'})


class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.application.active_connections.add(self)

    def on_close(self):
        self.application.active_connections.remove(self)

application = tornado.web.Application([
    (r"/ws/", WSHandler),
    (r"/.*", MainHandler),
])

if __name__ == "__main__":
    application.active_connections = ActiveConnections()
    application.listen(8080)
    tornado.ioloop.IOLoop.current().start()
