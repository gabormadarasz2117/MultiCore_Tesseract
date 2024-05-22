import os
import sys
import multiprocessing
import math
import pandas as pd
import psutil
import pytesseract

from multiprocessing.pool import ThreadPool
from pdf2image import convert_from_path

class multi_TesseractOCR():
    def __init__(self):
        pass

    def extract_text(self, args) -> None:
        pdf_file = args[0] + "/" + args[1]
        pdf_file = os.path.abspath(pdf_file)
        output_folder = os.path.abspath(args[3]) if args[3] else os.path.dirname(pdf_file)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print("Az output mappa nem létezett, létrehozva:", output_folder)
        output_file = os.path.join(output_folder, os.path.splitext(args[1])[0] + ".txt")
        data = args[4]
        images = convert_from_path(pdf_file)
        extracted_text = self._apply_ocr(images, lang=args[2])

        # Eredmény kiírása a TXT fájlba
        with open(output_file, 'w') as f:
            f.write(extracted_text)

        # OCR statisztika kiírása CSV fájlba
        if data:
            stats = self._extract_data(images)
            stats.to_csv(os.path.join(output_folder, os.path.splitext(args[1])[0] + "_dat.csv"), header=False, mode='a')
            print("A statisztika megtalálható a(z) '{}' fájlban.".format(os.path.join(output_folder, os.path.splitext(args[1])[0] + "_dat.csv")))

        # TODO: ezt majd át kell írni logging-ra
        print("OCR befejezve. Az eredmény megtalálható a(z) '{}' fájlban.".format(output_file))
        return

    def _apply_ocr(self, images, lang='hun'):
        extracted_text = [pytesseract.image_to_string(image, lang=lang) for image in images]
        return "".join(extracted_text)

    def _extract_data(self, images, lang='hun'):
        doc_conf = pd.Series()
        for image in images:
            image_data = pytesseract.image_to_data(image, lang=lang, output_type='data.frame')
            image_data = image_data[image_data.conf != -1]
            image_conf = pd.Series(image_data.conf)
            doc_conf = pd.concat([doc_conf, image_conf])
            
        doc_data = pd.DataFrame(doc_conf.describe())
        return doc_data


if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("-i", "--input-folder", dest="source_folder", default=None, action="store", type="string",
                      help="input folder PATH",
                      metavar="FILE")
    parser.add_option("-p", "--process", dest="proc_num", default=2, action="store",
                      type="int",
                      help="Number of processes",
                      metavar="INTEGER")
    parser.add_option("-l", "--lang", dest="lang", default="hun", action="store",
                      type="string",
                      help="Language of the documents",
                      metavar="STRING")
    parser.add_option("-o", "--output-folder", dest="output_folder", default=None, action="store", type="string",
                      help="output folder PATH",
                      metavar="FILE")
    parser.add_option("-d", "--data-output", dest="data_output", default=False, action="store",
                      help="Enable OCR statistics output",
                      metavar="BOOLEAN")
    
    (options, args) = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(0)
    
    max_proc_num = int(math.floor(multiprocessing.cpu_count() * 0.24))
    if options.proc_num > max_proc_num:
        print("Warning: Number of processes exceeds 24% of available CPUs. Setting process number to {}.".format(max_proc_num))
        options.proc_num = max_proc_num
    
    available_ram = psutil.virtual_memory().available / (1024 ** 3)
    if available_ram < (options.proc_num) * 10:
        print("Warning! The RAM can get overflowed based on the number of processes configured!")
    
    files_in_source_folder = [file for file in os.listdir(options.source_folder) if file.endswith('.pdf')]
    
    args = [(options.source_folder, pdf_file, options.lang, options.output_folder, options.data_output) for pdf_file in files_in_source_folder]
    with ThreadPool(processes=options.proc_num) as pool:
            # execute the task asynchronously
            pool.map(multi_TesseractOCR().extract_text, args)
            pool.close()
            pool.join()
            # display a message
            print("Done.")
