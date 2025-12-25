import os
import tempfile
from pdf2image import convert_from_path


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
