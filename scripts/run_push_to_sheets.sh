#!/bin/bash
echo "==================================="
echo "Starting push_to_sheets..."
/app/.venv/bin/python -m src.push_to_sheets
echo "push_to_sheets finished."
echo "==================================="