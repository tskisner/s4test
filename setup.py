#!/usr/bin/env python3

import os
import sys
import re

import unittest
import shutil
import glob

from setuptools import find_packages, setup, Extension
from setuptools.command.test import test as TestCommand
from distutils.command.clean import clean as CleanCommand
from setuptools.command.build_ext import build_ext as BuildExt

import versioneer

# The setup options
setup_opts = dict()

# Entry points / scripts.  Add scripts here and define the main() of each
# script in s4sim.scripts.<foo>.main()
setup_opts["entry_points"] = {
    "console_scripts": ["s4sim_testscript = s4sim.scripts.testscript:main"]
}

setup_opts["name"] = "s4sim"
setup_opts["provides"] = ["s4sim"]
setup_opts["version"] = versioneer.get_version()
setup_opts["description"] = "CMB-S4 Example Package"
setup_opts["author"] = "CMB-S4 Collaboration"
setup_opts["author_email"] = "datamanagement@cmb-s4.org"
setup_opts["url"] = "https://github.com/CMB-S4/s4sim"
setup_opts["packages"] = find_packages(where=".")
setup_opts["license"] = "BSD"
setup_opts["requires"] = ["Python (>3.4.0)"]

# Command Class dictionary.
# Begin with the versioneer command class dictionary.
cmdcls = versioneer.get_cmdclass()

# Override the "clean" command to purge all build products.


class CustomClean(CleanCommand):
    def run(self):
        super().run()
        clean_files = [
            "./build",
            "./dist",
            "./tmp",
            "./__pycache__",
            "s4sim/__pycache__",
            "s4sim/*.so",
            "s4sim/tests/__pycache__",
            "s4sim/scripts/__pycache__",
            "./*.egg-info",
        ]
        for cf in clean_files:
            # Make paths absolute and relative to this path
            apaths = glob.glob(os.path.abspath(cf))
            for path in apaths:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                elif os.path.isfile(path):
                    os.remove(path)
        return


cmdcls["clean"] = CustomClean

# These classes allow us to build a compiled extension that uses pybind11.
# For more details, see:
#
#  https://github.com/pybind/python_example
#
# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689


def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile

    devnull = None
    oldstderr = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".cpp") as f:
            f.write("int main (int argc, char **argv) { return 0; }")
            try:
                devnull = open("/dev/null", "w")
                oldstderr = os.dup(sys.stderr.fileno())
                os.dup2(devnull.fileno(), sys.stderr.fileno())
                compiler.compile([f.name], extra_postargs=[flagname])
            except CompileError:
                return False
            return True
    finally:
        if oldstderr is not None:
            os.dup2(oldstderr, sys.stderr.fileno())
        if devnull is not None:
            devnull.close()


def cpp_flag(compiler):
    """Return the -std=c++[11/14] compiler flag.

    The c++14 is prefered over c++11 (when it is available).
    """
    if has_flag(compiler, "-std=c++14"):
        return "-std=c++14"
    elif has_flag(compiler, "-std=c++11"):
        return "-std=c++11"
    else:
        raise RuntimeError(
            "Unsupported compiler -- at least C++11 support " "is needed!"
        )


class CustomBuildExt(BuildExt):
    """A custom build extension for adding compiler-specific options."""

    c_opts = {"msvc": ["/EHsc"], "unix": []}

    if sys.platform.lower() == "darwin":
        c_opts["unix"] += ["-stdlib=libc++", "-mmacosx-version-min=10.7"]

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        linkopts = []
        if ct == "unix":
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, "-fvisibility=hidden"):
                opts.append("-fvisibility=hidden")
            if has_flag(self.compiler, "-fopenmp"):
                opts.append("-fopenmp")
                linkopts.append("-fopenmp")
            if sys.platform.lower() == "darwin":
                linkopts.append("-stdlib=libc++")
        elif ct == "msvc":
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args.extend(opts)
            ext.extra_link_args.extend(linkopts)
        BuildExt.build_extensions(self)


ext_modules = [
    Extension(
        "s4sim._s4sim",
        ["s4sim/fake.cpp", "s4sim/_s4sim.cpp"],
        include_dirs=["s4sim"],
        language="c++",
    )
]

setup_opts["ext_modules"] = ext_modules
cmdcls["build_ext"] = CustomBuildExt

# Add command class to setup options
setup_opts["cmdclass"] = cmdcls

# Do the setup.
setup(**setup_opts)
