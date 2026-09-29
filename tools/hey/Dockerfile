# Fallback load generator when hey.exe isn't installed on Windows.
#   docker build -t civicpulse-hey tools/hey
FROM golang:alpine AS build
RUN go install github.com/rakyll/hey@latest

FROM alpine:3.20
COPY --from=build /go/bin/hey /usr/local/bin/hey
ENTRYPOINT ["hey"]
