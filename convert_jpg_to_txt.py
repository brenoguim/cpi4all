import json
import time
import requests
import concurrent.futures
import os
import subprocess

def convert_jpg_to_txt(from_f, to_f):
    subprocess.run("./jpg2txt {} {}".format(from_f, to_f), shell=True)

jpgdir = 'database/jpgs'
txtdir = 'database/txts'

subprocess.run("mkdir -p {}".format(txtdir), shell=True)

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    for jpg in os.listdir(jpgdir):
        from_f = os.path.join(jpgdir, jpg)
        to_f = os.path.join(txtdir, os.path.splitext(jpg)[0] + '.txt')
        if not os.path.exists(to_f):
            executor.submit(convert_jpg_to_txt, from_f, to_f)
