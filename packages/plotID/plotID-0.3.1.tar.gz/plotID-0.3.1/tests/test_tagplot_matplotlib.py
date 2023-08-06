#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unittests for tagplot_matplotlib
"""

import unittest
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from plotid.tagplot_matplotlib import tagplot_matplotlib
from plotid.plotoptions import PlotOptions


FIG1 = plt.figure()
FIG2 = plt.figure()
FIGS_AS_LIST = [FIG1, FIG2]

# Constants for tests
PROJECT_ID = "MR01"
METHOD = "time"
ROTATION = 90
POSITION = (0.975, 0.35)


class TestTagplotMatplotlib(unittest.TestCase):
    """
    Class for all unittests of the tagplot_matplotlib module.
    """

    def test_mplfigures(self) -> None:
        """Test of returned objects. Check if they are matplotlib figures."""
        options = PlotOptions(
            FIGS_AS_LIST,
            ROTATION,
            POSITION,
            figure_ids=["test123456", "654321tset"],
            prefix=PROJECT_ID,
            id_method=METHOD,
            qrcode=True,
            fontsize=10,
            font="plotid/resources/OpenSans/OpenSans-Bold.ttf",
            fontcolor=(0, 0, 1),
        )
        options.validate_input()
        figs_and_ids = tagplot_matplotlib(options)
        self.assertIsInstance(figs_and_ids.figs[0], Figure)
        self.assertIsInstance(figs_and_ids.figs[1], Figure)

    def test_single_mplfigure(self) -> None:
        """
        Test of returned objects. Check if matplotlib figures are returned,
        if a single matplot figure is given (not as a list).
        """
        options = PlotOptions(FIG1, ROTATION, POSITION)
        options.validate_input()
        figs_and_ids = tagplot_matplotlib(options)
        self.assertIsInstance(figs_and_ids.figs[0], Figure)

    def test_mplerror(self) -> None:
        """Test if Error is raised if wrong type of figures is given."""
        options = PlotOptions(3, ROTATION, POSITION)
        options.validate_input()
        with self.assertRaises(TypeError):
            tagplot_matplotlib(options)

    def test_mpl_plotoptions(self) -> None:
        """
        Test if Error is raised if not an instance of PlotOptions is passed.
        """
        with self.assertRaises(TypeError):
            tagplot_matplotlib("wrong_object")


if __name__ == "__main__":
    unittest.main()
