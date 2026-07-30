from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DashboardPage(BasePage):
    PROFILE = (By.CSS_SELECTOR, '[aria-label="Profile"]')
    LOGOUT_BTN = (
        By.XPATH,
        "//ul[contains(@class, 'MuiList-root')]//span[normalize-space(text())='Logout']",
    )

    def logout(self) -> None:
        self.click(self.PROFILE)
        el = self.find_element(self.LOGOUT_BTN)
        self.by_js.click(el)

    def profile_button_not_visible(self) -> bool:
        return self.is_not_visible(self.PROFILE)
