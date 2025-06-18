# Importa o decorador para criar uma keyword no Robot Framework
from robot.api.deco import keyword

# Permite acessar keywords internas do Robot Framework, como AppiumLibrary
from robot.libraries.BuiltIn import BuiltIn

# Importa ActionChains para criar gestos complexos com múltiplos toques
from selenium.webdriver.common.action_chains import ActionChains

# Importa biblioteca padrão do Python para gerar pequenas variações no movimento (perturbação)
import random

# Define a classe responsável por implementar o gesto de zoom in (aproximação)
class AppiumZoomTreinamento:
    """Classe para executar gestos de zoom in com Appium, com perturbação no movimento."""

    # Define o escopo da biblioteca como global (compartilhada entre testes)
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        # Inicializa o acesso ao BuiltIn, que permite usar recursos do Robot Framework
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        # Retorna a instância atual do Appium driver (WebDriver)
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    # Define uma keyword customizada chamada "Perform Zoom_4"
    @keyword("Perform Zoom")
    def perform_zoom_in_gesture(self, locator, scale=1.5, duration=500, direction="vertical", pause_s=0.1, steps=50):
        """
        Executa um gesto de zoom in (aproximação com dois dedos) em um aplicativo Android.
        Aplica perturbações para simular movimento humano realista.

        Parâmetros:
            locator: localizador do elemento onde o gesto será aplicado.
            scale: fator de escala do gesto (>1.0 para zoom in).
            duration: tempo total da animação em milissegundos.
            direction: direção do gesto ("vertical" ou "horizontal").
            pause_s: tempo de espera antes de iniciar o movimento.
            steps: quantidade de passos interpolados (controla suavidade).
        """
        # Validações dos parâmetros recebidos
        if not isinstance(locator, str) or not locator:
            raise ValueError("The 'locator' argument must be a non-empty string.")
        if scale <= 1.0:
            raise ValueError("The 'scale' argument must be greater than 1.0 for Zoom In.")
        if duration <= 0:
            raise ValueError("The 'duration' must be a positive integer.")
        if direction.lower() not in ["vertical", "horizontal"]:
            raise ValueError("Direction must be 'vertical' or 'horizontal'.")

        try:
            # Obtém o driver Appium ativo
            driver = self._driver
            if not driver:
                raise RuntimeError("The Appium driver is not available.")

            # Pega o tamanho da tela do dispositivo
            screen_size = driver.get_window_size()
            screen_width = screen_size['width']
            screen_height = screen_size['height']

            # Localiza o elemento onde o gesto será aplicado
            appium_lib = self._builtin.get_library_instance("AppiumLibrary")
            element = appium_lib._element_find(locator, True, True)
            if not element:
                raise RuntimeError(f"Element not found for locator: {locator}")

            # Captura posição e tamanho do elemento
            location = element.location
            x, y = location['x'], location['y']
            width, height = element.size['width'], element.size['height']
            center_x, center_y = x + width / 2, y + height / 2  # Calcula o centro do elemento

            # Define um deslocamento mínimo inicial (pixels)
            offset = 10

            # Calcula o quanto os dedos devem se mover com base no scale
            movement = center_y * (scale - 1) if direction == "vertical" else center_x * (scale - 1)

            # Define os pontos iniciais e finais dos dedos, dependendo da direção
            if direction == "vertical":
                f1_start = (center_x, center_y - offset)
                f1_end = (center_x, center_y - movement)
                f2_start = (center_x, center_y + offset)
                f2_end = (center_x, center_y + movement)
            else:
                f1_start = (center_x - offset, center_y)
                f1_end = (center_x - movement, center_y)
                f2_start = (center_x + offset, center_y)
                f2_end = (center_x + movement, center_y)

            # Função para garantir que os valores estão dentro dos limites da tela
            def adjust(x, y):
                return max(0, min(x, screen_width)), max(0, min(y, screen_height))

            # Aplica o ajuste aos pontos calculados
            f1_start = adjust(*f1_start)
            f1_end = adjust(*f1_end)
            f2_start = adjust(*f2_start)
            f2_end = adjust(*f2_end)

            # Cria uma instância do ActionChains (cadeia de ações com múltiplos dedos)
            actions = ActionChains(driver)

            # Adiciona dois inputs de toque (simulando dois dedos)
            finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
            finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')

            # Move os dedos para os pontos iniciais
            finger1.create_pointer_move(x=f1_start[0], y=f1_start[1])
            finger2.create_pointer_move(x=f2_start[0], y=f2_start[1])

            # Pressiona os dois dedos na tela
            finger1.create_pointer_down(button=0)
            finger2.create_pointer_down(button=0)

            # Aguarda um curto tempo antes de iniciar o gesto
            finger1.create_pause(pause_s)
            finger2.create_pause(pause_s)

            # Inicia o movimento interpolado (em steps) com leve aleatoriedade
            for i in range(1, steps + 1):
                t = i / steps  # Fração do caminho percorrido até o ponto final
                # Adiciona pequenas variações com random para simular dedo humano
                interp_f1_x = f1_start[0] + t * (f1_end[0] - f1_start[0]) + random.uniform(-0, 0)
                interp_f1_y = f1_start[1] + t * (f1_end[1] - f1_start[1]) + random.uniform(-0, 0)
                interp_f2_x = f2_start[0] + t * (f2_end[0] - f2_start[0]) + random.uniform(-0, 0)
                interp_f2_y = f2_start[1] + t * (f2_end[1] - f2_start[1]) + random.uniform(-0, 0)

                # Garante que os pontos interpolados ainda estão dentro da tela
                interp_f1_x, interp_f1_y = adjust(interp_f1_x, interp_f1_y)
                interp_f2_x, interp_f2_y = adjust(interp_f2_x, interp_f2_y)

                # Duração do movimento de cada passo
                move_duration = int(duration / steps)

                # Executa o movimento do passo atual
                finger1.create_pointer_move(x=interp_f1_x, y=interp_f1_y, duration=move_duration)
                finger2.create_pointer_move(x=interp_f2_x, y=interp_f2_y, duration=move_duration)

            # Ao final, os dedos são levantados (touch up)
            finger1.create_pointer_up(button=0)
            finger2.create_pointer_up(button=0)

            # Executa toda a sequência criada
            actions.perform()

        except Exception as e:
            # Em caso de erro, lança uma exceção com mensagem útil
            raise RuntimeError(f"Error while performing the zoom in gesture: {str(e)}")
