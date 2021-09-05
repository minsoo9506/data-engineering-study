#!/usr/bash

x="Queen"
if [ $x == "King" ]; then
    echo "$x is a King"
else
    echo "$x is not a King"
fi

y=10
if [ $y -gt 5 ] && [ $y -lt 11 ]; then
    echo "$y is more than 5 and less than 11"
fi