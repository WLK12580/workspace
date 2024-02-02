#!/bin/bash

builddir="./build"
if [ -d ${builddir} ];then
    echo "delete build"
    rm -rf ${builddir}
fi  
cmake -B build
cmake --build build/