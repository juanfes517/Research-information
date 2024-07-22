from CvLAC.CvLAC import scrape_CvLAC
from ORCID.ORCID import scrape_ORCID
import pandas as pd
from docentes import docentes

def CvLAC():
  df_projects = pd.DataFrame(columns=["Docente", "Tipo_de_proyecto", "Nombre_del_proyecto", "Inicio", "Fin", "Resumen"])
  df_articles = pd.DataFrame(columns=["Docente", "Titulo_del_articulo", "pais", "revista", "año_de_publicacion", "paginas", "editorial", "DOI", "ISSN"])
  df_chaptersBooks = pd.DataFrame(columns=["Docente", "nombre_del_capitulo", "nombre_del_libro", "pais", "año", "editorial", "paginas", "ISBN"])

  scrape_CvLAC(df_projects=df_projects, df_articles=df_articles, df_chaptersBooks=df_chaptersBooks, docentes=docentes)
  df_projects.to_csv('resultados/CvLAC/projects.csv', index=False)
  df_articles.to_csv('resultados/CvLAC/articles.csv', index=False)
  df_chaptersBooks.to_csv('resultados/CvLAC/chaptersBooks.csv', index=False)

def ORCID():
  scrape_ORCID(docentes)


ORCID()



# Probar bien esto


import bibtexparser
import re

bibtex_str = r"""
@article{valdivieso2011virtual,
    title = {Virtual laboratory for simulation and learning of cardiovascular system function in BME studies},
    author = {Valdivieso, Hern{\'a}ndez and Mauricio, Alher y Salazar S{\'a}nchez, Mar{\'\i}a Bernarda y Urrego Higuita, David Alexander y Costa Castell{\'o}, Ramon y Ma{\~n}anas Villanueva, Miguel {\'A}ngel},
    journal = {Revista Facultad de Ingenier{\'i}a Universidad de Antioquia},
    number = {60},
    pages = {194--201},
    year = {2011},
    publisher = {Universidad de Antioquia}
}
"""

# Parse the BibTeX string
bib_database = bibtexparser.loads(bibtex_str)
entry = bib_database.entries[0]

# Function to replace BibTeX accents with Unicode characters
def replace_bibtex_accents(text):
    # Replace common accents
    replacements = {
        r"\\'a": "á", r"\\'e": "é", r"\\'i": "í", r"\\'o": "ó", r"\\'u": "ú",
        r"\\`a": "à", r"\\`e": "è", r"\\`i": "ì", r"\\`o": "ò", r"\\`u": "ù",
        r"\\^a": "â", r"\\^e": "ê", r"\\^i": "î", r"\\^o": "ô", r"\\^u": "û",
        r"\\~a": "ã", r"\\~o": "õ", r"\\~n": "ñ",
        r"\\u": "ŭ",
        r"\\c{c}": "ç", r"\\ss": "ß", r"\\AE": "Æ", r"\\ae": "æ", r"\\O": "Ø", r"\\o": "ø"
    }
    for bibtex, unicode_char in replacements.items():
        text = re.sub(bibtex, unicode_char, text)
    return text

# Extract and clean information
article_title = replace_bibtex_accents(entry.get('title', ''))
journal_name = replace_bibtex_accents(entry.get('journal', ''))
author = replace_bibtex_accents(entry.get('author', ''))
publication_year = entry.get('year', '')
pages = entry.get('pages', '')
publisher = replace_bibtex_accents(entry.get('publisher', ''))
issn = entry.get('issn', '')

# Print extracted information
print(f"Article Title: {article_title}")
print(f"Journal Name: {journal_name.replace('{', '').replace('}', '')}")
print(f"author: {author.replace('{', '').replace('}', '')}")
print(f"Publication Year: {publication_year}")
print(f"Pages: {pages}")
print(f"Publisher: {publisher}")
print(f"ISSN: {issn}")