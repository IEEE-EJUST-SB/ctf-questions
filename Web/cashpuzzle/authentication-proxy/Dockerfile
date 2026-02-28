# golang:1.23.3-alpine3.20 (from 1.12.2024)
FROM golang@sha256:c694a4d291a13a9f9d94933395673494fc2cc9d4777b85df3a7e70b3492d3574 AS builder

COPY ./src /src
WORKDIR /src
RUN go build .

# httpd:2.4.62-alpine3.20 (from 1.12.2024)
FROM httpd@sha256:b64b5734fbc0fbb8fb995d5cc29a2ff2d86ed4c83dfd4f4d82d183f2a66daed4

RUN apk add --no-cache parallel

RUN adduser -D ctf && \
    mkdir /usr/local/apache2/cache /storage && \
    chown ctf:ctf /usr/local/apache2/cache /usr/local/apache2/logs /storage

USER ctf:ctf

COPY --from=builder /src/authentication-proxy /usr/local/bin/

COPY --chown=ctf:ctf ./htdocs /usr/local/apache2/htdocs
COPY --chown=ctf:ctf ./httpd.conf /usr/local/apache2/conf/httpd.conf


ENTRYPOINT [ "parallel", "--tagstring", "{}", "--line-buffer", ":::" ]
CMD [ "httpd-foreground", "authentication-proxy" ]
