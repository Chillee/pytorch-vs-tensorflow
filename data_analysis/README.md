### How to use (for one conference)
1. Download all the paper titles/authors/links to pdfs: python conference_downloader.py {icml/emnlp/cvpr/...} {year}
2. Actually download the pdfs: python download_pdfs.py data/{json file}
3. Extract text from pdfs for easy searching: ./extract_texts.sh
4. Generate data.csv containing data needed for pytorch vs tensorflow: python generate_data.py

### How to use (for multiple conferences)
1. Fill in conferences.txt with {conference} {year} on each line
2. ./download_from_file.sh conferences.txt
3. ls data/*.json | xargs -I {} -P8 sh -c "python download_pdfs.py {}"
4. ./extract_tests.sh

### Optional (if you want metadata to be stored in json files)
1. Generate "word lists" that contain ids of papers that contain strings: cat words | xargs -I {} ./gen_ids.sh {}
2. python gen_metadata.py

### Utilities
1. Clean up pdfs that aren't in any json files: python verify_pdfs.py
