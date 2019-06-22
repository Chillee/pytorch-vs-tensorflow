#!/bin/sh

cat $1 | while read conf year; do
    python conference_downloader.py $conf $year
    done
