#!/bin/bash

dir=tests/integration/
iterate_over_folder() {
    filenames=$(find $dir -name "*.py")
    for filename in $filenames; do
        echo "Running test in: "$filename
        python3 ${filename}
    done
}

iterate_over_folder