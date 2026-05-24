import pytest
from algorithms.round_robin import round_robin


# 1. BASIC FUNCTIONAL TEST
def test_rr_basic():

    processes = [
        [0, 5, 'p1'],
        [1, 3, 'p2'],
        [2, 1, 'p3']
    ]

    gantt, completed = round_robin(processes, 2)

    assert gantt == [
        'p1', 'p2', 'p3', 'p1', 'p2', 'p1'
    ]

    assert completed == {
        'p3': [5, 3, 2],
        'p2': [8, 7, 4],
        'p1': [9, 9, 4]
    }


# 2. SINGLE PROCESS
def test_single_process():

    processes = [
        [0, 5, 'p1']
    ]

    gantt, completed = round_robin(processes, 2)

    assert gantt == ['p1', 'p1', 'p1']

    assert completed == {
        'p1': [5, 5, 0]
    }


# 3. EMPTY INPUT
def test_empty_input():

    gantt, completed = round_robin([], 2)

    assert gantt == []
    assert completed == {}


# 4. CPU IDLE AT START
def test_idle_at_start():

    processes = [
        [3, 4, 'p1']
    ]

    gantt, completed = round_robin(processes, 2)

    assert gantt == [
        'Idle', 'Idle', 'Idle',
        'p1', 'p1'
    ]

    assert completed == {
        'p1': [7, 4, 0]
    }


# 5. UNSORTED INPUT
def test_unsorted_input():

    processes = [
        [4, 2, 'p3'],
        [0, 5, 'p1'],
        [2, 3, 'p2']
    ]

    gantt, completed = round_robin(processes, 2)

    assert gantt == [
        'p1', 'p2', 'p1',
        'p3', 'p2', 'p1'
    ]

    assert completed['p3'] == [8, 4, 2]


# 6. SAME ARRIVAL TIMES
def test_same_arrival_time():

    processes = [
        [0, 4, 'p1'],
        [0, 3, 'p2'],
        [0, 2, 'p3']
    ]

    gantt, completed = round_robin(processes, 2)

    assert gantt == [
        'p1', 'p2', 'p3',
        'p1', 'p2'
    ]

    assert completed == {
        'p3': [6, 6, 4],
        'p1': [8, 8, 4],
        'p2': [9, 9, 6]
    }


# 7. LARGE TIME QUANTUM
def test_large_time_quantum():

    processes = [
        [0, 4, 'p1'],
        [1, 3, 'p2']
    ]

    gantt, completed = round_robin(processes, 10)

    # behaves similar to FCFS
    assert gantt == ['p1', 'p2']

    assert completed == {
        'p1': [4, 4, 0],
        'p2': [7, 6, 3]
    }


# 8. TIME QUANTUM = 1
def test_quantum_one():

    processes = [
        [0, 3, 'p1'],
        [0, 2, 'p2']
    ]

    gantt, completed = round_robin(processes, 1)

    assert gantt == [
        'p1', 'p2',
        'p1', 'p2',
        'p1'
    ]

    assert completed == {
        'p2': [4, 4, 2],
        'p1': [5, 5, 2]
    }


# 9. MULTIPLE IDLE GAPS
def test_multiple_idle_gaps():

    processes = [
        [2, 2, 'p1'],
        [10, 3, 'p2']
    ]

    gantt, completed = round_robin(processes, 2)

    assert gantt.count("Idle") > 0

    assert completed['p1'] == [4, 2, 0]
    assert completed['p2'] == [13, 3, 0]


# 10. PROCESS ARRIVES DURING EXECUTION
def test_process_arrival_during_execution():

    processes = [
        [0, 6, 'p1'],
        [1, 4, 'p2'],
        [2, 2, 'p3']
    ]

    gantt, completed = round_robin(processes, 2)

    assert gantt == [
        'p1', 'p2', 'p3',
        'p1', 'p2', 'p1'
    ]

    assert completed == {
        'p3': [6, 4, 2],
        'p2': [10, 9, 5],
        'p1': [12, 12, 6]
    }


# 11. INVALID TIME QUANTUM
def test_invalid_quantum():

    processes = [
        [0, 5, 'p1']
    ]

    with pytest.raises(ValueError):
        round_robin(processes, 0)


# 12. INPUT IMMUTABILITY
def test_input_not_modified():

    processes = [
        [0, 5, 'p1'],
        [1, 3, 'p2']
    ]

    original = [p[:] for p in processes]

    round_robin(processes, 2)

    assert processes == original