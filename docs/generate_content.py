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

    for c in content:
        outf.write('<li><a href="#">\n')
        outf.write('<ol>\n')
        for cl in c:
            outf.write('    <li class="document_line">{}</li>\n'.format(html.escape(cl).rstrip('\n')))
            #outf.write('    {}\n'.format(html.escape(cl).rstrip('\n')))
        outf.write("</ol>")
        outf.write("</a></li>\n")

    with open("pos_index.html", 'r') as inf:
        outf.write(inf.read())
