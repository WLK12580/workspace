#!/bin/bash

builddir="./build"
if [ -d ${builddir} ];then
    echo "-- delete build"
    rm -rf ${builddir}
fi  
echo "-- delete build directory done!"
cmake -B build
cmake --build build/