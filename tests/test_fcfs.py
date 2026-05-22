import pytest
from algorithms.fcfs import fcfs


# 1. BASIC FUNCTIONAL TEST
def test_fcfs_basic():
    processes = [
        [0, 10, 'p1'],
        [3, 5, 'p2'],
        [5, 2, 'p3']
    ]

    gantt, completed = fcfs(processes)

    assert gantt == ['p1', 'p2', 'p3']

    assert completed == {
        'p1': [10, 10, 0],
        'p2': [15, 12, 7],
        'p3': [17, 12, 10]
    }


# 2. SINGLE PROCESS
def test_single_process():
    processes = [[0, 5, 'p1']]

    gantt, completed = fcfs(processes)

    assert gantt == ['p1']
    assert completed == {'p1': [5, 5, 0]}


# 3. EMPTY INPUT
def test_empty_input():
    processes = []

    gantt, completed = fcfs(processes)

    assert gantt == []
    assert completed == {}


# 4. CPU IDLE AT START
def test_idle_start():
    processes = [[3, 4, 'p1']]

    gantt, completed = fcfs(processes)

    assert gantt == ['Idle', 'Idle', 'Idle', 'p1']
    assert completed == {'p1': [7, 4, 0]}


# 5. UNSORTED INPUT
def test_unsorted_input():
    processes = [
        [5, 2, 'p3'],
        [0, 10, 'p1'],
        [3, 5, 'p2']
    ]

    gantt, completed = fcfs(processes)

    assert gantt == ['p1', 'p2', 'p3']

    assert completed == {
        'p1': [10, 10, 0],
        'p2': [15, 12, 7],
        'p3': [17, 12, 10]
    }


# 6. SAME ARRIVAL TIMES
def test_same_arrival():
    processes = [
        [0, 4, 'p1'],
        [0, 3, 'p2'],
        [0, 2, 'p3']
    ]

    gantt, completed = fcfs(processes)

    assert gantt == ['p1', 'p2', 'p3']

    assert completed['p1'] == [4, 4, 0]
    assert completed['p2'] == [7, 7, 4]
    assert completed['p3'] == [9, 9, 7]


# 7. ZERO BURST TIME
def test_zero_burst():
    processes = [
        [0, 0, 'p1'],
        [1, 5, 'p2']
    ]

    gantt, completed = fcfs(processes)

    assert 'p1' in completed
    assert completed['p1'] == [0, 0, 0]



# 8. MULTIPLE IDLE GAPS
def test_multiple_idle_gaps():
    processes = [
        [2, 2, 'p1'],
        [10, 3, 'p2']
    ]

    gantt, completed = fcfs(processes)

    # must include idle before p1 and between p1 and p2
    assert gantt.count("Idle") > 0
    assert completed['p1'][0] == 4
    assert completed['p2'][0] == 13



# 9. LARGE GAP SCENARIO
def test_large_gap():
    processes = [
        [100, 5, 'p1'],
        [200, 3, 'p2']
    ]

    gantt, completed = fcfs(processes)

    assert gantt[0] == "Idle"
    assert completed['p1'][0] == 105
    assert completed['p2'][0] == 203


# 10. IMMUTABILITY CHECK
def test_input_not_modified():
    processes = [
        [0, 5, 'p1'],
        [1, 3, 'p2']
    ]

    original = [p[:] for p in processes]

    fcfs(processes)

    assert processes == original