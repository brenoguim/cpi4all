import json
import time
import requests
import concurrent.futures
import os
import subprocess

def convert_image_to_txt(from_f, to_f):
    subprocess.run("./image2txt {} {}".format(from_f, to_f), shell=True)

imagedir = 'database/images'
txtdir = 'database/txts'

subprocess.run("mkdir -p {}".format(txtdir), shell=True)

with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    for image in os.listdir(imagedir):
        from_f = os.path.join(imagedir, image)
        to_f = os.path.join(txtdir, os.path.splitext(image)[0] + '.txt')
        if not os.path.exists(to_f):
            executor.submit(convert_image_to_txt, from_f, to_f)
