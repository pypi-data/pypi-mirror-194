# Helpers for the ELM framework scripts

## Logging

Prefer dict based config.

## HTTP

The `http` module contains a Uvicorn server which can be run outside of the main thread.

## Json

The `json` module contains an implementation of `dumps` which handles Decimal (turns into string)

## Output

### never_ending_observer

Returns an `OnNext` only observer which logs an error to `logger` if it ever completes or errors.