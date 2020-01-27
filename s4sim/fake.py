# Copyright (c) 2020-2020 CMB-S4 Collaboration.
# Full license can be found in the top level "LICENSE" file.

"""Fake package source file.
"""

# This is a fake package file.  Delete this after creating a new package from the
# example template.

# As part of this example, import a fake class defined in the compiled
# extension.

from ._s4sim import FakeCompiled


def fake_function():
    fc = FakeCompiled()
    return fc
