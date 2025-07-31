*** Settings ***
Library    AppiumLibrary
Resource   ./base.resource

*** Test Cases ***
Detectar Mudança Visual

      Start session Google Maps
      sleep    5s

    Capturar Screenshot Inicial Como    tela_antes.png

    Perform Pinch Gesture     id=com.google.android.apps.maps:id/mainmap_container
    Sleep    5
    

    # Compara o screenshot final com o inicial, usando tolerância de 0.02
    Comparar Screenshot Final Com    tela_antes.png    0.02
