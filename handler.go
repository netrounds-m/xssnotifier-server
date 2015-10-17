package main

import (
	"log"
)

type Runable interface {
	run()
}

type Handler struct {
	cons       map[*connection]bool
	register   chan *conpair
	unregister chan *conpair
}

func newHandler() *Handler {
	return &Handler{
		cons:       make(map[*connection]bool),
		register:   make(chan *conpair),
		unregister: make(chan *conpair),
	}
}

func (h *Handler) run() {
	log.Println("Starting run loop")
	for {
		select {
		case cp := <-h.register:
			h.cons[cp.c] = true
			cp.d <- true
		case cp := <-h.unregister:
			if _, ok := h.cons[cp.c]; ok {
				delete(h.cons, cp.c)
				close(cp.c.send)
			}
			cp.d <- true
		}
	}
}
