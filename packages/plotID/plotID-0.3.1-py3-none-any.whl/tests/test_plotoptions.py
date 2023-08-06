#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unittests for plotoptions.
"""

import unittest
from plotid.plotoptions import PlotOptions, PlotIDTransfer

ROTATION = 270
POSITION = (100, 200)


class TestTagplot(unittest.TestCase):
    """
    Class for all unittests of the plotoptions module.
    """

    def test_validate_input(self) -> None:
        """
        Test if input validation runs successful.
        """
        PlotOptions(
            "FIG", ROTATION, POSITION, prefix="xyz", id_method="random"
        ).validate_input()

    def test_prefix(self) -> None:
        """Test if Error is raised if prefix is not a string."""
        with self.assertRaises(TypeError):
            PlotOptions(["FIG"], ROTATION, POSITION, prefix=3).validate_input()

    def test_data_storage(self) -> None:
        """Test if Error is raised if id_method is not a string."""
        with self.assertRaises(TypeError):
            PlotOptions(["FIG"], ROTATION, POSITION, id_method=4).validate_input()

    def test_str_plotoptions(self) -> None:
        """
        Test if the string representation of a PlotOptions object is correct.
        """
        plot_obj = PlotOptions(
            "FIG",
            ROTATION,
            POSITION,
            prefix="xyz",
            id_method="random",
            id_on_plot=False,
        )
        self.assertEqual(
            str(plot_obj),
            "<class 'plotid.plotoptions.PlotOptions'>: {'figs': 'FIG', 'figure_ids': "
            "[], 'rotation': 270, 'position': (100, 200), 'prefix': 'xyz', 'id_method':"
            " 'random', 'qrcode': False, 'qr_position': (1, 0), 'qr_size': 100, "
            "'id_on_plot': False, 'font': False, 'fontsize': 12, 'fontcolor': "
            "(0, 0, 0)}",
        )

    def test_str_plotidtransfer(self) -> None:
        """
        Test if the string representation of a PlotIDTransfer object is
        correct.
        """
        transfer_obj = PlotIDTransfer("FIG", [])
        self.assertEqual(
            str(transfer_obj),
            "<class 'plotid.plotoptions.PlotIDTransfer'>: "
            "{'figs': 'FIG', 'figure_ids': []}",
        )


if __name__ == "__main__":
    unittest.main()
