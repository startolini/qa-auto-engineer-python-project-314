from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ByJS:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click(self, element) -> None:
        self.driver.execute_script("arguments[0].click();", element)

    def scroll_into_view(self, element) -> None:
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

    def type(self, locator, text) -> None:
        el = self.driver.find_element(*locator)
        self.clear_input_with_backspace(locator)
        el.send_keys(text)

    def clear_input_with_backspace(
        self, locator: tuple, letter_count: int | None = None
    ):
        element = self.wait.until(EC.visibility_of_element_located(locator))

        current_value = element.get_attribute("value")
        current_letter_count = len(current_value) if current_value else 0

        if current_letter_count == 0:
            return

        if letter_count is not None and letter_count == current_letter_count:
            raise AssertionError("Cannot clear input via backspace")

        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().double_click().perform()

        for _ in range(current_letter_count):
            actions.send_keys(Keys.BACKSPACE)
        actions.send_keys(Keys.NULL).perform()

        # Рекурсивный вызов для проверки
        self.clear_input_with_backspace(locator, current_letter_count)
