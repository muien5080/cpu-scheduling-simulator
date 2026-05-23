import pytest
from algorithms.srtf import srtf

# 1. BASIC FUNCTIONAL TEST
def test_srtf_basic():
    processes = [
        [2, 6, 'p1'],
        [5, 2, 'p2'],
        [1, 8, 'p3'],
        [0, 3, 'p4'],
        [4, 4, 'p5']
    ]

    gantt, completed = srtf(processes)

    expected_completed = {
        'p4': [3, 3, 0],
        'p1': [15, 13, 7],
        'p2': [7, 2, 0],
        'p5': [10, 6, 2],
        'p3': [23, 22, 14]
    }

    assert completed == expected_completed


# 2. SINGLE PROCESS
def test_single_process():
    processes = [[0, 5, 'P1']]
    gantt, completed = srtf(processes)

    expected_completed = {
        'P1': [5, 5, 0]  
    }

    assert completed == expected_completed


# 3. EMPTY INPUT
def test_empty_input():
    processes = []
    gantt, completed = srtf(processes)
    assert gantt == []
    assert completed == {}


# 4. CPU IDLE AT START
def test_idle_start():
    processes = [[3, 4, 'P1']]
    gantt, completed = srtf(processes)
    assert gantt[:3] == ['Idle', 'Idle', 'Idle']
    assert completed['P1'] == [7, 4, 0]


# 5. SAME ARRIVAL
def test_same_arrival():
    processes = [
        [0, 4, 'P1'],
        [0, 3, 'P2'],
        [0, 2, 'P3']
    ]
    gantt, completed = srtf(processes)
    expected = {'P3': [2,2,0], 'P2': [5,5,2], 'P1': [9,9,5]}
    assert completed == expected


# 6. ZERO BURST TIME
def test_zero_burst():
    processes = [
        [0, 0, 'P1'],
        [1, 5, 'P2']
    ]
    gantt, completed = srtf(processes)
    assert completed['P1'] == [0,0,0]


# 7. MULTIPLE IDLE GAPS
def test_multiple_idle_gaps():
    processes = [
        [2, 2, 'P1'],
        [10, 3, 'P2']
    ]
    gantt, completed = srtf(processes)
    assert completed['P1'][0] == 4
    assert completed['P2'][0] == 13
    assert gantt.count("Idle") > 0


# 8. LATE ARRIVAL
def test_late_arrival():
    processes = [
        [10, 2, 'P1']
    ]
    gantt, completed = srtf(processes)
    assert gantt[:10] == ['Idle']*10
    assert completed['P1'] == [12, 2, 0]


# 9. MIXED ARRIVAL AND BURST
def test_mixed_arrival_burst():
    processes = [
        [0, 7, 'p1'],
        [2, 4, 'p2'],
        [4, 1, 'p3'],
        [5, 4, 'p4']
    ]

    gantt, completed = srtf(processes)

    expected_completed = {
        'p1': [16, 16, 9],
        'p2': [7, 5, 1],
        'p3': [5, 1, 0],
        'p4': [11, 6, 2]
    }

    assert completed == expected_completed


# 10. IMMUTABILITY CHECK
def test_input_not_modified():
    processes = [
        [0, 5, 'P1'],
        [1, 3, 'P2']
    ]
    original = [p[:] for p in processes]
    srtf(processes)
    assert processes == original