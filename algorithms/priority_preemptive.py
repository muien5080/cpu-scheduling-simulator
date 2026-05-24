"""
Priority preemptive
"""

# Process : [priority, pid, burst_time, arrival_time]

def priority_preemptive(process_list):

    if not process_list:
        return [], {}

    gantt = []
    completed = {}

    time = 0
    finished = 0
    n = len(process_list)

    remaining_bt = {p[1]: p[2] for p in process_list}
    arrival = {p[1]: p[3] for p in process_list}

    while finished < n:

        available = [
            p for p in process_list
            if p[3] <= time and remaining_bt[p[1]] > 0
        ]

        if not available:
            gantt.append('Idle')
            time += 1
            continue

        # pick highest priority (lowest number)
        available.sort(key=lambda x: (x[0], x[3]))

        process = available[0]
        pid = process[1]

        gantt.append(pid)

        remaining_bt[pid] -= 1
        time += 1

        if remaining_bt[pid] == 0:

            finished += 1

            ct = time
            tat = ct - arrival[pid]
            wt = tat - process[2]

            completed[pid] = [ct, tat, wt]

    return gantt, completed



if __name__ == "__main__":
    process_list= [
        [5,'p1',6,2], 
        [2,'p2',2,5], 
        [4,'p3',8,1], 
        [1,'p4',3,0], 
        [3,'p5',4,4]
    ]
    
    gantt , completed = priority_preemptive(process_list)
    
    print("Gantt Chart:")
    print(gantt)

    print("\nCompleted Processes:")
    for pid, stats in completed.items():
        print(pid, stats)