from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.action_chains import ActionChains


class AppiumLongPressExtensions:

    
    def __init__(self):
        self._builtin = BuiltIn()
    
    @property
    def _driver(self):
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()
    
    @keyword('LongP')
    def long_press(self, locator, duration=1000):
        
        driver = self._driver
        
        locator_parts = locator.split('=', 1)
        if len(locator_parts) != 2:
            raise ValueError("Locator deve estar no formato 'estrategia=valor'")
        
        strategy, value = locator_parts
        
       
        element = driver.find_element(strategy, value)
        
      
        actions = ActionChains(driver)
        actions.click_and_hold(element).pause(duration/1000).release().perform()

