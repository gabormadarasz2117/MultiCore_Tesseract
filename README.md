# Tesseract 5.0 OCR on N (X4) threads
Performs OCR on all .pdf files found in the input folder using Tesseract version 5.0. It processes N files simultaneously (on N*4 threads).

Note: Memory usage can be high when running multiple threads. It is advisable to consider that -p 10 = 100GB RAM!

## Install

### Build docker

```bash
bash ./build_docker.sh
```

## Run program on a folder
Options:

-i <PATH>: Path to the input folder (the folder containing PDF files to be OCR'd).

-o <PATH>: Path to the output folder (if not specified, .txt files will be saved in the input folder).

-p <int>: Number of processes. Default = 2 (Note: Tesseract uses 4 threads per process, so up to 24% of the processors can be used).

-l <string>: Language of the documents to be OCR'd. Default = "hun" (Note: Only Hungarian and English language dictionaries are installed).

-d <bool>: Model reliability regarding character recognition. Default = False.

```bash
python3 run_docker2.py -i /home/pdf -o /home/txt -p 10 -l hun -d True
```
