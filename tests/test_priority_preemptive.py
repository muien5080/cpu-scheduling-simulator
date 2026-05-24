import pytest
from algorithms.priority_preemptive import priority_preemptive


# 1. BASIC FUNCTIONAL TEST
def test_priority_preemptive_basic():

    processes = [
        [5, 'p1', 6, 2],
        [2, 'p2', 2, 5],
        [4, 'p3', 8, 1],
        [1, 'p4', 3, 0],
        [3, 'p5', 4, 4]
    ]

    gantt, completed = priority_preemptive(processes)

    assert gantt == [
        'p4', 'p4', 'p4',
        'p3',
        'p5',
        'p2', 'p2',
        'p5', 'p5', 'p5',
        'p3', 'p3', 'p3', 'p3', 'p3', 'p3', 'p3',
        'p1', 'p1', 'p1', 'p1', 'p1', 'p1'
    ]

    assert completed['p4'] == [3, 3, 0]
    assert completed['p2'] == [7, 2, 0]
    assert completed['p5'] == [10, 6, 2]
    assert completed['p3'] == [17, 16, 8]
    assert completed['p1'] == [23, 21, 15]


# 2. SINGLE PROCESS
def test_single_process():

    processes = [
        [1, 'p1', 5, 0]
    ]

    gantt, completed = priority_preemptive(processes)

    assert gantt == ['p1', 'p1', 'p1', 'p1', 'p1']

    assert completed == {
        'p1': [5, 5, 0]
    }


# 3. EMPTY INPUT
def test_empty_input():

    gantt, completed = priority_preemptive([])

    assert gantt == []
    assert completed == {}


# 4. CPU IDLE AT START
def test_idle_start():

    processes = [
        [1, 'p1', 4, 3]
    ]

    gantt, completed = priority_preemptive(processes)

    assert gantt[:3] == ['Idle', 'Idle', 'Idle']

    assert completed['p1'] == [7, 4, 0]


# 5. PREEMPTION TEST
def test_preemption_occurs():

    processes = [
        [5, 'p1', 10, 0],
        [1, 'p2', 3, 2]
    ]

    gantt, completed = priority_preemptive(processes)

    expected = [
        'p1', 'p1',
        'p2', 'p2', 'p2',
        'p1', 'p1', 'p1', 'p1',
        'p1', 'p1', 'p1', 'p1'
    ]

    assert gantt == expected

    assert completed['p2'] == [5, 3, 0]
    assert completed['p1'] == [13, 13, 3]


# 6. SAME PRIORITY TEST
def test_same_priority():

    processes = [
        [1, 'p1', 3, 0],
        [1, 'p2', 2, 1]
    ]

    gantt, completed = priority_preemptive(processes)

    # earlier arrival should continue
    assert gantt == ['p1', 'p1', 'p1', 'p2', 'p2']

    assert completed['p1'] == [3, 3, 0]
    assert completed['p2'] == [5, 4, 2]


# 7. ALL SAME ARRIVAL
def test_same_arrival():

    processes = [
        [3, 'p1', 4, 0],
        [1, 'p2', 2, 0],
        [2, 'p3', 3, 0]
    ]

    gantt, completed = priority_preemptive(processes)

    assert gantt == [
        'p2', 'p2',
        'p3', 'p3', 'p3',
        'p1', 'p1', 'p1', 'p1'
    ]

    assert completed['p2'] == [2, 2, 0]
    assert completed['p3'] == [5, 5, 2]
    assert completed['p1'] == [9, 9, 5]


# 8. MULTIPLE IDLE GAPS
def test_multiple_idle_gaps():

    processes = [
        [1, 'p1', 2, 3],
        [2, 'p2', 3, 10]
    ]

    gantt, completed = priority_preemptive(processes)

    assert gantt.count('Idle') > 0

    assert completed['p1'][0] == 5
    assert completed['p2'][0] == 13


# 9. LARGE GAP SCENARIO
def test_large_gap():

    processes = [
        [1, 'p1', 2, 100],
        [2, 'p2', 3, 200]
    ]

    gantt, completed = priority_preemptive(processes)

    assert gantt[0] == 'Idle'

    assert completed['p1'][0] == 102
    assert completed['p2'][0] == 203


# 10. INPUT IMMUTABILITY
def test_input_not_modified():

    processes = [
        [1, 'p1', 5, 0],
        [2, 'p2', 3, 1]
    ]

    original = [p[:] for p in processes]

    priority_preemptive(processes)

    assert processes == original


# 11. ZERO BURST TIME
def test_zero_burst_time():

    processes = [
        [1, 'p1', 0, 0],
        [2, 'p2', 3, 1]
    ]

    # current implementation will fail this
    # useful bug-detection test

    gantt, completed = priority_preemptive(processes)

    assert completed['p1'] == [0, 0, 0]


# 12. ALL PROCESSES IDLE UNTIL LATE
def test_all_late_arrivals():

    processes = [
        [1, 'p1', 2, 50],
        [2, 'p2', 2, 60]
    ]

    gantt, completed = priority_preemptive(processes)

    assert gantt[:50] == ['Idle'] * 50

    assert completed['p1'] == [52, 2, 0]
    assert completed['p2'] == [62, 2, 0]