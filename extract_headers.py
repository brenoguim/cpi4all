import json
import time
import requests
import concurrent.futures
import os
import subprocess

def extract_header(url, filename):
    if not os.path.exists(filename):
        print("Extracting header for {}".format(filename))
        h = requests.head(url)
        with open(filename, 'w') as hdr:
            json.dump(dict(h.headers), hdr)

rowdir = 'database/rows'
hdrdir = 'database/headers'
subprocess.run("mkdir -p {}".format(hdrdir), shell=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futs = []
    for row in os.listdir(rowdir):
        with open(os.path.join(rowdir,row), 'r') as frow:
            jrow = json.load(frow)
            subid = 0
            for link in jrow['links']:
                subid += 1
                hdr_name = '{}/{}_{}.json'.format(hdrdir, jrow['id'], subid)
                if not os.path.exists(hdr_name):
                    executor.submit(extract_header, link, hdr_name)
    
