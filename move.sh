#!/bin/bash
set -x
while read p; do
        mv "$p" ../home-backup-28.08.2020
done <names.txt
