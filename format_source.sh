#!/bin/bash
#
# Apply source code formatting.
#

# Get the directory containing this script
pushd $(dirname $0) > /dev/null
base=$(pwd -P)
popd > /dev/null

# Check executables
unexe=$(which uncrustify)
if [ "x${unexe}" = "x" ]; then
    echo "Cannot find the \"uncrustify\" executable.  Is it in your PATH?"
    exit 1
fi

blkexe=$(which black)
if [ "x${blkexe}" = "x" ]; then
    echo "Cannot find the \"black\" executable.  Is it in your PATH?"
    exit 1
fi

# The uncrustify config file
uncfg="${base}/uncrustify.cfg"

# Uncrustify runtime options per file
unrun="-c ${uncfg} --replace --no-backup"

# Uncrustify test options
untest="-c ${uncfg} --check"

# Black runtime options
blkrun="-l 88"

# Black test options
blktest="--check"

# Directories to process
cppdirs="s4sim"
pydirs="s4sim"

for cppd in ${cppdirs}; do
    find "${base}/${cppd}" -name "*.hpp" -not -path '*pybind11/*' -exec ${unexe} ${unrun} '{}' \;
    find "${base}/${cppd}" -name "*.cpp" -not -path '*pybind11/*' -exec ${unexe} ${unrun} '{}' \;
done

for pyd in ${pydirs}; do
    find "${base}/${pyd}" -name "*.py" -not -path '*pybind11/*' -exec ${blkexe} ${blkrun} '{}' \;
done
