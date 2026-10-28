import csv
from datetime import datetime, timedelta
import random

# Generate smart_home_october.csv
start_time = datetime(2026, 10, 27, 0, 0)
rows = []

random.seed(42)

for i in range(144): # every 10 minutes for 24 hours
    curr_time = start_time + timedelta(minutes=10 * i)
    t_str = curr_time.strftime("%Y-%m-%d %H:%M:%S")
    hour = curr_time.hour
    
    # Check if inside the haunting window (03:00 to 03:30 AM)
    is_haunted = (hour == 3 and curr_time.minute <= 30)
    
    if is_haunted:
        temp = round(12.0 - random.uniform(0.5, 2.5), 1) # sudden deep cold spot
        sound = round(random.uniform(55.0, 78.0), 1)      # eerie frequency noise
        motion = 1                                         # phantom movement detected
        mag = round(random.uniform(140.0, 195.0), 1)      # extreme EMF spike
        power = round(random.uniform(15.0, 35.0), 1)      # brownout / battery drain
        notes = "PARANORMAL_DISRUPTION"
    elif hour >= 23 or hour < 7:
        temp = round(20.5 + random.uniform(-0.4, 0.4), 1)
        sound = round(28.0 + random.uniform(-2.0, 4.0), 1)
        motion = 1 if (hour == 1 and curr_time.minute == 20) else 0
        mag = round(44.0 + random.uniform(-1.5, 1.5), 1)
        power = round(135.0 + random.uniform(-10.0, 10.0), 1)
        notes = "Normal_Night"
    else:
        temp = round(22.0 + random.uniform(-0.8, 1.2), 1)
        sound = round(48.0 + random.uniform(-6.0, 12.0), 1)
        motion = random.choice([0, 1, 1, 0])
        mag = round(45.0 + random.uniform(-2.0, 2.0), 1)
        power = round(280.0 + random.uniform(-40.0, 60.0), 1)
        notes = "Normal_Day"
        
    rows.append({
        "timestamp": t_str,
        "temperature_c": temp,
        "sound_level_db": sound,
        "motion_detected": motion,
        "magnetic_field_ut": mag,
        "power_draw_w": power,
        "environmental_flag": notes
    })

with open("data/smart_home_october.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("Generated data/smart_home_october.csv with 144 rows")

# Generate server_rack_telemetry.csv
server_rows = []
for i in range(120): # every 12 minutes
    curr_time = start_time + timedelta(minutes=12 * i)
    t_str = curr_time.strftime("%Y-%m-%d %H:%M:%S")
    hour = curr_time.hour
    
    is_ghost = (hour == 3 and curr_time.minute <= 24)
    if is_ghost:
        cpu_temp = round(78.5 + random.uniform(4.0, 9.0), 1)
        fan_rpm = 0 # Fan mysteriously halted!
        ghost_proc_count = random.randint(13, 24)
        volts = round(10.2 - random.uniform(0.5, 1.2), 2)
        net_rx_kb = round(random.uniform(666.0, 999.0), 1)
        status = "GHOST_THREAD_SURGE"
    else:
        cpu_temp = round(45.0 + random.uniform(-2.0, 3.0), 1)
        fan_rpm = random.randint(2800, 3200)
        ghost_proc_count = 0
        volts = round(12.0 + random.uniform(-0.1, 0.1), 2)
        net_rx_kb = round(random.uniform(40.0, 120.0), 1)
        status = "Operational"
        
    server_rows.append({
        "timestamp": t_str,
        "cpu_temp_c": cpu_temp,
        "fan_rpm": fan_rpm,
        "ghost_threads": ghost_proc_count,
        "bus_voltage": volts,
        "net_rx_kb": net_rx_kb,
        "system_status": status
    })

with open("data/server_rack_telemetry.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=server_rows[0].keys())
    writer.writeheader()
    writer.writerows(server_rows)

print("Generated data/server_rack_telemetry.csv with 120 rows")
