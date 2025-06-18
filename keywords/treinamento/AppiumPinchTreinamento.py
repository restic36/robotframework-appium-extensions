# Importa decorador do Robot Framework para registrar uma keyword personalizada
from robot.api.deco import keyword

# Importa biblioteca que permite acessar outras bibliotecas do Robot Framework, como AppiumLibrary
from robot.libraries.BuiltIn import BuiltIn

# Importa a ferramenta de criação de ações complexas com múltiplos toques (multi-touch)
from selenium.webdriver.common.action_chains import ActionChains

# Importa a biblioteca random para gerar pequenas variações (perturbações) nos movimentos dos dedos
import random

# Classe que implementa um gesto de pinch (zoom out) com dois dedos se aproximando
class AppiumPinchTreinamento:
    """Classe para executar gestos de zoom out (pinch) com Appium, com perturbação no movimento."""

    # Define o escopo da biblioteca como global (visível durante toda a execução)
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        # Inicializa o acesso ao BuiltIn do Robot Framework
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        # Obtém a instância atual do driver da AppiumLibrary
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    # Define uma keyword do Robot Framework chamada "Perform Pinch_4"
    @keyword("Perform Pinch")
    def perform_zoom_out_gesture(self, locator, scale=0.5, duration=500, direction="vertical", pause_s=0.1, steps=50):
        """
        Executa um gesto de zoom out (pinch) com perturbação para simular movimento realista.

        Args:
            locator (str): Localizador do elemento alvo do gesto.
            scale (float): Fator de escala (menor que 1 para zoom out).
            duration (int): Duração total da animação (em ms).
            direction (str): Direção do gesto ("vertical" ou "horizontal").
            pause_s (float): Tempo de pausa antes do movimento começar.
            steps (int): Número de passos interpolados para suavidade e precisão.
        """
        # Validações dos argumentos fornecidos
        if not isinstance(locator, str) or not locator:
            raise ValueError("The 'locator' argument must be a non-empty string.")
        if scale >= 1.0:
            raise ValueError("The 'scale' argument must be less than 1.0 for Zoom Out.")
        if duration <= 0:
            raise ValueError("The 'duration' must be a positive integer.")
        if direction.lower() not in ["vertical", "horizontal"]:
            raise ValueError("Direction must be 'vertical' or 'horizontal'.")

        try:
            # Obtém o driver da AppiumLibrary
            driver = self._driver
            if not driver:
                raise RuntimeError("The Appium driver is not available.")

            # Obtém o tamanho da tela do dispositivo
            screen_size = driver.get_window_size()
            screen_width = screen_size['width']
            screen_height = screen_size['height']

            # Encontra o elemento onde o gesto será aplicado
            appium_lib = self._builtin.get_library_instance("AppiumLibrary")
            element = appium_lib._element_find(locator, True, True)
            if not element:
                raise RuntimeError(f"Element not found for locator: {locator}")

            # Obtém a localização e o tamanho do elemento
            location = element.location
            x, y = location['x'], location['y']
            width, height = element.size['width'], element.size['height']
            center_x, center_y = x + width / 2, y + height / 2  # Ponto central do elemento

            # Define um pequeno deslocamento inicial
            offset = 10

            # Calcula o quanto os dedos devem se mover, proporcionalmente ao scale
            movement = center_y * (1 - scale) if direction == "vertical" else center_x * (1 - scale)

            # Define as posições iniciais e finais para os dois dedos
            if direction == "vertical":
                f1_start = (center_x, center_y - movement)
                f1_end = (center_x, center_y - offset)
                f2_start = (center_x, center_y + movement)
                f2_end = (center_x, center_y + offset)
            else:
                f1_start = (center_x - movement, center_y)
                f1_end = (center_x - offset, center_y)
                f2_start = (center_x + movement, center_y)
                f2_end = (center_x + offset, center_y)

            # Função auxiliar para garantir que os valores estejam dentro da tela
            def adjust(x, y):
                return max(0, min(x, screen_width)), max(0, min(y, screen_height))

            # Ajusta todas as posições para garantir que não saem da tela
            f1_start = adjust(*f1_start)
            f1_end = adjust(*f1_end)
            f2_start = adjust(*f2_start)
            f2_end = adjust(*f2_end)

            # Cria uma cadeia de ações com múltiplos dedos
            actions = ActionChains(driver)
            finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
            finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')

            # Move os dois dedos para as posições de início
            finger1.create_pointer_move(x=f1_start[0], y=f1_start[1])
            finger2.create_pointer_move(x=f2_start[0], y=f2_start[1])

            # Toca com os dois dedos na tela
            finger1.create_pointer_down(button=0)
            finger2.create_pointer_down(button=0)

            # Aguarda o tempo definido antes de iniciar o movimento
            finger1.create_pause(pause_s)
            finger2.create_pause(pause_s)

            # Executa o movimento dividido em "steps" (com pequenas variações para simular naturalidade)
            for i in range(1, steps + 1):
                t = i / steps  # Porcentagem do caminho
                # Aplica interpolações nos pontos, com randomização leve (perturbação)
                interp_f1_x = f1_start[0] + t * (f1_end[0] - f1_start[0]) + random.uniform(-0, 0)
                interp_f1_y = f1_start[1] + t * (f1_end[1] - f1_start[1]) + random.uniform(-0, 0)
                interp_f2_x = f2_start[0] + t * (f2_end[0] - f2_start[0]) + random.uniform(-0, 0)
                interp_f2_y = f2_start[1] + t * (f2_end[1] - f2_start[1]) + random.uniform(-0, 0)

                # Garante que os novos pontos ainda estejam dentro da tela
                interp_f1_x, interp_f1_y = adjust(interp_f1_x, interp_f1_y)
                interp_f2_x, interp_f2_y = adjust(interp_f2_x, interp_f2_y)

                # Calcula a duração de cada micro movimento
                move_duration = int(duration / steps)

                # Cria o movimento do frame atual
                finger1.create_pointer_move(x=interp_f1_x, y=interp_f1_y, duration=move_duration)
                finger2.create_pointer_move(x=interp_f2_x, y=interp_f2_y, duration=move_duration)

            # Ao final, os dedos são levantados (touch up)
            finger1.create_pointer_up(button=0)
            finger2.create_pointer_up(button=0)

            # Executa todas as ações acumuladas
            actions.perform()

        # Em caso de erro, exibe uma mensagem mais amigável
        except Exception as e:
            raise RuntimeError(f"Error while performing the zoom out gesture: {str(e)}")
