import json
import time
import requests
import concurrent.futures
import os
import subprocess

def convert_zip_to_txt(from_f, to_f):
    subprocess.run("python process_file.py {} {}".format(from_f, to_f), shell=True)

zipdir = 'database/zips'
txtdir = 'database/txts'

subprocess.run("mkdir -p {}".format(txtdir), shell=True)

with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    for zip in os.listdir(zipdir):
        from_f = os.path.join(zipdir, zip)
        to_f = os.path.join(txtdir, os.path.splitext(zip)[0] + ".txt")
        if not os.path.exists(to_f):
            executor.submit(convert_zip_to_txt, from_f, to_f)
