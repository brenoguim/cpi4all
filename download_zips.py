import json
import time
import requests
import concurrent.futures
import os
import subprocess

def is_zip(cid):
    with open('database/headers/{}.json'.format(cid), 'r') as fhdr:
        jhdr = json.load(fhdr)
        if 'zip' in jhdr['Content-Type']:
            return True
    return False 

def get_size(cid):
    with open('database/headers/{}.json'.format(cid), 'r') as fhdr:
        jhdr = json.load(fhdr)
        if 'Content-Length' in jhdr:
            return int(jhdr['Content-Length'])
    return 100000000

def already_downloaded(cid):
    return os.path.exists("database/zips/{}.zip".format(cid))

def already_processed(cid):
    return os.path.exists("database/txts/{}.txt".format(cid))

def download(cid, link):
    subprocess.run("wget -O database/tmp/{}.zip {} && mv database/tmp/{}.zip database/zips/".format(cid, link, cid), shell=True)
    subprocess.run("python3 process_file.py database/zips/{}.zip database/txts/{}.txt".format(cid, cid), shell=True)
    subprocess.run("rm -rf database/zips/{}.zip".format(cid, link, cid, cid), shell=True)
    

rowdir = 'database/rows'
zipdir = 'database/zips'
subprocess.run("mkdir -p {}".format(zipdir), shell=True)
subprocess.run("mkdir -p database/tmp", shell=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    futs = []
    to_download = []
    for row in os.listdir(rowdir):
        with open(os.path.join(rowdir,row), 'r') as frow:
            jrow = json.load(frow)
            subid = 0
            for link in jrow['links']:
                subid += 1
                cid = '{}_{}'.format(jrow['id'], subid)
                if is_zip(cid) and not already_downloaded(cid) and not already_processed(cid):
                    to_download.append( (cid, link, get_size(cid) ) )
    for el in sorted(to_download, key = lambda el: el[2]):
        executor.submit(download, el[0], el[1])

