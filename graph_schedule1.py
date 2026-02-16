# MVP:
# Use queue for deliver scheduling
# Log completed routes into a searchable structure
# Implement an undo stack to roll back actions
# Enable time range queries over history
# 
# SAMPLE INPUT:
# SCHEDULE DELIVERY City1->City4 at 9:00
# SCHEDULE DELIVERY City2->City3 at 9:15
# RECORD_HISTORY
# UNDO_LAST
# QUERY_HISTORY BETWEEN 9:00 9:30

# SAMPLE OUTPUT:
# Scheduled: City1->City4 at 9:00
# Scheduled: City2->City3 at 9:15
# Recorded history
# Undid last action
# History between 9:00 and 9:30:
# - City1->City4 at 9:00

# RUN COMMAND:
# python3 graph_schedule1.py schedule3.txt
from schedule import TransportSchedule

import sys

try:
    filename = sys.argv[1]

    scheduler = TransportSchedule()
    
    with open(filename, "r") as f:
        for line_number, line in enumerate(f, start = 1):
            clean_line = line.strip()
            if clean_line:
                splits = clean_line.split(" ")

                match splits:
                    case ["SCHEDULE", "DELIVERY", route, _, time]:
                        src, dst = route.split("->")
                        print(scheduler.schedule_delivery(src, dst, time))
                    case ["RECORD_HISTORY"]:
                        print(scheduler.record_history())
                    case ["UNDO_LAST"]:
                        print(scheduler.undo_last())
                    case ["QUERY_HISTORY", _, start_time, end_time]:
                        print(scheduler.query_history(start_time, end_time))
                    case _:
                        print(f"Unknown command {splits}. Skipping line {line_number}.")

except Exception as e:
    print(f"Error: {e}")