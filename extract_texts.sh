#!/bin/sh
cnt=0
ls data/pdfs/*.pdf | while read file; do
    if [ -f "${file%.*}.txt" ]; then
        echo "skipping $file"
    else
        echo "converting $file"
        pdftotext $file
    fi
done

