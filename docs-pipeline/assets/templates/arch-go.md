# Architecture

> Generated from the Go fallback template because automated project exploration was skipped or unavailable.

## Project Type

Go project detected by `go.mod`.

## Entry Points

- Application entry points should be confirmed from `cmd/`, package `main`, and module layout.
- Common candidates include `cmd/<app>/main.go` or root `main.go`.

## Module Boundaries

Record each stable package here after reading the code:

| Package | Responsibility | Key Files |
|---------|----------------|-----------|
| _Unconfirmed_ | Confirm from source before relying on this architecture file. | |

## Build, Test, and Run

Confirm commands against the module before use:

```bash
go build ./...
go test ./...
go run .
```

## Update Rule

Replace this fallback with code-derived architecture notes before making non-trivial architecture changes.
