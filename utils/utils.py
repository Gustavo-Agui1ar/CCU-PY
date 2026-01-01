import os
import sys
import tempfile
from pdf2image import convert_from_path
from PIL import Image
from typing import List


def juntar_imagens_em_uma(
    imagens: List[str],
    output_path: str,
    direcao: str = "vertical"
) -> str:
    """
    Junta múltiplas imagens em uma única imagem.

    :param imagens: lista de caminhos das imagens
    :param output_path: caminho da imagem final (png/jpg)
    :param direcao: "vertical" ou "horizontal"
    :return: caminho da imagem gerada
    """
    imgs = [Image.open(img).convert("RGB") for img in imagens]

    if direcao == "vertical":
        largura = max(img.width for img in imgs)
        altura = sum(img.height for img in imgs)

        imagem_final = Image.new("RGB", (largura, altura), "white")

        y_offset = 0
        for img in imgs:
            imagem_final.paste(img, (0, y_offset))
            y_offset += img.height

    elif direcao == "horizontal":
        largura = sum(img.width for img in imgs)
        altura = max(img.height for img in imgs)

        imagem_final = Image.new("RGB", (largura, altura), "white")

        x_offset = 0
        for img in imgs:
            imagem_final.paste(img, (x_offset, 0))
            x_offset += img.width
    else:
        raise ValueError("direcao deve ser 'vertical' ou 'horizontal'")

    imagem_final.save(output_path)
    return output_path


def pdf_para_imagens(pdf_path: str) -> tuple[list[str], str]:
    """
    Converte um PDF em imagens PNG temporárias.
    Retorna (lista_de_caminhos, pasta_temporaria)
    """
    temp_dir = tempfile.mkdtemp(prefix="pdf_preview_")

    imagens = convert_from_path(
        pdf_path,
        dpi=150,
        fmt="png",
        output_folder=temp_dir,
        paths_only=True
    )

    return imagens, temp_dir

def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python script.py <caminho_pdf_ou_imagem> [saida.png]")
        sys.exit(1)

    entrada = sys.argv[1]
    saida = sys.argv[2] if len(sys.argv) > 2 else "imagem_final.png"

    # Caso seja PDF
    if entrada.lower().endswith(".pdf"):
        imagens, temp_dir = pdf_para_imagens(entrada)
        print(f"PDF convertido em {len(imagens)} imagens temporárias em {temp_dir}")

        juntar_imagens_em_uma(
            imagens,
            saida,
            direcao="vertical"
        )

    # Caso seja imagem única ou pasta
    else:
        if os.path.isdir(entrada):
            imagens = sorted(
                os.path.join(entrada, f)
                for f in os.listdir(entrada)
                if f.lower().endswith((".png", ".jpg", ".jpeg"))
            )
        else:
            imagens = [entrada]

        if not imagens:
            raise ValueError("Nenhuma imagem encontrada")

        juntar_imagens_em_uma(
            imagens,
            saida,
            direcao="vertical"
        )

    print(f"Imagem final gerada em: {saida}")


if __name__ == "__main__":
    main()

