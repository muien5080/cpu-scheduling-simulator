import pytest
from algorithms.sjf_non_preemptive import sjf

# 1. BASIC FUNCTIONAL TEST
def test_sjf_basic():
    processes = [
        [2, 6, 'P1'],
        [5, 2, 'P2'],
        [1, 8, 'P3'],
        [0, 3, 'P4'],
        [4, 4, 'P5']
    ]

    gantt, completed = sjf(processes)

    assert gantt == ['P4', 'P1', 'P2', 'P5', 'P3']
    assert completed == {
        'P4': [3, 3, 0],
        'P1': [9, 7, 1],
        'P2': [11, 6, 4],
        'P5': [15, 11, 7],
        'P3': [23, 22, 14]
    }


# 2. SINGLE PROCESS
def test_single_process():
    processes = [[0, 5, 'P1']]

    gantt, completed = sjf(processes)

    assert gantt == ['P1']
    assert completed == {'P1': [5, 5, 0]}


# 3. EMPTY INPUT
def test_empty_input():
    processes = []

    gantt, completed = sjf(processes)

    assert gantt == []
    assert completed == {}


# 4. CPU IDLE AT START
def test_idle_start():
    processes = [[3, 4, 'P1']]

    gantt, completed = sjf(processes)

    assert gantt == ['Idle', 'Idle', 'Idle', 'P1']
    assert completed == {'P1': [7, 4, 0]}


# 5. UNSORTED INPUT
def test_unsorted_input():
    processes = [
        [5, 2, 'P2'],
        [0, 3, 'P1'],
        [1, 6, 'P3']
    ]

    gantt, completed = sjf(processes)

    # Correct for non-preemptive SJF
    assert gantt == ['P1', 'P3', 'P2']
    assert completed == {
        'P1': [3, 3, 0],
        'P3': [9, 8, 2],
        'P2': [11, 6, 4]
    }


# 6. SAME ARRIVAL TIMES
def test_same_arrival():
    processes = [
        [0, 4, 'P1'],
        [0, 3, 'P2'],
        [0, 2, 'P3']
    ]

    gantt, completed = sjf(processes)

    assert gantt == ['P3', 'P2', 'P1']
    assert completed['P1'] == [9, 9, 5]
    assert completed['P2'] == [5, 5, 2]
    assert completed['P3'] == [2, 2, 0]


# 7. ZERO BURST TIME
def test_zero_burst():
    processes = [
        [0, 0, 'P1'],
        [1, 5, 'P2']
    ]

    gantt, completed = sjf(processes)

    assert 'P1' in completed
    assert completed['P1'] == [0, 0, 0]


# 8. MULTIPLE IDLE GAPS
def test_multiple_idle_gaps():
    processes = [
        [2, 2, 'P1'],
        [10, 3, 'P2']
    ]

    gantt, completed = sjf(processes)

    # Idle before P1 and between P1 and P2
    assert gantt.count("Idle") > 0
    assert completed['P1'][0] == 4
    assert completed['P2'][0] == 13


# 9. LARGE GAP SCENARIO
def test_large_gap():
    processes = [
        [100, 5, 'P1'],
        [200, 3, 'P2']
    ]

    gantt, completed = sjf(processes)

    assert gantt[0] == "Idle"
    assert completed['P1'][0] == 105
    assert completed['P2'][0] == 203


# 10. IMMUTABILITY CHECK
def test_input_not_modified():
    processes = [
        [0, 5, 'P1'],
        [1, 3, 'P2']
    ]

    original = [p[:] for p in processes]

    sjf(processes)

    assert processes == original