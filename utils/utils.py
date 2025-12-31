import os
import tempfile
import shutil
import base64
from pdf2image import convert_from_path


DEBUG_FOLDER = os.path.join("pdf_debug")

def pdf_para_imagens(pdf_path: str) -> tuple[list[str], str]:
    """
    Converte um PDF em imagens PNG, salva cópias na pasta de debug,
    e retorna o conteúdo das imagens codificado em Base64 para visualização direta no Flet.
    
    Retorna (lista_de_strings_base64, pasta_temporaria_removida)
    """
    temp_dir = tempfile.mkdtemp(prefix="pdf_preview_")
    base64_images = [] 

    try:
        imagens_temporarias = convert_from_path(
            pdf_path,
            dpi=150,
            fmt="png",
            output_folder=temp_dir,
            paths_only=True
        )
        
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise e 

    if not os.path.exists(DEBUG_FOLDER):
        os.makedirs(DEBUG_FOLDER)
    else:
        for filename in os.listdir(DEBUG_FOLDER):
            file_path = os.path.join(DEBUG_FOLDER, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Falha ao deletar {file_path} na pasta de debug. Razão: {e}')


    for i, original_path in enumerate(imagens_temporarias):
        debug_filename = f"page_{i+1:02d}.png"
        debug_path = os.path.join(DEBUG_FOLDER, debug_filename)
        shutil.copy2(original_path, debug_path)
        
        with open(original_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            base64_images.append(encoded_string)
            
    shutil.rmtree(temp_dir, ignore_errors=True)

    return base64_images, DEBUG_FOLDER