import json
import time
import requests
import concurrent.futures
import os
import sys
import subprocess
import tempfile

def process_zip(from_path, to_path):
    with tempfile.TemporaryDirectory() as tmpdirname:
        subprocess.run('unzip {} -d {}'.format(from_path, tmpdirname), shell=True)
        # rename files
        remap=[]
        cnt=1
        for base, dirs, files in os.walk(tmpdirname):
            for f in files:
                new_f = os.path.join(tmpdirname, "cpi4all_{}_{}".format(cnt, f.replace(" ", "__")))
                os.rename(os.path.join(base, f), new_f)
                remap.append([new_f, os.path.join(tmpdirname, "cpi4all_output_{}.txt".format(cnt))])
                cnt+=1

        for f,t in remap:
            print("Processing: {} => {}".format(f,t))
            subprocess.run(["python", "process_file.py", f, t])
        
        subprocess.run('cat {} > {}'.format(" ".join([t for _,t in remap]), to_path), shell=True)
        

def process_pdf(from_path, to_path):
    subprocess.run('./pdf2txt {} {}'.format(from_path, to_path), shell=True)

def process_txt(from_path, to_path):
    subprocess.run('cp {} {}'.format(from_path, to_path), shell=True)

def process_xls(from_path, to_path):
    subprocess.run('ssconvert {} {}'.format(from_path, to_path), shell=True)

def process_unsupported(from_path, to_path):
    with open(to_path, 'w') as outf:
        outf.write("cpi4all_arquivo_nao_suportado: {}\n".format(from_path))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit("Bad args")

    from_path = sys.argv[1]
    to_path = sys.argv[2]

    if not os.path.exists(from_path):
        raise SystemExit("Source file does not exist: {}".format(from_path))

    if os.path.exists(to_path):
        raise SystemExit("Destination path already exists: {}".format(to_path))

    ext_list = os.path.splitext(from_path)
    ext = ""
    if len(ext_list) == 2:
        ext = ext_list[-1]

    ext = ext.lower()

    if ext == ".zip":
        process_zip(from_path, to_path)

    elif ext == ".pdf":
        process_pdf(from_path, to_path)

    elif ext == ".txt" or ext == ".html" or ext == ".csv" or ext == ".xml":
        process_txt(from_path, to_path)

    elif ext == ".xls" or ext == ".xlsx" or ext == ".sxc" or ext == ".ods":
        process_xls(from_path, to_path)

    else:
        process_unsupported(from_path, to_path)
