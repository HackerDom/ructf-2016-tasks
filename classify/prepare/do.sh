#!/bin/bash

./generate.py
svm-train -t 1 train.txt model
