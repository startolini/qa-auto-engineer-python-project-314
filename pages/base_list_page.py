from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class BaseListPage(BasePage):
    """Общие локаторы и действия списков (пользователи, статусы, метки)."""

    # Колонка, по значению которой ищется строка при выборе чекбокса
    ROW_KEY_COLUMN = "column-name"

    CREATE_BTN = (By.CSS_SELECTOR, '[aria-label="Create"]')
    SAVE_BUTTON = (By.CSS_SELECTOR, '[aria-label="Save"]')
    DELETE_BTN = (By.CSS_SELECTOR, '[aria-label="Delete"]')
    SELECT_ALL_CHECKBOX = (By.CSS_SELECTOR, '[aria-label="Select all"]')
    NO_ITEMS_LOGO = (By.CSS_SELECTOR, '[data-testid="InboxIcon"]')

    @classmethod
    def locator_row_checkbox_constructor(cls, value: str) -> tuple:
        return (
            By.XPATH,
            f"//tr[.//td[contains(@class, '{cls.ROW_KEY_COLUMN}')]"
            f"//span[normalize-space()='{value}']]//input[@type='checkbox']",
        )

    def click_create(self) -> None:
        self.click(self.CREATE_BTN)

    def click_save(self) -> None:
        self.click(self.SAVE_BUTTON)

    def click_delete_btn(self) -> None:
        self.click(self.DELETE_BTN)

    def select_row_by_value(self, value: str) -> None:
        el = self.find_element(self.locator_row_checkbox_constructor(value))
        self.by_js.click(el)

    def select_all_rows(self) -> None:
        el = self.find_element(self.SELECT_ALL_CHECKBOX)
        self.by_js.click(el)

    def no_items_logo_visible(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self.NO_ITEMS_LOGO))
            return True
        except TimeoutException:
            return False
