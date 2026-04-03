from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LabelsPage(BasePage):
    @staticmethod
    def locator_name_constructor(value: str) -> tuple:
        return (
            By.XPATH,
            f"//td[contains(@class, 'column-name')]//span[normalize-space()='{value}']",
        )

    @staticmethod
    def locator_checkbox_constructor(value: str) -> tuple:
        return (
            By.XPATH,
            f"//tr[.//td[contains(@class, 'column-name')]//span[normalize-space()='{value}']]//input[@type='checkbox']",
        )

    CREATE_BTN = (By.CSS_SELECTOR, '[aria-label="Create"]')
    NAME_INPUT = (By.CSS_SELECTOR, '[name="name"]')
    SAVE_BUTTON = (By.CSS_SELECTOR, '[type="submit"]')
    NAME_COLUMN = (By.CSS_SELECTOR, '[class*="column-name"]')
    SELECT_ALL_CHECKBOX = (By.CSS_SELECTOR, '[aria-label="Select all"]')
    DELETE_STATUS_BTN = (By.CSS_SELECTOR, '[aria-label="Delete"]')
    NO_LABELS_LOGO = (By.CSS_SELECTOR, '[data-testid="InboxIcon"]')

    def click_create_label(self) -> None:
        self.click(self.CREATE_BTN)

    def check_label_input_visible(self) -> bool:
        return self.is_visible(self.NAME_INPUT)

    def create_label(self, name: str) -> None:
        self.type(self.NAME_INPUT, name)
        self.click(self.SAVE_BUTTON)

    def get_value_from_table(self, name: str) -> str:
        name_value = self.get_text(self.locator_name_constructor(name))
        return name_value

    def open_label_details(self, name: str) -> str:
        self.click(self.locator_name_constructor(name))
        return self.get_dom_attribute(self.NAME_INPUT, "value") or ""

    def get_labels_text(self) -> list[str]:
        return self.get_texts(self.NAME_COLUMN)

    def select_all_labels(self):
        el = self.find_element(self.SELECT_ALL_CHECKBOX)
        self.by_js.click(el)

    def click_delete_btn(self):
        self.click(self.DELETE_STATUS_BTN)

    def no_labels_logo_visible(self) -> bool:
        return self.is_visible(self.NO_LABELS_LOGO)

    def select_label_by_name(self, name: str):
        el = self.find_element(self.locator_checkbox_constructor(name))
        self.by_js.click(el)
