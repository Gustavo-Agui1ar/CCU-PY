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


def report(cb, msg, value):
    if cb:
        cb(msg, value)


def ler_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        return {}

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def ler_csv_horas(caminho_csv: str):
    with open(caminho_csv, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            yield row

def get_configs_values(configs: dict) -> tuple:
    assinatura_cfg = configs.get("assinatura", {})
    tipo_assinatura = assinatura_cfg.get("tipo")
    texto_assinatura = assinatura_cfg.get("texto", "")
    caminho_assinatura = assinatura_cfg.get("arquivo", "")

    return tipo_assinatura, texto_assinatura, caminho_assinatura

def draw_assinatura(c: canvas.Canvas, tipo: str, texto: str, caminho: str, position_y: int):
    if tipo == "digitada":
        c.drawString(X_ASSINATURA, position_y, texto)
    elif tipo == "canvas" and os.path.exists(caminho):
        c.drawImage(caminho, X_ASSINATURA, position_y - 6, width=80, height=20, preserveAspectRatio=True, mask="auto")

def draw_line(c: canvas.Canvas, entrada: str, inicio_intercalo: str, fim_intercalo: str, saida: str, position_y: int):
    if entrada.strip():
        c.drawString(X_ENTRADA, position_y, entrada)

    if inicio_intercalo.strip() and fim_intercalo.strip():
        pos_intervalo_entrada = X_ENTRADA + abs(X_ENTRADA - X_SAIDA) / 3
        pos_intervalo_saida = X_ENTRADA + 2 * abs(X_ENTRADA - X_SAIDA) / 3
        c.drawString(pos_intervalo_entrada, position_y, inicio_intercalo)
        c.drawString(pos_intervalo_saida, position_y, fim_intercalo)

    if saida.strip():
        c.drawString(X_SAIDA, position_y, saida)

def gerar_overlay(csv_path: str, pdf_overlay: str, configs: dict, on_progress=None):
    report(on_progress, "Gerando overlay do PDF", 0.4)

    c = canvas.Canvas(pdf_overlay)
    c.setFont("Helvetica", FONT_SIZE)

    tipo_assinatura, texto_assinatura, caminho_assinatura = get_configs_values(configs)

    linhas = list(ler_csv_horas(csv_path))
    total = len(linhas)

    position_y = START_Y

    for i, (dia, entrada, inicio_intercalo, fim_intercalo, saida) in enumerate(linhas):
        
        draw_line(c, entrada, inicio_intercalo, fim_intercalo, saida, position_y)

        if saida.strip() and entrada.strip():
            draw_assinatura(c, tipo_assinatura, texto_assinatura, caminho_assinatura, position_y)

        position_y -= LINE_HEIGHT

        progress = 0.4 + (i / max(total, 1)) * 0.4
        report(on_progress, f"Processando registros ({i+1}/{total})", progress)

    c.save()
    report(on_progress, "Overlay gerado", 0.85)


def merge_pdfs(pdf_base: str, pdf_overlay: str, pdf_saida: str, on_progress=None):
    report(on_progress, "Mesclando PDFs", 0.9)

    original = PdfReader(pdf_base)
    overlay = PdfReader(pdf_overlay)

    writer = PdfWriter()

    for i, page in enumerate(original.pages):
        if i == 0 and overlay.pages:
            page.merge_page(overlay.pages[0])
        writer.add_page(page)

    with open(pdf_saida, "wb") as f:
        writer.write(f)

    report(on_progress, "PDF finalizado", 1.0)


def main(on_progress=None):
    report(on_progress, "Lendo configurações", 0.05)

    config = ler_config()
    csv_path = config.get("arquivos", {}).get("csv_horas", CSV_HORAS)

    report(on_progress, "Lendo CSV de horas", 0.2)

    gerar_overlay(csv_path, PDF_OVERLAY, config, on_progress)
    merge_pdfs(PDF_ENTRADA, PDF_OVERLAY, PDF_SAIDA, on_progress)
