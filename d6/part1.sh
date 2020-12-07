#!/bin/bash

awk -vRS="" '$1=$1' $1 | tr -d '[:blank:]' |\
 python3 part1.py 