package main

import (
	"crypto/md5"
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

var logger = log.Default()
var key = os.Getenv("KEY")
var flag = os.Getenv("FLAG")
var puzzlePath = "/puzzle/"
var seed = make([]byte, 16)

func main() {
	_, err := rand.Read(seed)
	if err != nil {
		panic(err)
	}

	http.HandleFunc("/puzzle/{piece}", func(w http.ResponseWriter, r *http.Request) {
		piece := r.PathValue("piece")

		opening, err := findAuthHeader(r.Header)
		if err != nil {
			returnError(w, err)
			return
		}

		solution := computeSolution(piece)
		if opening != solution {
			returnError(w, fmt.Errorf("Opening %s for request %s was wrong.", opening, piece))
			return
		}

		content, err := loadPiece(piece)
		if err != nil {
			returnError(w, err)
			return
		}

		logger.Println("Successful request for", piece, "returning", content)

		w.Header().Add("ETag", computeETag(piece))
		if piece == "flag" {
			// Catmaster: You thought it would be that easy?
			w.Header().Add("Cache-Control", "no-cache")
		}

		_, err = w.Write([]byte(content))
		if err != nil {
			logger.Println(err)
		}
	})

	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("I'm alive!"))
	})

	logger.Fatalln(http.ListenAndServe(":1234", nil))
}

func returnError(w http.ResponseWriter, err error) {
	logger.Println(err)
	w.WriteHeader(http.StatusBadRequest)
	w.Write([]byte(err.Error()))
}

func findAuthHeader(h http.Header) (string, error) {
	for _, values := range h {
		for _, value := range values {
			method, opening, found := strings.Cut(value, " ")
			if found && method == "MD5" {
				return opening, nil
			}
		}
	}
	return "", errNoAuthHeader
}

var errNoAuthHeader = fmt.Errorf("Auth header missing")

func computeSolution(n string) string {
	challenge := "puzzle-piece"
	solutionBytes := md5.Sum([]byte(challenge + n + key))
	return hex.EncodeToString(solutionBytes[:])
}

func loadPiece(p string) ([]byte, error) {
	if p == "flag" {
		return []byte(flag), nil
	}

	return os.ReadFile(filepath.Join(puzzlePath, p))
}

func computeETag(p string) string {
	etagBytes := md5.Sum(append([]byte(p), seed...))
	return hex.EncodeToString(etagBytes[:])
}
