#!/bin/bash

builddir="./build"
if [ -d ${builddir} ];then
    echo "delete build"
    rm -rf ${builddir}
fi  
sleep 0.5
cmake -B build
cmake --build build/