import csv
import json
import os
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PDF_ENTRADA = os.path.join(BASE_DIR, "pdfs", "entrada.pdf")
PDF_OVERLAY = os.path.join(BASE_DIR, "pdfs", "overlay.pdf")
PDF_SAIDA   = os.path.join(BASE_DIR, "pdfs", "saida.pdf")
CSV_HORAS   = os.path.join(BASE_DIR, "results", "horas.csv")
CONFIG_PATH = os.path.join(BASE_DIR, "configs", "config.json")

X_ENTRADA = 120
X_SAIDA   = 300
X_ASSINATURA = 350

START_Y = 666
FONT_SIZE = 12
LINE_HEIGHT = FONT_SIZE * 1.21

def ler_config() -> dict:
    """Lê o arquivo de configuração e retorna um dicionário."""
    if not os.path.exists(CONFIG_PATH):
        return {}

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def ler_csv_horas(caminho_csv: str):
    """Itera sobre as linhas do CSV ignorando o cabeçalho."""
    with open(caminho_csv, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            yield row

def gerar_overlay(csv_path: str, pdf_overlay: str, configs: dict = None):
    """Gera o PDF de overlay com horários."""
    c = canvas.Canvas(pdf_overlay)
    c.setFont("Helvetica", FONT_SIZE)
    
    assinatura_cfg = configs.get("assinatura", {})
    tipo_assinatura = assinatura_cfg.get("tipo")
    texto_assinatura = assinatura_cfg.get("texto", "")
    caminho_assinatura = assinatura_cfg.get("arquivo", "")

    position_y = START_Y

    for dia, entrada, saida in ler_csv_horas(csv_path):
        if entrada.strip():
            c.drawString(X_ENTRADA, position_y, entrada)

        if saida.strip():
            c.drawString(X_SAIDA, position_y, saida)

        if saida.strip() and entrada.strip():
            if tipo_assinatura == "digitada":
                c.drawString(X_ASSINATURA, position_y, texto_assinatura)
            elif tipo_assinatura == "canvas":
                if os.path.exists(caminho_assinatura):
                    c.drawImage(
                        caminho_assinatura,
                        X_ASSINATURA,
                        position_y - 6,
                        width=80,
                        height=20,
                        preserveAspectRatio=True,
                        mask='auto'
                    )
        position_y -= LINE_HEIGHT

    c.save()

def merge_pdfs(pdf_base: str, pdf_overlay: str, pdf_saida: str):
    original = PdfReader(pdf_base)
    overlay = PdfReader(pdf_overlay)

    writer = PdfWriter()

    for i, page in enumerate(original.pages):
        if i == 0 and len(overlay.pages) > 0:
            page.merge_page(overlay.pages[0])
        writer.add_page(page)

    with open(pdf_saida, "wb") as f:
        writer.write(f)


def main():
    config = ler_config()

    csv_path = config.get("arquivos", {}).get("csv_horas", CSV_HORAS)

    gerar_overlay(csv_path, PDF_OVERLAY, config)
    merge_pdfs(PDF_ENTRADA, PDF_OVERLAY, PDF_SAIDA)


if __name__ == "__main__":
    main()
