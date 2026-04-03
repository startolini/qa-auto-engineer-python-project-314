from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class LoginPage(BasePage):
    USER = (By.CSS_SELECTOR, '[name="username"]')
    PASS = (By.CSS_SELECTOR, '[name="password"]')
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")

    def login(self, username: str, password: str) -> None:
        self.type(self.USER, username)
        self.type(self.PASS, password)
        self.click(self.SUBMIT_BTN)

    def submit_button_not_visile(self):
        return self.wait.until(EC.invisibility_of_element_located(self.SUBMIT_BTN))
