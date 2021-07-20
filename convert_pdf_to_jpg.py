import json
import time
import requests
import concurrent.futures
import os
import subprocess

def convert_pdf_to_jpg(from_f, to_f):
    subprocess.run("./pdf2jpg {} {}".format(from_f, to_f), shell=True)

pdfdir = 'database/pdfs'
jpgdir = 'database/jpgs'

subprocess.run("mkdir -p {}".format(jpgdir), shell=True)

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    for pdf in os.listdir(pdfdir):
        from_f = os.path.join(pdfdir, pdf)
        to_f = os.path.join(jpgdir, os.path.splitext(pdf)[0] + '.jpg')
        if not os.path.exists(to_f) and os.stat(from_f).st_size < 10000000:
            executor.submit(convert_pdf_to_jpg, from_f, to_f)
