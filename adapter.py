#!/usr/bin/env python3
import json
import os
import time
import urllib.request

# Ensure the directory exists
os.makedirs("/etc/prometheus/targets", exist_ok=True)

# File path
target_file = "/etc/prometheus/targets/targets.json"

while True:
    try:
        # Fetch data from inventory service
        with urllib.request.urlopen("http://inventory-service:1337/inventory") as response:
            sensors = json.loads(response.read().decode())
            
        print(f"Got {len(sensors)} sensors")
        
        # Create the Prometheus SD format - one entry for all sensors
        targets = []
        
        for sensor in sensors:
            target = {
                "targets": ["inventory-service:1337"],
                "labels": {
                    "job": "sensors",
                    "sensor_name": sensor
                }
            }
            targets.append(target)
        
        # Write to file
        with open(target_file, "w") as f:
            json.dump(targets, f)
            
        print(f"Written {len(targets)} targets to {target_file}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Sleep for 60 seconds
    time.sleep(60)
