#!/bin/bash
echo "==================================="
echo "Starting check_raid_results..."
/usr/local/bin/python -m src.check_raid_results
echo "check_raid_results finished."
echo "==================================="