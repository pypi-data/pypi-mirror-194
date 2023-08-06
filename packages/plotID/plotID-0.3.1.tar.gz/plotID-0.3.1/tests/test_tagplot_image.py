#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unittests for tagplot_image
"""

import os
import unittest
import matplotlib.pyplot as plt
from PIL import PngImagePlugin, JpegImagePlugin
from plotid.tagplot_image import tagplot_image
from plotid.plotoptions import PlotOptions


FIG1 = plt.figure()
IMG1 = "image1.png"
FIG2 = plt.figure()
IMG2 = "image2.jpg"

# Constants for tests
PROJECT_ID = "MR01"
METHOD = "time"
ROTATION = 90
POSITION = (0.975, 0.35)


class TestTagplotImage(unittest.TestCase):
    """
    Class for all unittests of the tagplot_image module.
    """

    def setUp(self) -> None:
        plt.savefig(IMG1)
        plt.savefig(IMG2)

    def test_images(self) -> None:
        """
        Test of returned objects. Check if they are png and jpg files,
        respectively.
        """
        options = PlotOptions(
            [IMG1, IMG2],
            ROTATION,
            POSITION,
            figure_ids=["test123456", "654321tset"],
            prefix=PROJECT_ID,
            id_method=METHOD,
            qrcode=True,
            fontsize=10,
            font="plotid/resources/OpenSans/OpenSans-Bold.ttf",
            fontcolor=(0, 1, 0),
        )
        options.validate_input()
        figs_and_ids = tagplot_image(options)
        self.assertIsInstance(figs_and_ids.figs[0], PngImagePlugin.PngImageFile)
        self.assertIsInstance(figs_and_ids.figs[1], JpegImagePlugin.JpegImageFile)

    def test_single_image(self) -> None:
        """
        Test of returned objects. Check if png files are returned,
        if a single matplot figure is given (not as a list).
        """
        options = PlotOptions(IMG1, ROTATION, POSITION)
        options.validate_input()
        figs_and_ids = tagplot_image(options)
        self.assertIsInstance(figs_and_ids.figs[0], PngImagePlugin.PngImageFile)

    def test_image_not_str(self) -> None:
        """Test if Error is raised if wrong type of image is given."""
        options = PlotOptions(
            3, ROTATION, POSITION, prefix=PROJECT_ID, id_method=METHOD
        )
        options.validate_input()
        with self.assertRaises(TypeError):
            tagplot_image(options)

    def test_image_not_file(self) -> None:
        """Test if Error is raised if the image file does not exist."""
        options = PlotOptions("xyz", ROTATION, POSITION)
        options.validate_input()
        with self.assertRaises(FileNotFoundError):
            tagplot_image(options)

    def test_image_plotoptions(self) -> None:
        """
        Test if Error is raised if not an instance of PlotOptions is passed.
        """
        with self.assertRaises(TypeError):
            tagplot_image("wrong_object")

    def test_font_file_not_defined(self) -> None:
        """Test if a Warning is raised if an invalid font file was specified."""
        options = PlotOptions(IMG1, ROTATION, POSITION, font="font")
        options.validate_input()
        with self.assertWarns(Warning):
            tagplot_image(options)

    def tearDown(self) -> None:
        os.remove(IMG1)
        os.remove(IMG2)


if __name__ == "__main__":
    unittest.main()
