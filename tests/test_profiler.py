"""
Information
---------------------------------------------------------------------
Name        : test_profiler.py
Location    : ~/tests
Author      : Tom Eleff
Published   : 2024-03-19
Revised on  : .

Description
---------------------------------------------------------------------
Tests methods within `pytilities.profiler`.
"""

import time
from pytensils import profiler


# Profiler function(s)
@profiler.run_time
def test_run_time_success():
    time.sleep(1)
