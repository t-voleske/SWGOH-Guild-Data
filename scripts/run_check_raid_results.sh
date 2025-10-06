#!/bin/bash
echo "==================================="
echo "Starting check_raid_results..."
/app/.venv/bin/python -m src.check_raid_results
echo "check_raid_results finished."
echo "==================================="