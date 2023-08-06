# -*- coding: utf-8 -*-
"""
Runner for all tests regarding the plotid project.

Includes starting all tests and measuring the code coverage.
"""

import sys
import os
import unittest
import coverage

path = os.path.abspath("plotid")
sys.path.append(path)

cov = coverage.Coverage()
cov.start()

loader = unittest.TestLoader()
tests = loader.discover(".")
testRunner = unittest.runner.TextTestRunner(verbosity=2)
result = testRunner.run(tests)

cov.stop()
cov.save()

if result.wasSuccessful():
    covered = cov.report(show_missing=True, precision=2)
    assert covered > 95, "Not enough coverage."
    sys.exit(0)
else:
    sys.exit(1)
