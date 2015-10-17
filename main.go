package main

import (
	"log"
	"net/http"
)

func main() {
	log.Println("Starting server...")

	h := newHandler()
	go h.run()

	http.Handle("/", HttpRequestHandler{h: h})
	http.Handle("/ws", WsHandler{h: h})
	log.Fatal(http.ListenAndServe(":8080", nil))
}
