import pdfplumber
import os
import re

CARPETA_PDFS = "facturas"

for archivo in os.listdir(CARPETA_PDFS):

    if archivo.endswith(".pdf"):

        ruta = os.path.join(CARPETA_PDFS, archivo)

        with pdfplumber.open(ruta) as pdf:

            texto = ""

            for pagina in pdf.pages:

                contenido = pagina.extract_text()

                if contenido:
                    texto += contenido

        print("\n==============================")
        print("FACTURA:", archivo)
        print("==============================")

        # -------------------------
        # NUMERO FACTURA
        # -------------------------

        factura = re.search(
            r'Factura\\s*(\\d+)|Número de Factura\\s*(\\d+)',
            texto,
            re.IGNORECASE
        )

        numero_factura = None

        if factura:
            numero_factura = factura.group(1) or factura.group(2)

        # -------------------------
        # BASE
        # -------------------------

        base = re.search(
            r'Base imponible\\s*([\\d\\.,]+)',
            texto,
            re.IGNORECASE
        )

        base_imponible = None

        if base:
            base_imponible = base.group(1)

        # -------------------------
        # IVA
        # -------------------------

        iva = re.search(
            r'Cuota IVA\\s*([\\d\\.,]+)',
            texto,
            re.IGNORECASE
        )

        cuota_iva = None

        if iva:
            cuota_iva = iva.group(1)

        # -------------------------
        # TOTAL
        # -------------------------

        total = re.search(
            r'Importe total\\s*([\\d\\.,]+)',
            texto,
            re.IGNORECASE
        )

        total_factura = None

        if total:
            total_factura = total.group(1)

        # -------------------------
        # MOSTRAR
        # -------------------------

        print("Número factura:", numero_factura)
        print("Base imponible:", base_imponible)
        print("IVA:", cuota_iva)
        print("Total:", total_factura)
