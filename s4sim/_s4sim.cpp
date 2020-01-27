#include <string>
#include <sstream>

#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include <pybind11/stl_bind.h>

// Include headers for our various compiled sources.
#include <fake.hpp>

namespace py = pybind11;


PYBIND11_MODULE(_s4sim, m) {
    m.doc() = R"(
    Internal compiled tools for the s4sim package.

    )";

    py::class_ <
        s4sim::FakeCompiled,      // The class to wrap
        s4sim::FakeCompiled::pshr // The smart pointer class to use
        > (
        m, "FakeCompiled", R"(
        Simple fake class.

        This class is just a fake example...

        )"
        )
    .def(py::init < > ())
    .def("make_data", &s4sim::FakeCompiled::make_data, py::arg(
             "n"),
         R"(
        Make some data.

        Args:
            n (int):  The number of data points

        Returns:
            (array):  An array of some fake data.
    )")
    .def("__repr__",
         [](s4sim::FakeCompiled const & self) {
             std::ostringstream o;
             o << "<s4sim.FakeCompiled ";
             o << ">";
             return o.str();
         }
         );
}
