package main

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

var client = http.DefaultClient
var logger = log.Default()
var key = os.Getenv("KEY")
var storagePath = "/storage/"

func main() {
	http.HandleFunc("/puzzle/{piece}", func(w http.ResponseWriter, r *http.Request) {
		piece := r.PathValue("piece")

		body, err := tryCache(r)
		if err != nil {
			returnError(w, err)
			return
		}
		if body != nil {
			w.Write(body)
			return
		}

		req, err := http.NewRequest("GET", fmt.Sprintf("http://localhost:5001/puzzle/%s", piece), nil)
		if err != nil {
			returnError(w, err)
			return
		}

		req.Header = r.Header
		updateHeader(req.Header, piece)

		resp, err := client.Do(req)
		if err != nil {
			returnError(w, err)
			return
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			returnError(w, fmt.Errorf("Got status %s\n", resp.Status))
			return
		}

		body, err = io.ReadAll(resp.Body)
		if err != nil {
			returnError(w, err)
			return
		}

		etag := resp.Header.Get("ETag")
		w.Header().Add("ETag", etag)

		err = tryStore(etag, resp.Header, body)
		if err != nil {
			returnError(w, err)
			return
		}

		if piece == "flag" {
			w.Write([]byte("Catmaster: It's not that simple"))
			return
		}
		_, err = w.Write(body)
		if err != nil {
			logger.Println("Passing body failed")
		}
	})

	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("I'm alive!"))
	})

	logger.Fatalln(http.ListenAndServe("localhost:1234", nil))
}

func returnError(w http.ResponseWriter, err error) {
	logger.Println(err)
	w.WriteHeader(http.StatusBadRequest)
	w.Write([]byte(err.Error()))
}

func tryCache(r *http.Request) ([]byte, error) {
	etag, err := getETag(r)
	if err != nil {
		return nil, err
	}
	if etag == "" {
		return nil, nil
	}

	// Check for a cache (cash) hit
	file, err := os.Open(filepath.Join(storagePath, etag))
	if os.IsNotExist(err) {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}

	body, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}

	return body, nil
}

func getETag(r *http.Request) (string, error) {
	r.ParseForm()
	etag := r.Form.Get("ETag") // Is this how you use ETags?

	// Catmaster: Can't make this too easy for you ;P
	path := filepath.Join(storagePath, etag)
	for _, prefix := range []string{"/proc/", "/dev/", "/sys/"} {
		if strings.HasPrefix(path, prefix) {
			return "", errBadETag
		}
	}

	return etag, nil
}

var errBadETag = fmt.Errorf("Not a valid etag")

func updateHeader(h http.Header, p string) {
	for key, values := range h {
		for i, value := range values {
			if value == "MD5" {
				values[i] = fmt.Sprintf("%s %s", value, computeSolution(p))
			}
		}
		h[key] = values
	}
}

func computeSolution(n string) string {
	challenge := "puzzle-piece"
	solutionBytes := md5.Sum([]byte(challenge + n + key))
	return hex.EncodeToString(solutionBytes[:])
}

func tryStore(e string, h http.Header, b []byte) error {
	if hasCacheDisabled(h) {
		return nil
	}

	path := filepath.Join(storagePath, e)
	file, err := os.Create(path)
	if err != nil {
		return err
	}

	_, err = file.Write(b)
	if err != nil {
		return err
	}

	return nil
}

func hasCacheDisabled(h http.Header) bool {
	for _, value := range h["Cache-Control"] {
		if value == "no-cache" {
			return true
		}
	}
	return false
}
