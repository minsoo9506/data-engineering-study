#!/usr/bash

function print_hello() {
    echo "Hi~"
}

print_hello

function print_filename {
    echo "The first file is $1"
    for file in $@
    do
        echo "This file is $file"
    done
}

print_filename "file1.txt" "file2.txt"

function return_check {
    echol
}

return_check

echo $?

function sum {
  echo $(expr $1 + $2)
}
result=$(sum 1 20)
echo $result # 21