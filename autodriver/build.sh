#!/bin/bash

build="./build"
if [ -d ${build} ];then
    echo "-- delete build"
    rm -rf ${build}
fi  
echo "delete build directory done!"
cmake -B ${build}
cmake --build ${build}/

if [ -d log ];then
   mv log ${build}/log
fi 
if [ -d install ];then
   mv install ${build}/install
fi 
