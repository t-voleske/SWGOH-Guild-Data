#!/bin/bash
echo "==================================="
echo "Starting push_to_sheets..."
/usr/local/bin/python -m src.push_to_sheets
echo "push_to_sheets finished."
echo "==================================="