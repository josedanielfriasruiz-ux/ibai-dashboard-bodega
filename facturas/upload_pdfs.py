import pdfplumber
import os

CARPETA_PDFS = "facturas"

for archivo in os.listdir(CARPETA_PDFS):

    if archivo.endswith(".pdf"):

        ruta = os.path.join(CARPETA_PDFS, archivo)

        with pdfplumber.open(ruta) as pdf:

            texto = ""

            for pagina in pdf.pages:
                texto += pagina.extract_text()

        print("FACTURA:", archivo)

        print(texto[:2000])
