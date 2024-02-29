#!/bin/bash
g++ -o mysql_test ./*.cpp -lmysqlclient -lspdlog -g -std=c++11
