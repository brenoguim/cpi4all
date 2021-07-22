import html
import os

txts_dir = "../database/txts"
content = []
for t in os.listdir(txts_dir):
    with open(os.path.join(txts_dir, t), 'r') as txtf:
        content.append(txtf.readlines())

with open("index.html", 'w') as outf:
    with open("pre_index.html", 'r') as inf:
        outf.write(inf.read())

    outf.write("const data = [");
    for c in content:
        outf.write("[");
        for cl in c:
            outf.write("'")
            outf.write(html.escape(cl.rstrip('\n'), True))
            outf.write("',\n")
        outf.write("],\n");
    outf.write("];")

    with open("pos_index.html", 'r') as inf:
        outf.write(inf.read())
