from robot.api.deco import keyword
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, WebDriverException
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.by import By
import json


class VisibleElements:
    """
    Custom AppiumLibrary keyword that returns visible elements on the screen using either resource-id or content-desc (accessibility_id on Android), optionally filtered by type.
    Useful for visual validation in mobile automation tests.
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'


    def __init__(self):
        self._builtin = BuiltIn()

    def _get_appium_driver(self):
    # Gets the current Appium driver instance
        appium_lib = self._builtin.get_library_instance("AppiumLibrary")
        return appium_lib._current_application()
    
    def _find_all_elements(self, driver):
    # Return all elements in the current screen using a generic XPath
        return driver.find_elements(By.XPATH, "//*")
    
    def _safe_attr(self, el, name):
    # Read attribute, strip, and normalize empty/null to ''.
    # A inclusão dessa função ajuda na robustez e legibilidade do código, evitando ter que repetir o mesmo padrão de try/except/strip/null em vários pontos
        try:
            val = el.get_attribute(name) #-> ele vai tentar ler o atributo do elemento
        except Exception:
            return "" #-> e retornar "" caso ocorra um erro de exceção de leitura, em vez de quebrar o fluxo
        if not val:
            return "" #-> tbm vai normalizar valores ruins/vazios, transformando "None", espaços e até o texto literal "null" em ""
        val = str(val).strip()
        if not val or val.lower() == "null":
            return ""
        return val #-> e retornar o valor limpo/não-vazio

    def _passes_filter(self, el, filter_type):
    # Check if the element matches the given filter type
        """Args:
            el (WebElement): the element to evaluate.
            filter_type (str): filter type options ('all' | 'clickable' | 'text' | 'button' | 'input').

        Returns:
            bool: Returns True if the element passes the filter, False otherwise."""
        
        class_name = self._safe_attr(el, "class") or self._safe_attr(el, "className")
        text = (el.text or "").strip()
        clickable_attr = self._safe_attr(el, "clickable")
        clickable = str(clickable_attr).strip().lower() == "true" #-> só pra não falhar no caso de receber "True", com T maiúsculo

        if filter_type == "all":
            return True
        if filter_type == "clickable":
            return clickable
        if filter_type == "text":
            return bool(text)
        if filter_type == "button":
            return "Button" in class_name
        if filter_type == "input":
            return "EditText" in class_name
        # Returns False in case of an unrecognized filter (should not occur due to prior validation)
        return False
    
    def _choose_identifier(self, el, id_mode):
        """
        Returns (value, kind) according to id_mode:
          - 'auto': prefer resource-id; if empty, fallback to content-desc
          - 'resource_id': resource-id only
          - 'accessibility_id': content-desc only (Android accessibility_id alias)
        """
        rid = self._safe_attr(el, "resource-id")
        cdesc = self._safe_attr(el, "content-desc")

        if id_mode == "resource_id":
            return (rid, "resource_id") if rid else (None, None)
        if id_mode == "accessibility_id":
            return (cdesc, "accessibility_id") if cdesc else (None, None)
        # Em id_mode = "auto", pra cada elemento que passa no filter_type ele vai tentar ler o resource_id, se não houver rid válido, ele tenta o content-desc
        # Elementos sem nenhum desses dois identificadores, continuam sendo mantidos de fora
        # A prioridade continua sendo o resource_id que costuma ser mais estável
        # Em resumo, em modo auto, a lista fica mista -> com resource_id e accessibility_id (content-desc)
        if rid:
            return rid, "resource_id"
        if cdesc:
            return cdesc, "accessibility_id"
        return None, None

    def _build_debug_dict(self, el, chosen_value, chosen_kind):
    # Build a structured dictionary of element attributes for debug mode
        """Args:
            el (WebElement): the element that passed the visibility and `filter_type` checks.
            chosen_value (str): the identifier value selected according to `id_mode` (e.g., resource-id or content-desc).
            chosen_kind(str): the type of identifier selected. One of: 'resource_id' | 'accessibility_id' (on Android, accessibility_id is an alias of content-desc).

        Returns:
            dict: Structured data for debugging and inspection.
        """
        
        return {
            "identifier": {"value": chosen_value, "kind": chosen_kind}, #-> inclui o tipo de id usado e seu valor pra ajudar na rastreabilidade
            "resource_id": self._safe_attr(el, "resource-id"),
            "accessibility_id": self._safe_attr(el, "content-desc"),
            "text": el.text or "",
            "class": self._safe_attr(el, "class"),
            "clickable": self._safe_attr(el, "clickable") == "true"
        }

    @keyword("Get Visible Elements On Screen")
    def get_visible_elements_on_screen(self, filter_type: str = "all", id_mode: str = "auto", debug: bool = False):
        """
        Return visible screen elements using either resource_id or accessibility_id (per id_mode), optionally filtered by type.

        Args:
            filter_type (str): Filter to apply. Options: 'all' | 'clickable' | 'text' | 'button' | 'input'.
            id_mode (str): Identifier mode. Options: 'auto' | 'resource_id' | 'accessibility_id'. Note: on Android, 'accessibility_id' reads 'content-desc'.
            debug (bool): If debug=True, return full element details as JSON; otherwise, return a list of IDs.

        Returns:
            list: List of filtered visible elements.
        """

        valid_filters = {'all', 'clickable', 'text', 'button', 'input'}
        # Normalize input to lowercase (lower()) and strip (strip()) spaces to avoid typos
        filter_type = (filter_type or "").strip().lower() #-> ajustezinho pra garantir que não quebra se vierem "None"
        if filter_type not in valid_filters:
            self._builtin.fail(f"Invalid filter '{filter_type}'. Options: {valid_filters}")

        # vamo incluir uma validação do id_mode pra validar o erro, quando for o caso.
        valid_ids = {"auto", "resource_id", "accessibility_id"}
        # Normalize input to lowercase (lower()) and strip (strip()) spaces to avoid typos
        id_mode = (id_mode or "").strip().lower()
        if id_mode not in valid_ids:
            self._builtin.fail(f"Invalid id_mode '{id_mode}'. Options: {valid_ids}")

        driver = self._get_appium_driver()
        try:
            elements = self._find_all_elements(driver)
        except WebDriverException as e:
            self._builtin.log(f"Error fetching elements: {e}", level="ERROR")
            return []
        
        self._builtin.log(f"Found {len(elements)} elements before filtering", level="DEBUG")

        visible_elements = []
        seen = set() #-> em telas dinâmicas, é possível que o Appium capte um elemento duas vezes, então vamo incluir um seen pra evitar duplicados no resultado fora do modo debug
        for el in elements:
            try:
                # First filter: real visibility
                try: #-> incluí esse try/except pra deixar o is_displayed() mais resiliente em telas dinâmicas
                    if not el.is_displayed():
                        continue
                except (StaleElementReferenceException, NoSuchElementException):
                    continue

                # Second filter: match element type
                # Vai ser mais barato colocar a filtragem por tipo antes, pra poupar leituras de atributos de elementos que seriam descartados
                if not self._passes_filter(el, filter_type):
                    continue 

                # Third filter: must yield a chosen identifier
                chosen_value, chosen_kind = self._choose_identifier(el, id_mode)
                if not chosen_value:
                    continue

                # Deduplicar pela tupla pra evitar uma possível colisão (mesmo que seja raro) se o resource_id do elemento for igual ao content-desc
                key = (chosen_kind, chosen_value)
                if key in seen:
                    continue
                seen.add(key)

                # Define return format
                if debug:
                    # debug mode
                    visible_elements.append(self._build_debug_dict(el, chosen_value, chosen_kind))
                else:
                    # normal mode
                    visible_elements.append(chosen_value)

            # Ignore elements that are no longer valid
            except (StaleElementReferenceException, NoSuchElementException) as ex:
            # NoSuchElementException: the element does not exist (e.g., invalid selector or not rendered yet)
            # StaleElementReferenceException: the element is no longer attached to the DOM (e.g., dynamic re-render)
                self._builtin.log(f"Ignored element due to {type(ex).__name__}: {ex}", level="DEBUG")
                continue

        # Log total elements that passed all filters
        count = len(visible_elements)
        self._builtin.log (f"Total visible elements after filtering: {count}", level="INFO")

        if debug:
            debug_output = json.dumps(visible_elements, indent=2)
            self._builtin.log("DEBUG JSON:\n" + debug_output, level="INFO")

        else:
            self._builtin.log("Visible elements:\n" + json.dumps(visible_elements, indent=2), level="INFO")
        return visible_elements