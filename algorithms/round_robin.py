"""
Round Robin CPU Scheduling Algorithm
"""

from collections import deque
from typing import List, Tuple, Dict

Process = Tuple[int, int, str]


def round_robin(process_list: List[Process],time_quantum: int) -> Tuple[list, Dict[str, list]]:
    """
    Returns:
        gantt_chart: execution order
        completed: {pid: [CT, TAT, WT]}
    """

    if not process_list:
        return [], {}

    if time_quantum <= 0:
        raise ValueError("Time Quantum must be greater than 0")

    processes = sorted(process_list, key=lambda x: x[0])

    ready_queue = deque()

    gantt_chart = []
    completed = {}

    remaining_bt = {
        pid: burst
        for arrival, burst, pid in processes
    }

    original_bt = {
        pid: burst
        for arrival, burst, pid in processes
    }

    current_time = 0
    i = 0
    n = len(processes)

    while ready_queue or i < n:

        # add arrived processes to ready queue
        while i < n and processes[i][0] <= current_time:
            ready_queue.append(processes[i])
            i += 1

        # idle handling
        if not ready_queue:
            gantt_chart.append("Idle")
            current_time += 1
            continue

        arrival_time, burst_time, pid = ready_queue.popleft()

        execute_time = min(
            time_quantum,
            remaining_bt[pid]
        )

        gantt_chart.append(pid)

        current_time += execute_time
        remaining_bt[pid] -= execute_time

        # check newly arrived processes
        while i < n and processes[i][0] <= current_time:
            ready_queue.append(processes[i])
            i += 1

        # process completed
        if remaining_bt[pid] == 0:

            ct = current_time
            tat = ct - arrival_time
            wt = tat - original_bt[pid]

            completed[pid] = [ct, tat, wt]

        # process still has remaining burst time
        else:
            ready_queue.append(
                [arrival_time, burst_time, pid]
            )

    return gantt_chart, completed


if __name__ == "__main__":

    processes = [
        [2, 6, "p1"],
        [5, 2, "p2"],
        [1, 8, "p3"],
        [0, 3, "p4"],
        [4, 4, "p5"]
    ]

    time_quantum = 2

    gantt, completed = round_robin(
        processes,
        time_quantum
    )

    print("Gantt Chart:")
    print(gantt)

    print("\nCompleted Processes:")
    for pid, stats in completed.items():
        print(pid, stats)