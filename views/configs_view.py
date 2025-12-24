import flet as ft
import json
import os

from styles.style import *

CONFIG_PATH = "configs/config.json"

def configuracoes_view(page: ft.Page) -> ft.Control:
    # -------- CAMPOS --------
    url = ft.TextField(label="URL", width=FIELD_WIDTH)
    usuario = ft.TextField(label="Usuário", width=FIELD_WIDTH)
    senha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        width=FIELD_WIDTH,
    )

    browser = ft.Dropdown(
        label="Browser",
        value="firefox",
        width=FIELD_WIDTH,
        options=[
            ft.dropdown.Option("firefox"),
            ft.dropdown.Option("chrome"),
            ft.dropdown.Option("edge"),
        ],
    )

    timeout_bloqueio = ft.TextField(label="Timeout Bloqueio", width=HALF_FIELD_WIDTH)
    timeout_visibilidade = ft.TextField(label="Timeout Visibilidade", width=HALF_FIELD_WIDTH)

    csv_horas = ft.TextField(label="CSV Horas", width=FIELD_WIDTH)

    status = ft.Text()

    # -------- FUNÇÕES --------
    def carregar_config():
        if not os.path.exists(CONFIG_PATH):
            return

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)

        url.value = config.get("url", "")
        usuario.value = config.get("usuario", "")
        senha.value = config.get("senha", "")
        browser.value = config.get("browser", "firefox")

        timeouts = config.get("timeouts", {})
        timeout_bloqueio.value = timeouts.get("bloqueio", "")
        timeout_visibilidade.value = timeouts.get("visibilidade", "")

        arquivos = config.get("arquivos", {})
        csv_horas.value = arquivos.get("csv_horas", "")

    def salvar_config(e):
        config = {
            "url": url.value,
            "usuario": usuario.value,
            "senha": senha.value,
            "browser": browser.value,
            "timeouts": {
                "bloqueio": timeout_bloqueio.value,
                "visibilidade": timeout_visibilidade.value,
            },
            "arquivos": {
                "csv_horas": csv_horas.value
            }
        }

        os.makedirs("configs", exist_ok=True)

        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        status.value = "Configurações salvas com sucesso"
        status.style = STATUS_SUCCESS
        page.update()

    # carregar dados ao abrir a view
    carregar_config()

    return ft.Container(
        padding=PAGE_PADDING,
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text("Configurações", style=TITLE_STYLE),
                url,
                usuario,
                senha,
                browser,
                ft.Text("Timeouts", weight=ft.FontWeight.BOLD),
                ft.Row(
                    spacing=20,
                    controls=[timeout_bloqueio, timeout_visibilidade],
                ),
                csv_horas,
                ft.ElevatedButton(
                    "Salvar",
                    width=BUTTON_WIDTH,
                    height=BUTTON_HEIGHT,
                    on_click=salvar_config,
                ),
                status,
            ],
        ),
    )
