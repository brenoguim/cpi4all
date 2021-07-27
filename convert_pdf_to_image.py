import json
import time
import requests
import concurrent.futures
import os
import subprocess

def convert_pdf_to_image(from_f, to_f):
    subprocess.run("./pdf2image {} {}".format(from_f, to_f), shell=True)

pdfdir = 'database/pdfs'
imagedir = 'database/images'
txtdir = 'database/txts'

subprocess.run("mkdir -p {}".format(imagedir), shell=True)

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    for pdf in os.listdir(pdfdir):
        from_f = os.path.join(pdfdir, pdf)
        to_f = os.path.join(imagedir, os.path.splitext(pdf)[0])
        txt_f = os.path.join(txtdir, os.path.splitext(pdf)[0])
        if not os.path.exists(to_f) and not os.path.exists(txt_f):
            executor.submit(convert_pdf_to_image, from_f, to_f)
