#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unittests for tagplot.
"""

import os
import unittest
import matplotlib.pyplot as plt
from plotid.tagplot import tagplot

# Constants for tests
FIG1 = plt.figure()
FIG2 = plt.figure()
FIGS_AS_LIST = [FIG1, FIG2]
IMG1 = "image1.png"
IMG2 = "image2.jpg"
IMGS_AS_LIST = [IMG1, IMG2]

PROJECT_ID = "MR01"
PLOT_ENGINE = "matplotlib"
METHOD = "time"


class TestTagplot(unittest.TestCase):
    """
    Class for all unittests of the tagplot module.
    """

    def setUp(self) -> None:
        plt.savefig(IMG1)
        plt.savefig(IMG2)

    def test_tagplot(self) -> None:
        """
        Test if tagplot runs successful.
        """
        tagplot(FIGS_AS_LIST, PLOT_ENGINE, prefix=PROJECT_ID, id_method=METHOD)
        tagplot(FIGS_AS_LIST, PLOT_ENGINE, rotation=42, position=(0.3, 0.14))
        tagplot(IMGS_AS_LIST, "image", location="north")

    def test_rotation(self) -> None:
        """Test if Error is raised if rotation is not a number."""
        with self.assertRaises(TypeError):
            tagplot(FIGS_AS_LIST, PLOT_ENGINE, rotation="42")

    def test_position(self) -> None:
        """Test if Error is raised if position is not a tuple containing two numbers."""
        with self.assertRaises(ValueError):
            tagplot(FIGS_AS_LIST, PLOT_ENGINE, position=(0.3, 0.14, 5))
        with self.assertRaises(TypeError):
            tagplot(FIGS_AS_LIST, PLOT_ENGINE, position=0.3)
        with self.assertRaises(TypeError):
            tagplot(FIGS_AS_LIST, PLOT_ENGINE, position=(0.3, True))

    def test_prefix(self) -> None:
        """Test if Error is raised if prefix is not a string."""
        with self.assertRaises(TypeError):
            tagplot(
                FIGS_AS_LIST,
                PLOT_ENGINE,
                location="southeast",
                prefix=3,
                id_method=METHOD,
            )

    def test_plotengine(self) -> None:
        """
        Test if Errors are raised if the provided plot engine is not supported.
        """
        with self.assertRaises(ValueError):
            tagplot(FIGS_AS_LIST, 1, location="north")
        with self.assertRaises(ValueError):
            tagplot(FIGS_AS_LIST, "xyz", location="south")

    def test_idmethod(self) -> None:
        """
        Test if Errors are raised if the id_method is not an string.
        """
        with self.assertRaises(TypeError):
            tagplot(FIGS_AS_LIST, PLOT_ENGINE, id_method=(0, 1), location="west")
        with self.assertRaises(TypeError):
            tagplot(FIGS_AS_LIST, PLOT_ENGINE, id_method=1)
        with self.assertRaises(TypeError):
            tagplot(FIGS_AS_LIST, PLOT_ENGINE, id_method=[0, 1])

    def test_location(self) -> None:
        """
        Test if Errors are raised if the provided location is not supported.
        """
        with self.assertRaises(TypeError):
            tagplot(FIGS_AS_LIST, PLOT_ENGINE, location=1)
        with self.assertWarns(Warning):
            tagplot(FIGS_AS_LIST, PLOT_ENGINE, location="up")

    def tearDown(self) -> None:
        os.remove(IMG1)
        os.remove(IMG2)


if __name__ == "__main__":
    unittest.main()
