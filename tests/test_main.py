from xssnotifier.main import ActiveConnections, WSHandler, MainHandler, main
import tornado.web
import json
import mock


class MockRequest:
    connection = mock.MagicMock()


class MockConnection:
    def write_message(self, message):
        pass


class TestActiveConnections:
    def test_init(self):
        ac = ActiveConnections()
        assert isinstance(ac.connections, type([]))
        assert len(ac.connections) == 0

    def test_add(self):
        ac = ActiveConnections()

        c = MockConnection()

        ac.add(c)

        assert c in ac.connections

    def test_double_add(self):
        ac = ActiveConnections()

        c = MockConnection()

        ac.add(c)
        ac.add(c)

        assert c in ac.connections
        assert len(ac.connections) == 1

    def test_remove(self):
        ac = ActiveConnections()
        c1 = MockConnection()
        c2 = MockConnection()

        ac.connections = [c1, c2]

        ac.remove(c1)

        assert c1 not in ac.connections
        assert c2 in ac.connections

    def test_double_remove(self):
        ac = ActiveConnections()

        c = MockConnection()

        ac.connections = [c]

        ac.remove(c)
        ac.remove(c)

        assert len(ac.connections) == 0

    @mock.patch('%s.MockConnection.write_message' % __name__)
    def test_write_message(self, mock_connection):
        ac = ActiveConnections()

        c = MockConnection()
        ac.connections = [c]

        ac.write_message({'key': 'value'})

        mock_connection.assert_called_once_with(json.dumps({'key': 'value'}))


class TestMainHandler:
    @mock.patch('xssnotifier.main.ActiveConnections.write_message')
    def test_write_message(self, mock_write):
        ac = ActiveConnections()
        app = tornado.web.Application()
        app.active_connections = ac
        r = MockRequest()

        r.path = '/myuser/somepath.js'
        r.uri = 'http://example.com/myuser/somepath.js'
        mh = MainHandler(app, r)

        mh.write_message()

        mock_write.assert_called_once_with({
            'user': 'myuser',
            'file': 'somepath.js',
            'uri': 'http://example.com/myuser/somepath.js'
        })

    @mock.patch('xssnotifier.main.MainHandler.write_message')
    def test_get(self, mock_write):
        ac = ActiveConnections()
        app = tornado.web.Application()
        app.active_connections = ac
        r = MockRequest()
        mh = MainHandler(app, r)

        mh.get()

        assert mock_write.call_count == 1, 'Didn\'t call handler exactly once'

    @mock.patch('xssnotifier.main.MainHandler.write_message')
    def test_post(self, mock_write):
        ac = ActiveConnections()
        app = tornado.web.Application()
        app.active_connections = ac
        r = MockRequest()
        mh = MainHandler(app, r)

        mh.post()

        assert mock_write.call_count == 1, 'Didn\'t call handler exactly once'


class TestWSHandlers:
    def test_check_origin(self):
        ac = ActiveConnections()
        app = tornado.web.Application()
        app.active_connections = ac
        r = MockRequest()
        wh = WSHandler(app, r)
        assert wh.check_origin(None)
        assert wh.check_origin(False)

    def test_con_close(self):
        ac = ActiveConnections()
        app = tornado.web.Application()
        app.active_connections = ac
        r = MockRequest()
        wh = WSHandler(app, r)
        ac.connections.append(wh)

        wh.on_close()

        assert wh not in ac.connections

    def test_open_connection(self):
        ac = ActiveConnections()
        app = tornado.web.Application()
        app.active_connections = ac
        r = MockRequest()
        wh = WSHandler(app, r)

        wh.open()

        assert wh in ac.connections


@mock.patch('tornado.web.Application.listen')
@mock.patch('tornado.platform.epoll.EPollIOLoop.start')
def test_main(mock_start, mock_listen):
    main()

    assert mock_listen.call_count == 1, 'Not listening once'
    assert mock_start.call_count == 1, 'Not started once'
