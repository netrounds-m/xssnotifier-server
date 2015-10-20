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
        # TODO: Do this in a separate thread
        for c in self.connections:
            c.write_message(json.dumps(message))


class MainHandler(tornado.web.RequestHandler):
    def write_message(self):
        path = self.request.path
        path_parts = path.split('/')
        if len(path_parts) <= 2:
            return

        user = path_parts[1]
        file_name = path_parts[2]

        self.application.active_connections.write_message({
            'user': user,
            'file': file_name,
            'uri': self.request.uri,
            # TODO: Include headers
            # 'headers': self.request.headers.get_all(),
        })

    def get(self):
        self.write_message()

    def post(self):
        self.write_message()


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
