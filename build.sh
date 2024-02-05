#!/bin/bash

builddir="./buildDir"
if [ -d ${builddir} ];then
    echo "-- delete build"
    rm -rf ${builddir}
fi  
echo "-- delete build directory done!"
cmake -B builddir
cmake --build builddir/