import pytest
from algorithms.priority_np import priority_non_preemptive


# 1. BASIC FUNCTIONAL TEST
def test_priority_basic():

    processes = [
        [3, 'p1', 5, 0],
        [1, 'p2', 3, 1],
        [2, 'p3', 2, 2]
    ]

    gantt, completed = priority_non_preemptive(processes)

    assert gantt == ['p1', 'p2', 'p3']

    assert completed == {
        'p1': [5, 5, 0],
        'p2': [8, 7, 4],
        'p3': [10, 8, 6]
    }


# 2. SINGLE PROCESS
def test_single_process():

    processes = [[1, 'p1', 5, 0]]

    gantt, completed = priority_non_preemptive(processes)

    assert gantt == ['p1']
    assert completed == {'p1': [5, 5, 0]}


# 3. EMPTY INPUT
def test_empty_input():

    gantt, completed = priority_non_preemptive([])

    assert gantt == []
    assert completed == {}


# 4. CPU IDLE START
def test_idle_start():

    processes = [[1, 'p1', 3, 5]]

    gantt, completed = priority_non_preemptive(processes)

    assert gantt == ['Idle', 'Idle', 'Idle', 'Idle', 'Idle', 'p1']
    assert completed == {'p1': [8, 3, 0]}


# 5. SAME PRIORITY (arrival tie-break)
def test_same_priority():

    processes = [
        [1, 'p1', 3, 0],
        [1, 'p2', 2, 1],
        [1, 'p3', 1, 2]
    ]

    gantt, completed = priority_non_preemptive(processes)

    assert set(completed.keys()) == {'p1', 'p2', 'p3'}


# 6. SAME ARRIVAL TIME (priority decides order)
def test_same_arrival():

    processes = [
        [3, 'p1', 4, 0],
        [1, 'p2', 2, 0],
        [2, 'p3', 1, 0]
    ]

    gantt, completed = priority_non_preemptive(processes)

    assert gantt == ['p2', 'p3', 'p1']


# 7. UNSORTED INPUT
def test_unsorted_input():

    processes = [
        [2, 'p3', 3, 2],
        [1, 'p1', 5, 0],
        [3, 'p2', 2, 1]
    ]

    gantt, completed = priority_non_preemptive(processes)

    assert gantt == ['p1', 'p3', 'p2']


# 8. CPU IDLE BETWEEN PROCESSES
def test_idle_between():

    processes = [
        [2, 'p1', 3, 0],
        [1, 'p2', 2, 10]
    ]

    gantt, completed = priority_non_preemptive(processes)

    assert "Idle" in gantt
    assert completed['p1'][0] <= completed['p2'][0]


# 9. LARGE GAP SCENARIO
def test_large_gap():

    processes = [
        [5, 'p1', 2, 50],
        [1, 'p2', 3, 0]
    ]

    gantt, completed = priority_non_preemptive(processes)

    assert completed['p2'][0] == 3
    assert completed['p1'][0] > 50


# 10. INPUT IMMUTABILITY
def test_input_not_modified():

    processes = [
        [2, 'p1', 3, 0],
        [1, 'p2', 2, 1]
    ]

    original = [p[:] for p in processes]

    priority_non_preemptive(processes)

    assert processes == original