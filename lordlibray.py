import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup  
import spacy 
import Levenshtein

nlp = spacy.load("pt_core_news_sm")

hsh_global = {}

def spac_analy(doc):
    for ent in doc.ents:
        if ent.label_ == "PER":
            nome = ent.text.strip()
            hsh_global[nome] = hsh_global.get(nome, 0) + 1

def book_ext(arquivo):
    livro = epub.read_epub(arquivo)
    cap = []

    for item in livro.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text = soup.get_text().strip()

            if len(text) > 100:
                cap.append(text)

    for i, doc in enumerate(nlp.pipe(cap, batch_size=2)):
        print(f"--- Analisando Capítulo {i+1} ---")
        spac_analy(doc)

    print("\n--- Iniciando Análise de Discrepâncias ---")
    lev_dis()

def lev_dis():
    verdades = [n for n, f in hsh_global.items() if f > 5]
    suspeitos = [n for n, f in hsh_global.items() if f <= 2]

    for s in suspeitos:
        for v in verdades:
            dist = Levenshtein.distance(s, v)
            if 0 < dist <= 2:
                print(f"Possível erro encontrado: '{s}' (aparece {hsh_global[s]}x) "
                      f"pode ser '{v}' (aparece {hsh_global[v]}x)") 
    
book_ext('O_Senhor_dos_Anéis_Parte_1.epub')





