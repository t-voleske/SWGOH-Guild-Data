#!/bin/bash
echo "==================================="
echo "Starting roster_checks..."
/app/.venv/bin/python -m src.roster_checks
echo "roster_checks finished."
echo "==================================="
