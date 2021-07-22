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
function myFunction(input) {

"""

pos_index = """
    const filter = input.value.toUpperCase();

    const ul = document.getElementById("myUL");

    function generateDocumentLines(lines, filter) {
        var linetxt = ""
        var lineid = 1
        var skipped = false
        for (const line of lines) {
            if (line.indexOf(filter) > -1) {
                if (skipped) {
                    linetxt += "<tr><td>...</td><td></td></tr>\\n"
                }
                linetxt += "<tr><td>" + lineid.toString() +
                           "</td><td>" + line + "</td></tr>\\n"
                skipped = false 
            } else {
                skipped = true
            }
            lineid += 1
        }
        return linetxt
    }


    txt = ""
    for (const doc of data) {
        var linetxt = generateDocumentLines(doc["txt"], filter)

        if (linetxt.length > 0) {
            txt += '<li>'

            txt += '<h5>'
            txt += '|<a href="https://legis.senado.leg.br/comissoes/docsRecCPI?codcol=2441">Linha ' + doc["id"] + ', '
                 + 'Documento ' + doc["sub_id"] + '</a>|'
                 + '<a href="' + doc["link"] + '">PDF</a>|'
            txt += '</h5>'

            txt += '<table>\\n'
            txt += linetxt
            txt += '</table>'

            txt += '</li>\\n'
        }
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
</script>

</body>
</html>
"""

txts_dir = "../database/txts"
content = []

txts = [os.path.join(txts_dir, t) for t in os.listdir(txts_dir)]
txts = sorted(txts)

for t in txts:
    c = dict() 

    with open(t, 'r') as txtf:
        c["txt"] = txtf.readlines()

    base_id = os.path.basename(os.path.splitext(t)[0]).split("_")[0]
    sub_id = os.path.basename(os.path.splitext(t)[0]).split("_")[1]

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
