*** Settings ***

Library    SeleniumLibrary
Library    BuiltIn
Library    OperatingSystem

*** Keywords ***

Abrir Navegador E Logar
    [Arguments]    ${CONFIG}    ${DEBUG}

    Log To Console    STEP: Logando na intranet
    
    ${BROWSER}=    Set Variable    ${CONFIG["browser"]}
    
    # Configurações Específicas para Chrome
    IF    '${BROWSER}' == 'chrome'
        ${options}=    Evaluate
        ...    sys.modules['selenium.webdriver'].ChromeOptions()    sys

        IF    not ${DEBUG}
            Call Method    ${options}    add_argument    --headless=new
            Call Method    ${options}    add_argument    --disable-gpu
            Call Method    ${options}    add_argument    --disable-extensions
            Call Method    ${options}    add_argument    --disable-notifications
            Call Method    ${options}    add_argument    --disable-infobars
            Call Method    ${options}    add_argument    --disable-dev-shm-usage
        END

        Call Method    ${options}    add_argument    --window-size=1920,1080

    # Configurações Específicas para Firefox
    ELSE IF    '${BROWSER}' == 'firefox'
        ${options}=    Evaluate
        ...    sys.modules['selenium.webdriver'].FirefoxOptions()    sys

        IF    not ${DEBUG}
            Call Method    ${options}    add_argument    -headless
            Call Method    ${options}    set_preference    dom.webnotifications.enabled    False
            Call Method    ${options}    set_preference    media.autoplay.default    5
        END
        
        Set Environment Variable    GECKODRIVER_LOG    fatal
        Set Environment Variable    MOZ_LOG            fatal
        
    ELSE
        Fail    Navegador inválido: ${CONFIG["browser"]}
    END
    
    Open Browser
    ...    ${CONFIG["url"]}
    ...    ${BROWSER}
    ...    options=${options}
    ...    service_log_path=${NONE}
    
    Input Text      id=username    ${CONFIG["usuario"]}
    Input Password  id=password    ${CONFIG["senha"]}
    Click Button    id=kc-login

    Log To Console    STEP: Login concluído