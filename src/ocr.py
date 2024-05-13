import os.path
import sys
from typing import Dict

from interface_OCR import InterfaceOCR
from multi_t_tess import multi_TesseractOCR

class OCR:
    def __init__(self):
        self.ocr_engines: Dict[str, InterfaceOCR] = {
            "multi": multi_TesseractOCR()
        }

    def extract_text(self, pdf_file: str, output_file: str, data: bool, ocr_engine: str = 'tesseract') -> None:
        self.ocr_engines[ocr_engine].extract_text(pdf_file, output_file, data)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(base_dir)

    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("-i", "--pdf", "--input-pdf", dest="input_pdf", default=f'{root_dir}/pdf/1221.30736.pdf',
                      action="store", type="string",
                      help="input PDF file PATH",
                      metavar="FILE")
    parser.add_option("-o", "--output", "--output-file", dest="output_text", default=f'{root_dir}/txt/output.txt',
                      action="store",
                      type="string",
                      help="output text file PATH",
                      metavar="FILE")
    parser.add_option("--metric", "--ocr-metric", dest="ocr_metric", default=f'tesseract',
                      action="store",
                      type="string",
                      help="ocr metric [tesseract|tika|pypdf|easy]",
                      metavar="STRING")
    parser.add_option("--ow", "--overwrite", "--over-write", dest="overwrite_mode", default=False,
                      action="store_true",
                      help="overwrite existing output files")
    parser.add_option("-d", "--data", "--input-data", dest="data", default=False, action="store_true",
                      help="Write OCR statistics")
                          
    (options, args) = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(0)
    
    OCR().extract_text(options.input_pdf, options.output_text, options.data, options.ocr_metric)
