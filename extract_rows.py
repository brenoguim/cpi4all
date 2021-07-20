from bs4 import BeautifulSoup
import json
import time
import requests
import concurrent.futures
import os
import subprocess

def collect_row_data(id2file, trow):
    cnt=0
    data=dict()
    for d in trow.find_all('td'):
        cnt+=1
        if (cnt == 1):
            n=int(d.get_text())
            data["id"] = n

        if (cnt == 2):
            links=[]
            subcnt = 0
            for link in d.find_all('a'):
                links.append(str(link['href']))
                subcnt += 1
            data["links"] = links

        if (cnt == 3):
            data["data_recebimento"] = str(d.get_text())

        if (cnt == 4):
            data["remetente"] = str(d.get_text())

        if (cnt == 5):
            data["origem"] = str(d.get_text())

        if (cnt == 6):
            data["descricao"] = str(d.get_text())

        if (cnt == 7):
            data["caixa"] = str(d.get_text())

        if (cnt == 7):
            data["em_resposta"] = str(d.get_text())

    if "id" in data and len(data["links"]):
        id2data[data["id"]] = data

def print_meta(id2data):
    subprocess.run("mkdir -p database/rows", shell=True)
    all=[]
    for i in id2data:
        file_name = "database/rows/{}.json".format(i)
        if not os.path.exists(file_name):
            meta = open(file_name, 'w')
            meta.write(json.dumps(id2data[i]))
            meta.close()

subprocess.run("wget -O main.html https://legis.senado.leg.br/comissoes/docsRecCPI?codcol=2441", shell=True)

id2data=dict()
file = open("main.html", 'r')
soup = BeautifulSoup(file, features="html.parser")

tab = soup.find_all('div', class_='panel panel-default')[0]
tab = tab.find_all('table')[0]

id2data=dict()

for r in tab.find_all('tr'):
    collect_row_data(id2data, r)

print_meta(id2data)

subprocess.run("rm -rf main.html", shell=True)
