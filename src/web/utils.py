def get_maintenance_time():
    with open('/flags/maintenance.on', 'r') as f:
        retry_after = f.readline()
    return retry_after