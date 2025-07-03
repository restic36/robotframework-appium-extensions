# -> principais sugestões:
# pra seguir o estilo estrutural da biblioteca oficial da Appium, trocar a classe pra GestureKeyword
# criar subfunções auxiliares pra facilitar possíveis futuras manutenções
# incluir o parâmetro 'movement'à keyword pra deixar a amplitude do gesto ajustável
# incluir logging mais detalhado pra facilitar o entendimento de possíveis erros e auditorias
# incluir uma validação do formato do locator strategy=value pra tentar reduzir erros silenciosos durante testes
# incluir fallback automático para centro da tela em caso de locator None
# fazer o ajuste ao tamanho da tela como uma função reutilizável e com warnings.warn
# detalhar mais o tratamento de exceções, com mais mensagens informativas e logs intermediários
# incluir o ROBOT_LIBRARY_SCOPE = 'GLOBAL' pra tornar a keyword acessível globalmente no escopo Robot

from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
import warnings
import random


class GestureKeywords:  # -> vamo instanciar a classe GestureKeywords
    """Custom Gesture Extension Class for AppiumLibrary with enhanced pinch gesture."""
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    @property  # -> transforma um método em uma "propriedade" da classe
    def driver(self):
        # vai pegar a instância atual da AppiumLibrary e retornar o driver ativo do Appium
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    def _get_element_center(self, locator):
        # -> pra identificar o elemento e calcular seu ponto central
        appium_lib = self._builtin.get_library_instance("AppiumLibrary")
        element = appium_lib._element_find(locator, True, True)
        if not element:  # -> se o locator for passado, mas o elemento não for encontrado, ele gera um erro
            raise RuntimeError(f"Element not found for locator: {locator}")
        location = element.location  # -> retorna o canto superior esquerdo do elemento
        size = element.size  # -> retorna o tamanho (width, height)
        # -> com isso ele calcula o centro do elemento
        x, y = location['x'], location['y']
        width, height = size['width'], size['height']
        return x + width / 2, y + height / 2, element

    def _calculate_finger_inicial_positions(self, x, y, scale, movement, direction):
        # -> pra definir as posições de início de cada dedo com base no centro e no deslocamento
        # -> a gente precisa incluir uma distância ao centro do elemento, pra que os dedos
        # comecem afastados e tenham "gás" pra se aproximarem ao realizar o movimento de pinch
        # -> pra determinar o quão longe os dedos vão começar do centro
        displacement = scale * movement
        if direction.lower() == "vertical":  # -> se o gesto for vertical
            # -> se afastam no eixo y
            return (x, y - displacement), (x, y + displacement)
        else:  # -> se o gesto for na horizontal
            # -> se afastam no eixo x
            return (x - displacement, y), (x + displacement, y)

    def _adjust_to_screen_bounds(self, positions, screen_width, screen_height):
        # -> ele vai receber as coordenadas x e y e os limites da tela
        # -> e ajustar essas coordenadas pros limites da tela
        adjusted_positions = []
        for x, y in positions:
            new_x = max(0, min(x, screen_width))
            new_y = max(0, min(y, screen_height))
            if (x, y) != (new_x, new_y):
                warnings.warn(
                    f"Finger position ({x}, {y}) adjusted to ({new_x}, {new_y}) to fit within screen bounds.")
                # -> caso o ponto original esteja fora da tela, aqi ele vai emitir um aviso
            # -> e vai ajustar, caso seja necessário
            adjusted_positions.append((new_x, new_y))
        return adjusted_positions

    def _validate_pinch_args(self, locator, scale, duration, direction, movement):
        # -> ele vai validar os argumentos pra assegurar que eles são válidos e seguros
        if locator is not None:
            if not isinstance(locator, str) or not locator:
                raise ValueError("The 'locator' must be a non-empty string.")
            if '=' not in locator:
                raise ValueError(
                    f"Locator '{locator}' must be in the format 'strategy=value'")
        if not (0.1 <= scale < 1.0):
            raise ValueError("Scale must be between 0.1 and less than 1.0")
        if duration <= 0:
            raise ValueError("Duration must be a positive integer.")
        if direction.lower() not in ["vertical", "horizontal"]:
            raise ValueError("Direction must be 'vertical' or 'horizontal'.")
        if movement <= 0:
            raise ValueError("Movement must be positive")

    # -> transforma a função em uma keyword utilizável no Robot
    @keyword("Perform Pinch Gesture")
    def perform_pinch_gesture(self, locator=None, scale=0.5, duration=500, direction="vertical", movement=200, pause=0.1, steps=50):
        """
        Performs a realistic pinch gesture with perturbation.

        Args:
            locator (str): Element locator (optional; if None, uses screen center).
            scale (float): Gesture scale (0.1 to 1.0).
            duration (int): Total duration of the gesture in milliseconds.
            direction (str): Gesture direction ("vertical" or "horizontal").
            movement (int/float): Gesture amplitude in pixels.
            pause (int/float): Pause in seconds before movement begins.
            steps (int): Number of interpolation steps for gesture realism.
        """
        # ele chama a subfunção pra validar os argumentos
        self._validate_pinch_args(
            locator, scale, duration, direction, movement)

        try:
            driver = self.driver  # -> obtém e valida o driver
            if not driver:
                # -> pra proteger contra sessões ausentes ou mal iniciadas
                raise RuntimeError("The Appium driver is not available.")

            # pra pegar as dimensões da tela
            screen_size = driver.get_window_size()
            screen_width = screen_size['width']
            screen_height = screen_size['height']

            if locator is None:  # -> pro caso do usuário, propopsitalmente, não incluir um locator, ele usa o centro da tela como fallback
                center_x = screen_width / 2
                center_y = screen_height / 2
                # -> e mostra uma mensagem clara pro usuário de que vai usar o centro da tela
                self._builtin.log(
                    "No locator provided. Using center of the screen.", "INFO")
            else:  # -> caso contrário, ele chama a subfunção pra identificar o elemento e calcular seu ponto central
                center_x, center_y, _ = self._get_element_center(locator)
                # -> e mostra uma mensagem clara pro usuário com as coordenadas do centro do elemento
                self._builtin.log(
                    f"Element center at ({center_x}, {center_y})", "INFO")

            # -> aqi ele chama a subfunção pra definir as posições de início de cada dedo com base no centro e na escala
            f1_start, f2_start = self._calculate_finger_inicial_positions(
                center_x, center_y, scale, movement, direction)

            # define as posições finais dos dedos
            offset = 10  # -> define uma distância mínima pra que os dedos se encontrem no final
            if direction.lower() == "vertical":  # -> se o gesto for vertical
                # -> se movem verticalmente com um offset de separação em Y
                f1_end = (center_x, center_y - offset)
                f2_end = (center_x, center_y + offset)
            else:  # -> se o gesto for vertical
                # -> se movem verticalmente com um offset de separação em X
                f1_end = (center_x - offset, center_y)
                f2_end = (center_x + offset, center_y)

            # -> depois chama a subfunção pra ajustar todas as coordenadas pra garantir que estão dentro dos limites da tela
            f1_start, f1_end, f2_start, f2_end = self._adjust_to_screen_bounds(
                [f1_start, f1_end, f2_start, f2_end], screen_width, screen_height
            )

            # -> pra saber exatamente onde o gesto foi executado e registrar exatamente o que foi feito
            # -> vamo incluir um logging detalhado que vai, inclusive,  facilitar a revisão de falhas
            self._builtin.log(f"Finger 1 starts at ({f1_start})", "INFO")
            self._builtin.log(f"Finger 2 starts at ({f2_start})", "INFO")

            # -> aqi a gente cria uma instância de ActionChains, associada ao driver Appium
            actions = ActionChains(driver)
            # -> aqi a gente zera a lista de dispositivos de entrada, pra garantir que vamo começar um gesto do zero
            actions.w3c_actions.devices = []
            # -> usa a API W3C do Appium para criar um roteiro de gestos, enfileirando ações
            finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
            finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')

            # -> aqi ele inicia a configuração do pinch, usando as posições de início dos dedos que a gente definiu acima com a subfunção
            finger1.create_pointer_move(x=f1_start[0], y=f1_start[1])
            finger2.create_pointer_move(x=f2_start[0], y=f2_start[1])

            # -> usa o mousebutton.left pra simular o toque com o dedo (tal qual o botão esquerdo do mouse)
            finger1.create_pointer_down(button=MouseButton.LEFT)
            finger2.create_pointer_down(button=MouseButton.LEFT)

            # -> aqi ele garante uma sincronização realista do gesto, fazendo ambos os dedos tocarem e pressionarem a tela por "pause" segundos
            finger1.create_pause(pause)
            finger2.create_pause(pause)

            # -> cria um loop pra dividir o gesto em etapas de movimento
            for i in range(1, steps + 1):
                # cada etapa simula um frame da "animação" dos dedos se movendo, mostrando uma maior fluidez no movimento
                t = i / steps  # -> esse fator de interpolação vai servir como uma % de progresso do ponto inicial até o final
                # pra mover o dedo 1 suavemente da posição inicial até a final (passo 1 - quase no início/passo 50 - quase no destino)
                # -> o random.uniform introduz um leve ruído no gesto pra simular o comportamento humano
                interp_f1_x = f1_start[0] + t * \
                    (f1_end[0] - f1_start[0]) + random.uniform(-0.5, 0.5)
                # -> esse ruído ajuda a evitar que o appium detecte o movimento como artificial
                interp_f1_y = f1_start[1] + t * \
                    (f1_end[1] - f1_start[1]) + random.uniform(-0.5, 0.5)
                # pra mover o dedo 2 suavemente da posição inicial até a final (passo 1 - quase no início/passo 50 - quase no destino)
                interp_f2_x = f2_start[0] + t * \
                    (f2_end[0] - f2_start[0]) + random.uniform(-0.5, 0.5)
                interp_f2_y = f2_start[1] + t * \
                    (f2_end[1] - f2_start[1]) + random.uniform(-0.5, 0.5)

                # -> ele vai garantir que os dedos não saiam da tela durante o movimento, ajustando aos limites
                interp_f1_x, interp_f1_y = max(0, min(interp_f1_x, screen_width)), max(
                    0, min(interp_f1_y, screen_height))
                interp_f2_x, interp_f2_y = max(0, min(interp_f2_x, screen_width)), max(
                    0, min(interp_f2_y, screen_height))

                # -> encontra a duração do movimento dividindo o tempo total do gesto pelo número de passos, pra cada etapa ser suave e com a mesma duração
                move_duration = int(duration / steps)
                # -> depois diz ao Appium pra mover o dedo pra nova posição interpolada
                finger1.create_pointer_move(
                    x=interp_f1_x, y=interp_f1_y, duration=move_duration)
                finger2.create_pointer_move(
                    x=interp_f2_x, y=interp_f2_y, duration=move_duration)

            # -> aqi ele tira o dedo da tela, finalizando o gesto
            finger1.create_pointer_up(button=MouseButton.LEFT)
            finger2.create_pointer_up(button=MouseButton.LEFT)

            # -> aqi ele executa todas as ações programadas com ActionChains pro dispositivo
            actions.perform()
            # -> seguimos com logging detalhado
            self._builtin.log("Pinch gesture performed successfully.", "INFO")

        except Exception as e:
            raise RuntimeError(
                f"Error while performing the pinch gesture: {str(e)}")
            # -> aqi ele captura qualquer erro do processo e transforma numa mensagem compreensível
