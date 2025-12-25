import subprocess
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ROBOT_DIR = BASE_DIR
ROBOT_FILE = os.path.join(ROBOT_DIR, "CCU.robot")
OUTPUT_DIR = os.path.join(ROBOT_DIR, "results")

ROBOT_CMD = [
    sys.executable,
    "-m",
    "robot",
    "--outputdir",
    OUTPUT_DIR,
    ROBOT_FILE,
]


def report(cb, msg, value):
    if cb:
        cb(msg, value)


def executar_robot(on_progress=None):
    report(on_progress, "Preparando execução do robô", 0.05)

    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        report(on_progress, "Iniciando Robot Framework", 0.10)

        process = subprocess.Popen(
            ROBOT_CMD,
            cwd=ROBOT_DIR,
            stdin=sys.stdin, 
            stdout=subprocess.PIPE,   # Captura a saída
            stderr=subprocess.STDOUT, # IMPORTANTE: Joga os erros no mesmo fluxo da saída
            text=True,
            bufsize=1 # Buffer linha a linha
        )

        for line in process.stdout:
            line = line.strip()
            
        process.wait()

        if process.returncode != 0:
            raise RuntimeError(f"Robot falhou com código {process.returncode}")

        report(on_progress, "Coleta finalizada", 0.50)

    except Exception as e:
        report(on_progress, f"Erro ao executar robô: {e}", 0.0)
        raise

if __name__ == "__main__":
    executar_robot()