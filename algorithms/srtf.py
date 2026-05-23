"""
SRTF (Shortest Remaining Time First) CPU Scheduling Algorithm
"""

from typing import List, Tuple, Dict

Process = Tuple[int, int, str]  # (arrival_time, burst_time, pid)


def srtf(process_list: List[Process]) -> Tuple[list, Dict[str, list]]:
    """
    SRTF Scheduling Algorithm

    Returns:
        gantt_chart: execution order including 'Idle'
        completed: {pid: [CT, TAT, WT]}
    """

    if not process_list:
        return [], {}

    # Copy processes with remaining burst time: [arrival, burst, pid, remaining]
    processes = [[p[0], p[1], p[2], p[1]] for p in process_list]

    current_time = 0
    gantt_chart = []
    completed = {}

    while processes:
        # Processes that have arrived
        available = [p for p in processes if p[0] <= current_time]

        if not available:
            gantt_chart.append("Idle")
            current_time += 1
            continue

        # Pick process with shortest remaining time
        available.sort(key=lambda x: x[3])
        proc = available[0]
        arrival, burst, pid, remaining = proc

        if remaining > 0:
            gantt_chart.append(pid)
            proc[3] -= 1
            current_time += 1
            if proc[3] == 0:
                ct = current_time
                tat = ct - arrival
                wt = tat - burst
                completed[pid] = [ct, tat, wt]
                processes.remove(proc)
        else:
            # Zero burst process
            ct = current_time
            tat = ct - arrival
            wt = tat - burst
            completed[pid] = [ct, tat, wt]
            processes.remove(proc)

    return gantt_chart, completed


if __name__ == "__main__":
    processes = [
        [2, 6, "p1"],
        [5, 2, "p2"],
        [1, 8, "p3"],
        [0, 3, "p4"],
        [4, 4, "p5"]
    ]

    gantt, completed = srtf(processes)

    print("Gantt Chart:")
    print(gantt)

    print("\nCompleted Processes:")
    for pid, stats in completed.items():
        print(pid, stats)