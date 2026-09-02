# Manual CLI

## Run command
```bash 
PYTHONPATH=services/pipeline/src python -m pipeline.cli --start "2026-08-20 00:00" --end "2026-08-23 00:00"
```

## CLI check
The CLI was tested with a valid date range.

Result:

- Status: success
- Records processed: 365

If an error occurs, the CLI shows the error message.