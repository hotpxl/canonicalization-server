# Canonicalization Server

API providing canonicalization service.

## Build

```bash
docker build -t canonicalization-server .
```

## Run

```bash
docker run -d -p 8080:80 --log-opt max-file=8 --log-opt max-size=8m --name canonicalization-server canonicalization-server
```

This will open an HTTP server on port 8080. Try the following for a demonstration.

```bash
curl -H "Content-Type: application/json" -X POST -d '{"text": "hound", "type": "object"}' localhost:8080/canonicalize
```
