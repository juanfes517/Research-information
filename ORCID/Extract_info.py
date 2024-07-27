import bibtexparser

def extract_books(citation):
  bib_database = bibtexparser.loads(citation)

  # Extract the information
  for entry in bib_database.entries:
    titulo = quitar_caracteres(entry.get('title', ''))
    juournal = quitar_caracteres(entry.get('journal', ''))
    año = quitar_caracteres(entry.get('year', ''))
    volumen = quitar_caracteres(entry.get('volume', ''))
    paginas = quitar_caracteres(entry.get('pages', ''))
    autores = quitar_caracteres(entry.get('author', ''))
    
    return [titulo, juournal, año, volumen, paginas, autores]


def extract_chaptersBooks(citation):
  bib_database = bibtexparser.loads(citation)

  # Extract the information
  for entry in bib_database.entries:
    doi = quitar_caracteres(entry.get('doi', ''))
    url = quitar_caracteres(entry.get('url', ''))
    año = quitar_caracteres(entry.get('year', ''))
    editorial = quitar_caracteres(entry.get('publisher', ''))
    paginas = quitar_caracteres(entry.get('pages', ''))
    autores = quitar_caracteres(entry.get('author', ''))
    nombre_del_capitulo = quitar_caracteres(entry.get('title', ''))
    nombre_del_libro = quitar_caracteres(entry.get('booktitle', ''))
    
    return [doi, url, año, editorial, paginas, autores, nombre_del_capitulo, nombre_del_libro]


def extract_conferencePaper(citation):
  bib_database = bibtexparser.loads(citation)

  # Extract the information
  for entry in bib_database.entries:
    titulo = quitar_caracteres(entry.get('title', ''))
    revista = quitar_caracteres(entry.get('journal', ''))
    año = quitar_caracteres(entry.get('year', ''))
    volumen = quitar_caracteres(entry.get('volume', ''))
    paginas = quitar_caracteres(entry.get('pages', ''))
    autores = quitar_caracteres(entry.get('author', ''))
    
    return [titulo, revista, año, volumen, paginas, autores]


def extract_articles(citation):
  bib_database = bibtexparser.loads(citation)

  # Extract the information
  for entry in bib_database.entries:
    titulo = quitar_caracteres(entry.get('title', ''))
    revista = quitar_caracteres(entry.get('journal', ''))
    año = quitar_caracteres(entry.get('year', ''))
    mes = quitar_caracteres(entry.get('month', ''))
    doi = quitar_caracteres(entry.get('doi', ''))
    url = quitar_caracteres(entry.get('url', ''))
    editorial = quitar_caracteres(entry.get('publisher', ''))
    volumen = quitar_caracteres(entry.get('volume', ''))
    numero = quitar_caracteres(entry.get('number', ''))
    paginas = quitar_caracteres(entry.get('pages', ''))
    autores = quitar_caracteres(entry.get('author', ''))

    
    return [titulo, revista, año, mes, doi, url, editorial, volumen, numero, paginas, autores]

# Quita cierto caracteres de un string
def quitar_caracteres(text):
    replacements = {
        '{': '',
        '}': '',
        "'": '',
        "\\": '',
        '~n': 'ñ'
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text

