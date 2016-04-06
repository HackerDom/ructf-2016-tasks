#!/bin/bash

dd count=1 bs=128M if=/dev/zero of=fs
fdisk fs<<EOF
n



+32M
n




w
EOF
sudo kpartx -a fs
sudo mkfs.ext4 /dev/mapper/loop0p1
sudo mkfs.ntfs /dev/mapper/loop0p2
sudo mount /dev/mapper/loop0p2 /mnt
./trash.py /mnt
