# golang:1.23.3-alpine3.20 (from 1.12.2024)
FROM golang@sha256:c694a4d291a13a9f9d94933395673494fc2cc9d4777b85df3a7e70b3492d3574 AS builder

COPY ./src /src
WORKDIR /src
RUN go build .

# alpine:3.20.3 (from 1.12.2024)
FROM alpine@sha256:1e42bbe2508154c9126d48c2b8a75420c3544343bf86fd041fb7527e017a4b4a

RUN adduser -D ctf
USER ctf:ctf

COPY --from=builder /src/puzzle-api /usr/local/bin
COPY ./puzzle /puzzle

ENTRYPOINT [ "puzzle-api" ]
