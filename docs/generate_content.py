import html
import os
import json

pre_index =  """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {
  box-sizing: border-box;
}

#myInput {
  background-image: url('/css/searchicon.png');
  background-position: 10px 12px;
  background-repeat: no-repeat;
  width: 100%;
  font-size: 16px;
  padding: 12px 20px 12px 40px;
  border: 1px solid #ddd;
  margin-bottom: 12px;
}

#myUL {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

#myUL li {
  border: 1px solid #ddd;
  margin-top: -1px; /* Prevent double borders */
  background-color: #f6f6f6;
  padding: 12px;
  text-decoration: none;
  font-size: 18px;
  color: black;
  display: block
}

#myUL li h5 {
  text-align: right
}

#myUL li :hover:not(.header) {
  background-color: #eee;
}
</style>
</head>
<body>

<h2>Procurar nos documentos da CPI</h2>

<input type="text" id="myInput" placeholder="Filtrar por..." title="Digite um termo para procurar">

<ul id="myUL">
</ul>

<script>
function generateDocumentLines(lines, filter, cid, visible_id) {
    var linetxt = ""
    var lineid = 1
    var skipped = false
    filter = filter.toUpperCase()
    for (const line of lines) {
        if (line.toUpperCase().indexOf(filter) > -1) {
            if (skipped) {
                linetxt += '<tr><td><a href="javascript:expand('+cid+','+visible_id+');">...</a></td><td></td></tr>\\n'
            }
            linetxt += "<tr><td>" + lineid.toString() +
                       "</td><td>" + line + "</td></tr>\\n"
            skipped = false 
        } else {
            skipped = true
        }
        lineid += 1
    }
    if (skipped && linetxt.length > 0) {
        linetxt += '<tr><td><a href="javascript:expand('+cid+','+visible_id+');">...</a></td><td></td></tr>\\n'
    }
    return linetxt
}


"""

pos_index = """
function myFunction(input) {
    const filter = input.value;

    const ul = document.getElementById("myUL");

    txt = ""
    cid = 0
    visible_id = 0
    for (const doc of data) {
        var linetxt = generateDocumentLines(doc["txt"], filter, cid, visible_id)

        if (linetxt.length > 0) {
            txt += '<li>'

            txt += '<h5>'

            txt += '| <a href="javascript:collapse('+cid+','+visible_id+');">Colapsar</a> '
            txt += '| <a href="javascript:expand('+cid+','+visible_id+');">Expandir</a> '
            txt += '| <a href="https://legis.senado.leg.br/comissoes/docsRecCPI?codcol=2441">Linha ' + doc["id"] + ', '
                 + 'Documento ' + doc["sub_id"] + '</a> |'
                 + ' <a href="' + doc["link"] + '">PDF</a> |'
            txt += '</h5>'

            txt += '<table style="width: 100%">\\n'
            txt += '<tbody>\\n'
            txt += linetxt
            txt += '</tbody>\\n'
            txt += '</table>'

            txt += '</li>\\n'
            visible_id += 1
        }
        cid += 1
    }
    ul.innerHTML = txt;
}

function load() {
    var input = document.getElementById("myInput")
    input.addEventListener('keyup', (event) => {
        if (event.which == 13 || event.key == 13) {
            event.preventDefault()
            myFunction(input)
        }
    });
}
document.addEventListener("DOMContentLoaded", load, false)

function expand(id, visible_id) {
    var ul = document.getElementById("myUL");
    var li = ul.getElementsByTagName("li")[visible_id];
    var table = li.getElementsByTagName("table")[0]
    var tbody = table.getElementsByTagName("tbody")[0]
    tbody.innerHTML = generateDocumentLines(data[id]["txt"], "", id, visible_id)
}

function collapse(id, visible_id) {
    var ul = document.getElementById("myUL");
    var li = ul.getElementsByTagName("li")[visible_id];
    var table = li.getElementsByTagName("table")[0]
    var tbody = table.getElementsByTagName("tbody")[0]

    var input = document.getElementById("myInput")
    const filter = input.value.toUpperCase();
    tbody.innerHTML = generateDocumentLines(data[id]["txt"], filter, id, visible_id)
}

</script>

</body>
</html>
"""

txts_dir = "../database/txts"
content = []

def get_base_id(filename):
    return int(os.path.basename(os.path.splitext(filename)[0]).split("_")[0])

def get_sub_id(filename):
    return int(os.path.basename(os.path.splitext(filename)[0]).split("_")[1])


txts = [os.path.join(txts_dir, t) for t in os.listdir(txts_dir)]
txts = sorted(txts, key=lambda k: get_base_id(k)*100 + get_sub_id(k))

for t in txts:
    c = dict() 

    with open(t, 'r') as txtf:
        c["txt"] = txtf.readlines()

    base_id = get_base_id(t)
    sub_id = get_sub_id(t)

    c["id"] = base_id
    c["sub_id"] = sub_id

    with open('../database/rows/{}.json'.format(base_id)) as jfile:
        j = json.load(jfile)
        c["link"] = j["links"][int(sub_id)-1]

    content.append(c)

with open("index.html", 'w') as outf:
    outf.write(pre_index)
    outf.write("const data = {}\n".format(json.dumps(content)))
    outf.write(pos_index)
