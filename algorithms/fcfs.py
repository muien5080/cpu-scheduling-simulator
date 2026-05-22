"""
FCFS (First Come First Serve) CPU Scheduling Algorithm
"""

from typing import List, Tuple, Dict

Process = Tuple[int, int, str]


def fcfs(process_list: List[Process]) -> Tuple[list, Dict[str, list]]:
    """
    FCFS Scheduling Algorithm

    Returns:
        gantt_chart: execution order
        completed: {pid: [CT, TAT, WT]}
    """

    if not process_list:
        return [], {}

    processes = sorted(process_list, key=lambda x: x[0])

    current_time = 0
    gantt_chart = []
    completed = {}

    while processes:

        arrival_time, burst_time, pid = processes[0]

        # idle handling
        if arrival_time > current_time:
            gantt_chart.append("Idle")
            current_time += 1
            continue

        processes.pop(0)
        gantt_chart.append(pid)

        current_time += burst_time

        ct = current_time
        tat = ct - arrival_time
        wt = tat - burst_time

        completed[pid] = [ct, tat, wt]

    return gantt_chart, completed


if __name__ == "__main__":

    processes = [
        [0, 10, "p1"],
        [3, 5, "p2"],
        [5, 2, "p3"],
        [6, 6, "p4"],
        [8, 6, "p5"]
    ]

    gantt, completed = fcfs(processes)

    print("Gantt Chart:")
    print(gantt)

    print("\nCompleted Processes:")
    for pid, stats in completed.items():
        print(pid, stats)