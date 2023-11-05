#!/bin/bash

rm -rf "evilcorp.html"

if [ ! -f "evilcorp.html" ]; then
    cp "../materials/evilcorp.html" .
fi

python3.11 "exploit.py"