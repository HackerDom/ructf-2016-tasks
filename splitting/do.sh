#!/bin/sh

TAR_FILE=1.tar
OUTPUT_DIR=o

rm -rf $TAR_FILE $OUTPUT_DIR

./task.py $TAR_FILE
mkdir $OUTPUT_DIR
tar -xf $TAR_FILE -C $OUTPUT_DIR/
./solve.py $OUTPUT_DIR/*
