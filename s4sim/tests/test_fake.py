# Copyright (c) 2020-2020 CMB-S4 Collaboration.
# Full license can be found in the top level "LICENSE" file.

"""Fake package test source file.
"""

from unittest import TestCase

from ..fake import fake_function


class FakeTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_fake(self):
        fc = fake_function()
        print(fc)
        data = fc.make_data(3)
        print(data, flush=True)
