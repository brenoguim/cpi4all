import html
import os

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

#myUL li a{
  border: 1px solid #ddd;
  margin-top: -1px; /* Prevent double borders */
  background-color: #f6f6f6;
  padding: 12px;
  text-decoration: none;
  font-size: 18px;
  color: black;
  display: block
}

#myUL li a:hover:not(.header) {
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
    txt = ""
    for (const doc of data) {
        var linetxt = ""
        var lineid = 1
        for (const line of doc) {
            if (line.indexOf(filter) > -1) {
                linetxt += "<tr><td>" + lineid.toString() +
                           "</td><td>        " + line + "</td></tr>\n"
            }
            lineid += 1
        }

        if (linetxt.length > 0) {
            txt += '<li><a href="#"><table>\n'
            txt += linetxt
            txt += '</table></a></li>\n'
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
for t in os.listdir(txts_dir):
    with open(os.path.join(txts_dir, t), 'r') as txtf:
        content.append(txtf.readlines())

with open("index.html", 'w') as outf:
    outf.write(pre_index)

    outf.write("const data = [");
    for c in content:
        outf.write("[");
        for cl in c:
            outf.write("'")
            outf.write(html.escape(cl.rstrip('\n'), True))
            outf.write("',\n")
        outf.write("],\n");
    outf.write("];")

    outf.write(pos_index)
