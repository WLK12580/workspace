#!/bin/bash

builddir="./build"
if [ -d ${builddir} ];then
    echo "-- delete build"
    rm -rf ${builddir}
fi  
echo "delete build directory done!"
cmake -B ${builddir}
cmake --build ${builddir}/


if [ -d log ];then
   mv log ${builddir}/log
fi 
if [ -d install ];then
   mv install ${builddir}/install
fi 
