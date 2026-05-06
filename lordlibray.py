import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup  
import spacy 

nlp = spacy.load("pt_core_news_sm")

def book_ext(arquivo):
    livro = epub.read_epub(arquivo)
    cap = []

    for item in livro.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text = soup.get_text().strip()

            if len(text) > 100:
                cap.append(text)

    for i, doc in enumerate(nlp.pipe(cap, batch_size=1)):
        print(f"--- Analisando Capítulo {i+1} ---")
        verificar_erros(doc)

def verificar_erros(doc):
    # test erros de digitação ou nomes próprios em minúsculo
    for ent in doc.ents:
        if ent.label_ == "PER": # PERsonagens 
            print(f"Entidade encontrada: {ent.text}")

book_ext('O_Senhor_dos_Anéis_Parte_1.epub')





