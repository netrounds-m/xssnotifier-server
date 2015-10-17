package main

import (
	"github.com/gorilla/websocket"
	"log"
	"net/http"
)

type connection struct {
	ws   *websocket.Conn
	send chan []byte
	h    *Handler
}

type conpair struct {
	c *connection
	d chan bool
}

type Message struct {
	Method string
	User   string
	File   string
}

func (c *connection) reader() {
	for {
		_, _, err := c.ws.ReadMessage()
		if err != nil {
			break
		}
	}
	c.ws.Close()
}

func (c *connection) writer() {
	for message := range c.send {
		err := c.ws.WriteMessage(websocket.TextMessage, message)
		if err != nil {
			break
		}
	}
	c.ws.Close()
}

func checkOrigin(r *http.Request) bool {
	return true
}

var upgrader = &websocket.Upgrader{ReadBufferSize: 1024, WriteBufferSize: 1024, CheckOrigin: checkOrigin}

type WsHandler struct {
	h *Handler
}

func (wsh WsHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println(err)
		return
	}
	c := &connection{send: make(chan []byte, 256), ws: ws, h: wsh.h}
	c.h.register <- &conpair{c: c, d: make(chan bool)}
	defer func() { c.h.unregister <- &conpair{c: c, d: make(chan bool)} }()
	go c.writer()
	c.reader()
}
