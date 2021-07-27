import json
import time
import requests
import concurrent.futures
import os
import subprocess

def is_pdf(cid):
    with open('database/headers/{}.json'.format(cid), 'r') as fhdr:
        jhdr = json.load(fhdr)
        if 'pdf' in jhdr['Content-Type']:
            return True
    return False 

def get_size(cid):
    with open('database/headers/{}.json'.format(cid), 'r') as fhdr:
        jhdr = json.load(fhdr)
        if 'Content-Length' in jhdr:
            return int(jhdr['Content-Length'])
    return 100000000

def already_consumed(cid):
    return os.path.exists("database/txts/{}.txt".format(cid))

def download(cid, link):
    subprocess.run("wget -O database/tmp/{}.pdf {} && mv database/tmp/{}.pdf database/pdfs/".format(cid, link, cid), shell=True)
    

rowdir = 'database/rows'
pdfdir = 'database/pdfs'
subprocess.run("mkdir -p {}".format(pdfdir), shell=True)
subprocess.run("mkdir -p database/tmp", shell=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futs = []
    to_download = []
    for row in os.listdir(rowdir):
        with open(os.path.join(rowdir,row), 'r') as frow:
            jrow = json.load(frow)
            subid = 0
            for link in jrow['links']:
                subid += 1
                cid = '{}_{}'.format(jrow['id'], subid)
                if is_pdf(cid) and not already_consumed(cid):
                    to_download.append( (cid, link, get_size(cid) ) )
    for el in sorted(to_download, key = lambda el: el[2]):
        executor.submit(download, el[0], el[1])

