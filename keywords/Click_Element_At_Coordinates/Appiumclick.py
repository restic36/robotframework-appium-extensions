import time
# Importa a biblioteca 'time' para usar sleep (pausa entre ações)

from robot.api.deco import keyword
# Importa o decorator @keyword para transformar o método Python em uma keyword reconhecida pelo Robot Framework

from robot.libraries.BuiltIn import BuiltIn
# Permite acesso às funcionalidades internas do Robot Framework, como log e chamadas de outras bibliotecas

from selenium.webdriver.common.actions.action_builder import ActionBuilder
# Usado para construir ações de toque com a API W3C Actions (como clique, arraste, etc.)

from selenium.webdriver.common.actions.pointer_input import PointerInput
# Representa uma entrada de ponteiro (como o dedo em uma tela touch)

class Appiumclick:
    # Define uma classe que conterá keywords personalizadas para interação com Appium

    def __init__(self):
        self._builtin = BuiltIn()
        # Armazena uma instância da biblioteca interna do Robot Framework para facilitar chamadas como log, etc.

    @property
    def _driver(self):
        # Retorna o driver atual da AppiumLibrary (ou seja, o controle da aplicação em teste)
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()

    @keyword('ClickC')
    def clickC(self, locator, xoffset=0.5, yoffset=0.5):
        """
        Keyword que realiza um clique customizado em um elemento com base em um offset.
        - locator: identificador do elemento (ex: xpath, id)
        - xoffset: deslocamento horizontal (0 a 1 = porcentagem do tamanho, >1 = pixels)
        - yoffset: deslocamento vertical (idem acima)
        """

        driver = self._driver
        appium_lib = self._builtin.get_library_instance('AppiumLibrary')
        # Pega instância da AppiumLibrary e do driver ativo

        self._builtin.log("Verificando se o driver está ativo", level='INFO')
        if not driver:
            raise RuntimeError("Driver não está inicializado ou conectado ao dispositivo.")
        # Verifica se o driver está disponível antes de prosseguir

        self._builtin.log(f"Procurando elemento com locator: {locator}", level='INFO')
        try:
            element = appium_lib.get_webelement(locator)
        except Exception as e:
            raise ValueError(f"Elemento com locator '{locator}' não encontrado: {e}")
        # Tenta localizar o elemento na tela. Se falhar, lança um erro descritivo.

        location = element.location  # Obtém a posição (x, y) do elemento na tela
        size = element.size          # Obtém o tamanho (largura e altura) do elemento
        self._builtin.log(f"Localização do elemento: {location}, Tamanho: {size}", level='INFO')

        try:
            xoffset = float(xoffset)
            yoffset = float(yoffset)
        except Exception:
            raise ValueError("xoffset e yoffset devem ser números (ex: 0.5 para porcentagem ou 30 para pixels)")
        # Converte os offsets para float e trata erro se não forem numéricos

        # Se os valores estiverem entre 0 e 1, considera como porcentagem do tamanho do elemento
        if 0 <= xoffset <= 1:
            xoffset_px = int(size['width'] * xoffset)
        else:
            xoffset_px = int(xoffset)

        if 0 <= yoffset <= 1:
            yoffset_px = int(size['height'] * yoffset)
        else:
            yoffset_px = int(yoffset)

        # Soma os deslocamentos à posição do elemento para obter a posição final do clique
        x = location['x'] + xoffset_px
        y = location['y'] + yoffset_px
        self._builtin.log(f"Coordenadas calculadas para clique: ({x}, {y}) (offsets: {xoffset_px}, {yoffset_px})", level='INFO')

        window_size = driver.get_window_size()
        # Pega o tamanho da tela do dispositivo para validar se o clique está dentro da área visível
        self._builtin.log(f"Tamanho da tela: {window_size}", level='INFO')

        if not (0 <= x <= window_size['width'] and 0 <= y <= window_size['height']):
            raise ValueError(f"Coordenadas ({x}, {y}) estão fora da tela do dispositivo.")
        # Garante que o ponto calculado está dentro da tela

        try:
            self._builtin.log("Executando clique usando W3C Actions", level='INFO')
            # Inicia construção da ação de toque usando W3C Actions

            touch = PointerInput("touch", "finger")
            # Cria um ponteiro do tipo 'touch' representando o dedo

            actions = ActionBuilder(driver, mouse=touch)
            # Cria uma instância do construtor de ações W3C com esse ponteiro

            actions.pointer_action.move_to_location(x, y)
            # Move o ponteiro para a posição calculada

            actions.pointer_action.pointer_down()
            # Simula o toque (dedo pressionado)

            time.sleep(0.2)
            # Pausa breve para simular um toque mais realista (poderia ser substituído por pause no futuro)

            actions.pointer_action.pointer_up()
            # Solta o dedo da tela (fim do toque)

            actions.perform()
            # Executa a sequência de ações criada

            self._builtin.log("Clique realizado com sucesso via W3C Actions", level='INFO')
        except Exception as e:
            self._builtin.log(f"Erro ao executar W3C Actions: {e}", level='ERROR')
            raise
