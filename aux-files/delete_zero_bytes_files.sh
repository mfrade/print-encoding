#!/bin/bash

for file in CharNames--*.txt; do
    if [ ! -f "clean/$file" ]; then
        grep -v '<unknown>' "$file" > "clean/$file"
        if [ ! -s "clean/$file" ]; then # check if the file is empty
            rm "clean/$file" # delete the file
        fi
    fi
done
