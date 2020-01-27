// Copyright (c) 2020-2020 CMB-S4 Collaboration.

// Full license can be found in the top level "LICENSE" file.

#ifndef FAKE_HPP
#define FAKE_HPP

#include <string>
#include <vector>
#include <memory>


namespace s4sim {
// This class is a trivial example.

class FakeCompiled : public std::enable_shared_from_this <FakeCompiled> {
    public:

        typedef std::shared_ptr <FakeCompiled> pshr;
        typedef std::unique_ptr <FakeCompiled> puniq;

        FakeCompiled();

        std::vector <double> make_data(int n) const;
};
}
#endif // ifndef FAKE_HPP
