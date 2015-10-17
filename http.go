package main

import (
	"encoding/json"
	"html"
	"log"
	"net/http"
	"strings"
)

type HttpRequestHandler struct {
	h *Handler
}

func (hrh HttpRequestHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	path := html.EscapeString(r.URL.Path)
	parts := strings.Split(path, "/")

	if len(parts) < 2 {
		return
	}

	user := parts[1]

	if strings.Compare(user, "favicon.ico") == 0 {
		return
	}

	file := parts[2]

	m := Message{r.Method, user, file}
	go hrh.SendMessage(m)
	go hrh.LogMessage(m)
}

func (hrh HttpRequestHandler) LogMessage(m Message) {
	log.Println(
		m.Method,
		m.User,
		m.File,
	)
}

func (hrh HttpRequestHandler) SendMessage(m Message) {
	j, err := json.Marshal(m)
	if err != nil {
		log.Fatal(err)
		return
	}

	for c := range hrh.h.cons {
		c.send <- j
	}
}
