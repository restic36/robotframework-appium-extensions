*** Settings ***

Resource    base_treinamento.resource

*** Test Cases ***

Deve realizar um zoom no Google Maps
    [Tags]    zoom
    Start session Google Maps    #Keyword definida no base.resource
    
    Sleep    10

    Wait Until Element Is Visible    //android.widget.Button[@content-desc="Enter compass mode"]
    #Click Element    //android.widget.Button[@content-desc="Enter compass mode"]
    Sleep    2

    Perform Zoom     locator=id=com.google.android.apps.maps:id/mainmap_container   scale=1.5    duration=500    direction=horizontal
    ...        pause_s=0.3    steps=50

    Sleep    2

Deve realizar um pinch no Google Maps
    [Tags]    pinch
    Start session Google Maps    #Keyword definida no base.resource
    Sleep    10

    #Estratégia de verificação - Steps
    Wait Until Element Is Visible    //android.widget.Button[@content-desc="Enter compass mode"]
    #Click Element    //android.widget.Button[@content-desc="Enter compass mode"]

    Sleep    2    #Pausas para aguardar o carregamento

    Perform Pinch      locator=id=com.google.android.apps.maps:id/mainmap_container   scale=0.5    duration=500    direction=horizontal
    ...       pause_s=0.3    steps=50
    
    Sleep    2

Deve realizar um zoom na Camera
    [Tags]    zoomcamera
    Start session Camera    #Keyword definida no base.resource
    
    Sleep    10
    
    Click Element    id=com.android.camera2:id/confirm_button  #Necessario clicar em Next na splash page ao iniciar a camera
    Wait Until Element Is Visible    //android.widget.ImageView[@content-desc="Shutter"]  #Aguardar o botao do obturador aparecer na tela
    
    Sleep    2

    Perform Zoom     locator=com.android.camera2:id/mode_options_overlay   scale=1.5    duration=500    direction=horizontal
    ...        pause_s=0.3    steps=50

    Sleep    2