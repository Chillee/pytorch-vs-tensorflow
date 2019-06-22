#!/bin/sh
getId() {
    echo $1 | cut -d : -f 1 | xargs -I {} basename {} .txt
}
grep -HiR "$1" --include \*.txt | while read -r line ; do
    id=$(getId $line)
    echo $id
done | tee "data/$1_t.ids"

cat "data/$1_t.ids" | sort | uniq > data/$1.ids
rm "data/$1_t.ids"

