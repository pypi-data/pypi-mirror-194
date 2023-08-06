#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unittests for create_id
"""

import unittest
import qrcode
import plotid.create_id as cid
from plotid.create_id import create_qrcode


class TestCreateID(unittest.TestCase):
    """
    Class for all unittests of the create_id module.
    """

    def test_existence(self) -> None:
        """Test if create_id returns a string."""
        self.assertIsInstance(cid.create_id("time"), str)
        self.assertIsInstance(cid.create_id("random"), str)

    def test_errors(self) -> None:
        """Test if Errors are raised when id_method is wrong."""
        with self.assertRaises(ValueError):
            cid.create_id(3)
        with self.assertRaises(ValueError):
            cid.create_id("h")

    def test_length(self) -> None:
        """Test if figure_id has the correct length."""
        self.assertEqual(len(cid.create_id("time")), 10)
        self.assertEqual(len(cid.create_id("random")), 8)

    def test_qrcode(self) -> None:
        """Test if qrcode returns a image."""
        self.assertIsInstance(create_qrcode("test_ID"), qrcode.image.pil.PilImage)


if __name__ == "__main__":
    unittest.main()
