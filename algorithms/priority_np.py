"""
Priority CPU scheduling Non- Preemptive
"""

# Process : [Priority, pid, burst_time, arrival_time]
def priority_non_preemptive(process_list):

    gantt = []
    time = 0
    completed = {}

    if not process_list:
        return [], {}

    processes = process_list[:]  # avoid modifying original

    while processes:

        available = [p for p in processes if p[3] <= time]

        if not available:
            gantt.append('Idle')
            time += 1
            continue

        # sort by priority, then arrival time
        available.sort(key=lambda x: (x[0], x[3]))

        process = available[0]
        processes.remove(process)

        gantt.append(process[1])

        time += process[2]

        ct = time
        tat = ct - process[3]
        wt = tat - process[2]

        completed[process[1]] = [ct, tat, wt]

    return gantt, completed


if __name__ == "__main__":

    process_list = [
        [5,'p1',6,2],
        [4,'p2',2,5],
        [1,'p3',8,1],
        [2,'p4',3,0],
        [3,'p5',4,4]
    ]

    gantt, completed = priority_non_preemptive(process_list)

    print("Gantt Chart:", gantt)
    print("Completed:", completed)