import time
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.interaction import KEY

class Appiumclick:

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()

    @keyword('ClickC')
    def clickC(self, locator, xoffset, yoffset):
        driver = self._driver
        appium_lib = self._builtin.get_library_instance('AppiumLibrary')

        self._builtin.log("Verificando se o driver está ativo", level='INFO')
        if not driver:
            raise RuntimeError("Driver não está inicializado ou conectado ao dispositivo.")

        self._builtin.log(f"Procurando elemento com locator: {locator}", level='INFO')
        try:
            element = appium_lib.get_webelement(locator)
        except Exception as e:
            raise ValueError(f"Elemento com locator '{locator}' não encontrado: {e}")

        location = element.location
        size = element.size
        self._builtin.log(f"Localização do elemento: {location}, Tamanho: {size}", level='INFO')

        try:
            xoffset = float(xoffset)
            yoffset = float(yoffset)
        except Exception:
            raise ValueError("xoffset e yoffset devem ser números (pixels ou fração de 0 a 1 para porcentagem)")

        # Se o offset for <= 1, considera como porcentagem do tamanho do elemento
        if 0 <= xoffset <= 1:
            xoffset_px = int(size['width'] * xoffset)
        else:
            xoffset_px = int(xoffset)
        if 0 <= yoffset <= 1:
            yoffset_px = int(size['height'] * yoffset)
        else:
            yoffset_px = int(yoffset)

        x = location['x'] + xoffset_px
        y = location['y'] + yoffset_px
        self._builtin.log(f"Coordenadas calculadas para clique: ({x}, {y}) (offsets: {xoffset_px}, {yoffset_px})", level='INFO')

        window_size = driver.get_window_size()
        self._builtin.log(f"Tamanho da tela: {window_size}", level='INFO')

        if not (0 <= x <= window_size['width'] and 0 <= y <= window_size['height']):
            raise ValueError(f"Coordenadas ({x}, {y}) estão fora da tela do dispositivo.")

        try:
            self._builtin.log("Executando clique usando W3C Actions", level='INFO')
            # Definindo 'touch' corretamente com a string "touch"
            touch = PointerInput("touch", "finger")
            actions = ActionBuilder(driver, mouse=touch)

            # Ação de movimento para as coordenadas calculadas
            actions.pointer_action.move_to_location(x, y)

            # Realizando o pointer_down (pressionando o dedo na tela)
            actions.pointer_action.pointer_down()

            # Aguarde um momento para simular o toque de forma mais visível
            time.sleep(0.2)

            # Realizando o pointer_up (levantando o dedo da tela)
            actions.pointer_action.pointer_up()

            actions.perform()

            self._builtin.log("Clique realizado com sucesso via W3C Actions", level='INFO')
        except Exception as e:
            self._builtin.log(f"Erro ao executar W3C Actions: {e}", level='ERROR')
            raise
