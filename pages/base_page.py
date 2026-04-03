from typing import TYPE_CHECKING
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.by_js import ByJS
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pages.side_menu_widget import SideMenuWidget
from utils.utils import get_os

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.menu = SideMenuWidget(self)
        self.by_js = ByJS(driver)
        self.actions = ActionChains(driver)

    def find_element(self, locator: tuple) -> "WebElement":
        return self.driver.find_element(*locator)

    def find_elements(self, locator: tuple) -> list["WebElement"]:
        return self.driver.find_elements(*locator)

    def open(self, url: str) -> None:
        self.driver.get(url)

    def click(self, locator: tuple) -> None:
        el = self.wait.until(EC.element_to_be_clickable(locator))
        el.click()

    def type(self, locator: tuple, text: str) -> None:
        el = self.wait.until(EC.visibility_of_element_located(locator))
        self.actions.click(el)
        self.actions.key_down(
            Keys.COMMAND if get_os() == "mac" else Keys.CONTROL
        ).send_keys("a").key_up(Keys.COMMAND)
        self.actions.send_keys(Keys.BACKSPACE)
        self.actions.perform()

        el.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        return self.find_element(locator).text

    def get_texts(self, locator: tuple) -> list[str]:
        elements = self.find_elements(locator)
        return [el.text for el in elements]

    def get_dom_attribute(self, locator: tuple, name: str) -> str | None:
        value = self.find_element(locator).get_dom_attribute(name)
        if value == "":
            return None
        return value

    def is_visible(self, locator: tuple) -> bool:
        try:
            return self.find_element(locator).is_displayed()
        except NoSuchElementException:
            return False

    def is_not_visible(self, locator: tuple) -> bool:
        return not self.is_visible(locator)
