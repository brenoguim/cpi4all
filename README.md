# cpi4all
Repositorio com arquivos processados da CPI da COVID para facilitar analise

# Organização

No site do senado é possivel encontrar a lista de [todos os documentos](https://legis.senado.leg.br/comissoes/docsRecCPI?codcol=2441) coletados pela CPI da COVID.

A tabela no site possui a seguinte estrutura:

| No  |  Arquivos  | Data de recebimento | Remetente | Origem | Descrição | Caixa | Em Resposta |
| ----|------------| ------------------- | ----------|--------|-----------|-------| ------------|
|  1  |   Link1    |     ...             |     ...   | ...    |    ...    | ...   | ...         |
|  2  |Link2/link3 |     ...             |     ...   | ...    |    ...    | ...   | ...         |

Esses links levam ao download de arquivos PDF com os documentos em questão.

Nesse repositorio você podera encontrar a versão txt desses arquivos. O nome do arquivo nesse repositorio é formado por `<No do documento>_<numero do link>`.
Por exemplo:

  link1 = 1_1 porque ele é relativo ao arquivo No 1, e é o primeiro link.

  link2 = 2_1 porque ele é relativo ao arquivo No 2, e é o primeiro link dessa linha.

  link3 = 2_2 porque ele é relativo ao arquivo No 2, e é o segundo link da linha.
  
A versão texto de todos os documentos está na pasta database/txts/.

Exemplos:

[Arquivo No 1, primeiro link: 1_1](database/txts/1_1.txt)

[Arquivo No 4, quarto link: 3_4](database/txts/3_4.txt)




Nota 1: Nem todos os arquivos foram convertidos ainda

Nota 2: A conversão usa reconhecimento de imagem e pode ficar bem ruim as vezes, gerando erros ortograficos ou palavras sem nexo algum.
  
# Para desenvolvedores
  
Os scripts funcionam na seguinte sequencia:

1. `extract_rows.py`: Vai no site do senado e extrai as informações de cada linha da tabela. Todos os dados são salvos em `database/rows`.
2. `extract_headers.py`: Para cada link em cada linha, esse script pega metadados do arquivo (tamanho, tipo) que vão ser uteis depois. Esses dados são salvos em `database/headers`.
3. `download_pdfs.py`: Baixa todos os PDFs descritos em `database/headers` e salva em `database/pdfs`.
4. `convert_pdf_to_jpg.py`: Converte todos os PDFs em `database/pdfs` para imagens em `database/jpgs`.
5. `convert_jpg_to_txt.py`: Converte todos as imagens em `database/jpgs` para texto em `database/txt`.
  
Por motivos de performance, apenas as pastas `database/rows`, `database/headers` e `database/txts` sao salvas nesse repositorio.
  

TODO:
  0. Melhorar esse readme :)
  1. Usar o githubpages para gerar um site estatico que permite pesquisar em todos os txt
  2. Terminar de converter todos os arquivos
  3. Investigar arquivos em que a conversão ficou pessima.
  4. Fazer extração automatica de datas e prover um json com a ordem cronologica dos arquivos.
