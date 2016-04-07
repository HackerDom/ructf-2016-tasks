#!/bin/bash

sync
sudo umount /mnt
fdisk fs <<EOF
d
1
d
w
EOF
