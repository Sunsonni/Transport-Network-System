# MVP:
# Use queue for deliver scheduling
# Log completed routes int a search able structure
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


# Class functions:

# RUN COMMAND:
# python3 graph_schedule1.py schedule3.txt
from schedule import TransportSchedule
from datetime import datetime

import sys

try:
    filename = sys.argv[1]

    scheduler = TransportSchedule()

    # print(scheduler.schedule_delivery("City25", "City0", "09:00"))
    # print(scheduler.schedule_delivery("City23", "City91", "09:15"))
    
    with open(filename, "r") as f:
        for line in f:
            clean_line = line.strip()
            if clean_line:
                splits = clean_line.split(" ")

                match splits:
                    case ["SCHEDULE", "DELIVERY", route, _, time]:
                        src, dst = route.split("->")
                        scheduler.schedule_delivery(src, dst, time)
                    case ["RECORD_HISTORY"]:
                        # TODO ADD RECORD HISTORY TO THIS
                        print("WILL ADD STUFF")
                    case ["UNDO_LAST"]:
                        print(scheduler.undo_last())
                    case ["QUERY_HISTORY", _, start_time, end_time]:
                        scheduler.query_history(start_time, end_time)

                        

                print(splits)
    print(f"queue: {scheduler.queue}")
    print(f"undo stack: {scheduler.undo_stack}")
    print(f"history: {scheduler.history}")
    print(f"queue history : {scheduler.query_history('10:00', '10:15')}")


except Exception as e:
    print(f"Error: {e}")