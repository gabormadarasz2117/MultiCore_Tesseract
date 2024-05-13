import logging
import os
import sys
from subprocess import Popen, PIPE, STDOUT

logger = logging.getLogger(__name__)
base_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(base_dir)


def run_docker_ocr(input_folder: str, output_folder = "", proc_num: int = 2, lang="hun", dev_mode: bool = False, data = False):
    input_folder = os.path.abspath(input_folder)
    output_folder = os.path.abspath(output_folder) if output_folder else os.path.abspath(input_folder)
    mount_code_dir = ""
    if dev_mode:
        mount_code_dir = f"-v {base_dir}/src:/code/src"
    # --gpus all
    command = f'docker run -u $(id -u) {mount_code_dir} -v {input_folder}:{input_folder} -i --rm --entrypoint "" docker.nlp.nytud.hu/multitess:20230319 python3 /code/src/multi_t_tess.py -i {input_folder} -o {output_folder} -p {proc_num} -l {lang} -d {data}'

    logger.debug(f"OCR docker command: {command}")
    out, err = Popen([command], shell=True, close_fds=True, stdout=PIPE, stderr=STDOUT).communicate()
    print(f"OUT: {out.decode('utf-8')}")
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("-i", "--input", "--input_folder", dest="source_folder",
                      action="store", type="string",
                      help="input folder PATH",
                      metavar="FILE")
    parser.add_option("-p", "--processes", dest="proc_num",
                      action="store",
                      type="int",
                      help="number of processes",
                      metavar="INTEGER")
    parser.add_option("-o", "--output_folder", dest="output_folder",
                      action="store", type="string",
                      help="output folder PATH",
                      metavar="FILE")
    parser.add_option("--dev_mode", dest="dev",
                      action="store", type="string", default=False,
                      help="developer mode",
                      metavar="BOOL")
    parser.add_option("-d", "--data-output", dest="data_output", default=False, action="store",
                      help="Enable OCR statistics output csv file",
                      metavar="BOOLEAN")
    parser.add_option("-l", "--lang", dest="lang", default="hun", action="store",
                      type="string",
                      help="Language of the documents",
                      metavar="STRING")
        
    (options, args) = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(0)

    run_docker_ocr(options.source_folder, options.output_folder, options.proc_num, options.lang, options.dev, options.data_output)