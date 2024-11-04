#!/usr/bin bash

if [ "$#" -ne 2 ]; then
    echo "Usage: sh run.sh <k-mer length> <input file>"
    exit 1
fi

# 인자 받기
K=$1               # k-mer의 길이
INPUT_FILE=$2   

python3 my_k-mer_count.py "$K" "$INPUT_FILE" >./201815042.txt