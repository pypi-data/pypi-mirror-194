# -*- coding: utf-8 -*-

"""
Unittests for save_plot
"""

import os
import unittest
import matplotlib.pyplot as plt
from PIL import Image
from plotid.save_plot import save_plot

FIGURE = plt.figure()
PLOT_NAME = "PLOT_NAME"
IMG1 = "image1.png"
IMG2 = "image2.jpg"


class TestSavePlot(unittest.TestCase):
    """
    Class for all unittests of the save_plot module.
    """

    def setUp(self) -> None:
        plt.savefig(IMG1)
        plt.savefig(IMG2)

    def test_save_plot_matplotlib(self) -> None:
        """
        Test if save_plot succeeds with valid arguments
        using the matplotlib engine.
        """
        plot_paths = save_plot(FIGURE, [PLOT_NAME], extension="jpg")
        self.assertIsInstance(plot_paths, list)
        os.remove(PLOT_NAME + ".tmp.jpg")

    def test_save_plot_image_png(self) -> None:
        """
        Test if save_plot succeeds with valid arguments using the image engine
        and a png file.
        """
        img1 = Image.open(IMG1)
        plot_paths = save_plot(img1, [PLOT_NAME])
        self.assertIsInstance(plot_paths, list)
        os.remove(PLOT_NAME + ".tmp.png")

    def test_save_plot_image_jpg(self) -> None:
        """
        Test if save_plot succeeds with valid arguments using the image engine
        and a list of jpg files.
        """
        img2 = Image.open(IMG2)
        imgs_as_list = [img2, img2]
        plot_paths = save_plot(imgs_as_list, [PLOT_NAME], extension="jpg")
        self.assertIsInstance(plot_paths, list)
        os.remove(PLOT_NAME + "1.tmp.jpg")
        os.remove(PLOT_NAME + "2.tmp.jpg")

    def test_more_figs_than_names(self) -> None:
        """
        Test if a warning is raised if more figures than plot names are given.
        Additionally, check if files are named correctly.
        """
        with self.assertWarns(Warning):
            save_plot([FIGURE, FIGURE, FIGURE], [PLOT_NAME])
        for i in (1, 2, 3):
            assert os.path.isfile(PLOT_NAME + f"{i}.tmp.png")
            os.remove(PLOT_NAME + f"{i}.tmp.png")

    def test_more_names_than_figs(self) -> None:
        """Test if  Error is raised if more names than figures are given."""
        with self.assertRaises(IndexError):
            save_plot([FIGURE, FIGURE], [PLOT_NAME, PLOT_NAME, PLOT_NAME])

    def test_wrong_fig_type(self) -> None:
        """Test if Error is raised when not a figure object is given."""
        with self.assertRaises(TypeError):
            save_plot("figure", "PLOT_NAME", extension="jpg")

    def test_wrong_fig_in_list(self) -> None:
        """
        Test if Error is raised when one figure is invalid in a list of
        valid figures.
        """
        with self.assertRaises(TypeError):
            save_plot([FIGURE, "figure", FIGURE], "PLOT_NAME", extension="jpg")
        os.remove("PLOT_NAME1.tmp.jpg")

    def tearDown(self) -> None:
        os.remove(IMG1)
        os.remove(IMG2)


if __name__ == "__main__":
    unittest.main()
