#!/bin/bash
echo "Starting entrypoint script..."

# Setup log rotation
cat > /etc/logrotate.d/log << EOF
/var/log/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
EOF

# Export environment variables to cron's environment
printenv | grep -v "no_proxy" >> /etc/environment

# Load ALL crontab entries at once
echo "Loading crontab..."
cat << 'CRONTAB' | crontab -
*/2 * * * * /scripts/run_push_to_sheets.sh >> /var/log/push_to_sheets.log 2>&1
0 7 */3 * * /scripts/run_log_raid_score.sh >> /var/log/run_log_raid_score.log 2>&1
29 * * * * /scripts/run_log_tickets.sh >> /var/log/run_log_tickets.log 2>&1
*/3 * * * * /scripts/run_manage_members.sh >> /var/log/run_manage_members.log 2>&1
0 4 * * * /scripts/run_check_raid_results.sh >> /var/log/run_check_raid_results.log 2>&1
0 5 * * * /scripts/run_roster_checks.sh >> /var/log/run_roster_checks.log 2>&1
0 6 * * */2 /scripts/run_log_gp.sh >> /var/log/run_log_gp.log 2>&1
CRONTAB

# Verify it was loaded
echo "Installed crontab:"
crontab -l

echo "Starting cron daemon..."
cron

echo "Current time: $(date)"
echo "Waiting for cron jobs..."

# Follow logs
tail -f /var/log/*.log 2>/dev/null || tail -f /var/log/push_to_sheets.log