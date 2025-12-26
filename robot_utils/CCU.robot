* Settings *
Library    SeleniumLibrary
Library    OperatingSystem
Library    Collections
Library    Dialogs

*** Variables ***

${CONFIG}    None
${DEBUG}    False

*** Keywords ***
Carregar Configuracoes
    ${json_text}=    Get File    ${CURDIR}/../configs/config.json
    ${CONFIG}=    Evaluate    json.loads($json_text)    json
    Set Suite Variable    ${CONFIG}

# Esperar Input Do Usuario
#     ${mes_ano}=    Get Value From User    Digite o mês e ano no formato MM/YYYY para coletar as horas:
#     RETURN    ${mes_ano}

Esperar Input Do Usuario
    RETURN    12/2025

Buscar Painel Com Mes e Ano
    [Arguments]    ${mes_ano}

    Log To Console    STEP: Buscando mês
    
    ${painel_texto}=    Get Text
    ...    xpath=//strong[@id="ccuAnoMesAtual"]

    WHILE    '${painel_texto}' != '${mes_ano}'
        Click Element
        ...    xpath=//button[@id="mesAnterior"]

        Esperar Tela De Dias

        ${painel_texto}=    Get Text
        ...    xpath=//strong[@id="ccuAnoMesAtual"]
    END

Abrir Navegador E Logar
    Log To Console    STEP: Logando na intranet
    IF    '${CONFIG["browser"]}' == 'chrome'
        ${options}=    Evaluate
        ...    sys.modules['selenium.webdriver'].ChromeOptions()    sys

        IF    not ${DEBUG}
            Call Method    ${options}    add_argument    --headless=new
            Call Method    ${options}    add_argument    --disable-gpu
        END

        Call Method    ${options}    add_argument    --window-size=1920,1080

    ELSE IF    '${CONFIG["browser"]}' == 'firefox'
        ${options}=    Evaluate
        ...    sys.modules['selenium.webdriver'].FirefoxOptions()    sys

        IF    not ${DEBUG}
            Call Method    ${options}    add_argument    -headless
        END
    ELSE
        Fail    Navegador inválido: ${CONFIG["browser"]}
    END

    Open Browser
    ...    ${CONFIG["url"]}
    ...    ${CONFIG["browser"]}
    ...    options=${options}

    Run Keyword If    ${DEBUG}    Maximize Browser Window

    Input Text      id=username    ${CONFIG["usuario"]}
    Input Password  id=password    ${CONFIG["senha"]}
    Click Button    id=kc-login
    
    Log To Console    STEP: Login concluído

Salvar Dicionario Em CSV
    [Arguments]    &{HORAS_POR_DIA}

    Log To Console    STEP: Gerando CSV

    ${arquivo}=    Set Variable    ${CONFIG["arquivos"]["csv_horas"]}
    ${conteudo}=    Set Variable    dia,data_inicial,data_final\n

    FOR    ${dia}    IN    @{HORAS_POR_DIA.keys()}
        ${dados}=    Get From Dictionary    ${HORAS_POR_DIA}    ${dia}
        ${inicio}=   Get From Dictionary    ${dados}    hora_inicio
        ${fim}=      Get From Dictionary    ${dados}    hora_fim
        ${linha}=    Set Variable    ${dia},${inicio},${fim}\n
        ${conteudo}=    Catenate    SEPARATOR=    ${conteudo}    ${linha}
    END

    Create File    ${arquivo}    ${conteudo}


Esperar Tela De Dias
    Wait Until Page Contains Element
    ...    xpath=//table[@id="ccuDias"]
    ...    ${CONFIG["timeouts"]["visibilidade"]}

    Wait Until Element Is Not Visible
    ...    xpath=//div[contains(@class,"ccuBloqueio")]
    ...    ${CONFIG["timeouts"]["bloqueio"]}


Coletar Horas Por Dia
    
    Log To Console    STEP: Extraindo dados

    &{HORAS_POR_DIA}=    Create Dictionary

    ${total_dias}=    Get Element Count
    ...    xpath=//table[@id="ccuDias"]//span[contains(@class, "ccuDia")]

    FOR    ${i}    IN RANGE    ${total_dias}
        ${dia_texto}    ${dados_dia}=    Processar Dia Por Indice    ${i}
        Set To Dictionary    ${HORAS_POR_DIA}    ${dia_texto}=${dados_dia}
    END

    RETURN    ${HORAS_POR_DIA}


Processar Dia Por Indice
    [Arguments]    ${indice}

    Wait Until Element Is Not Visible
    ...    xpath=//div[contains(@class,"ccuBloqueio")]
    ...    20s

    ${dia}=    Get WebElement
    ...    xpath=(//table[@id="ccuDias"]//span[contains(@class, "ccuDia")])[${indice + 1}]

    ${dia_texto}=    Get Text    ${dia}

    Scroll Element Into View    ${dia}
    Wait Until Element Is Visible    ${dia}    10s
    Wait Until Element Is Enabled    ${dia}    10s
    Click Element    ${dia}

    Wait Until Element Is Not Visible
    ...    xpath=//div[contains(@class,"ccuBloqueio")]
    ...    20s

    ${dados_dia}=    Coletar Horas Do Dia

    RETURN    ${dia_texto}    ${dados_dia}


Coletar Horas Do Dia
    ${horas}=    Get WebElements
    ...    xpath=//div[@id="ccuLancamentosCorpo"]//input[contains(@class,"hora")]

    @{horas_validas}=    Create List

    FOR    ${h}    IN    @{horas}
        ${valor}=    Get Element Attribute    ${h}    value
        IF    '${valor}' != ''
            Append To List    ${horas_validas}    ${valor}
        END
    END

    ${qtd_horas}=    Get Length    ${horas_validas}

    ${hora_inicio}=    Set Variable If
    ...    ${qtd_horas} > 0
    ...    ${horas_validas}[0]
    ...    ${EMPTY}

    ${hora_fim}=    Set Variable If
    ...    ${qtd_horas} > 1
    ...    ${horas_validas}[-1]
    ...    ${EMPTY}

    &{dados_dia}=    Create Dictionary
    ...    hora_inicio=${hora_inicio}
    ...    hora_fim=${hora_fim}

    RETURN    ${dados_dia}

*** Test Cases ***
Teste Extrair Horas CCU

    Carregar Configuracoes

    ${mes_ano}=    Esperar Input Do Usuario
    
    Abrir Navegador E Logar
    
    Esperar Tela De Dias

    Buscar Painel Com Mes e Ano    ${mes_ano}
    
    &{HORAS_POR_DIA}=    Coletar Horas Por Dia
    Salvar Dicionario Em CSV    &{HORAS_POR_DIA}

    Log To Console    STEP: CSV criado com sucesso

    Close Browser
