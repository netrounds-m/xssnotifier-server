package main

import (
	"testing"
)

func TestUnregister(t *testing.T) {
	h := newHandler()
	go h.run()

	done := make(chan bool)

	c := connection{send: make(chan []byte)}
	cp := conpair{c: &c, d: done}

	h.cons[&c] = true

	h.unregister <- &cp

	<-done

	if len(h.cons) != 0 {
		t.Errorf("Didn't remove connecton")
	}
}

func TestRegister(t *testing.T) {
	h := newHandler()
	go h.run()

	done := make(chan bool)

	c := connection{}
	cp := conpair{c: &c, d: done}

	h.register <- &cp

	<-done

	if len(h.cons) != 1 {
		t.Errorf("Didn't add connection")
	}

	if !h.cons[&c] {
		t.Errorf("Connection not added correctly")
	}
}
