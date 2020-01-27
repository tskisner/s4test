// Copyright (c) 2020-2020 CMB-S4 Collaboration.

// Full license can be found in the top level "LICENSE" file.

#include <fake.hpp>


s4sim::FakeCompiled::FakeCompiled() {}

std::vector <double> s4sim::FakeCompiled::make_data(int n) const {
    std::vector <double> ret(n);
    for (auto & r : ret) {
        r = 5.0;
    }
    return ret;
}
