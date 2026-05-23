"""
SJF (Shortest Job First) Non-Preemptive CPU Scheduling Algorithm
"""

from typing import List, Tuple, Dict

Process = Tuple[int, int, str]  # (arrival_time, burst_time, pid)


def sjf(process_list: List[Process]):
    """
    SJF Non-Preemptive Scheduling Algorithm.

    Returns:
        gantt_chart: List of execution order including 'Idle' for CPU idle time
        completed: Dictionary mapping pid to [Completion Time, Turnaround Time, Waiting Time]
    """

    if not process_list:
        return [], {}

    # Copy input to avoid mutation
    processes = process_list.copy()
    time = 0
    gantt_chart = []
    completed = {}

    while processes:
        # Filter available processes at current time
        available = [p for p in processes if p[0] <= time]

        if not available:
            # CPU is idle
            gantt_chart.append("Idle")
            time += 1
            continue

        # Pick process with smallest burst time
        available.sort(key=lambda x: x[1])
        process = available[0]
        arrival_time, burst_time, pid = process

        # Execute process
        gantt_chart.append(pid)
        time += burst_time

        # Calculate metrics
        ct = time
        tat = ct - arrival_time
        wt = tat - burst_time

        completed[pid] = [ct, tat, wt]

        # Remove process from queue
        processes.remove(process)

    return gantt_chart, completed


if __name__ == "__main__":
    # Example processes: (arrival_time, burst_time, pid)
    process_list = [
        [2, 6, 'P1'],
        [5, 2, 'P2'],
        [1, 8, 'P3'],
        [0, 3, 'P4'],
        [4, 4, 'P5']
    ]

    gantt, completed = sjf(process_list)
    print("Gantt Chart:", gantt)
    print("Completed Processes:")
    for pid, stats in completed.items():
        print(pid , stats)