from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class TaskStatusesPage(BasePage):
    @staticmethod
    def locator_name_constructor(value: str) -> tuple:
        return (
            By.XPATH,
            f"//td[contains(@class, 'column-name')]//span[normalize-space()='{value}']",
        )

    @staticmethod
    def locator_slug_constructor(value: str) -> tuple:
        return (
            By.XPATH,
            f"//td[contains(@class, 'column-slug')]//span[normalize-space()='{value}']",
        )

    CREATE_BTN = (By.CSS_SELECTOR, '[aria-label="Create"]')
    NAME_INPUT = (By.CSS_SELECTOR, '[name="name"]')
    SLUG_INPUT = (By.CSS_SELECTOR, '[name="slug"]')
    SAVE_BUTTON = (By.CSS_SELECTOR, '[type="submit"]')
    NAME_COLUMN = (By.CSS_SELECTOR, '[class*="column-name"]')
    SLUG_COLUMN = (By.CSS_SELECTOR, '[class*="column-slug"]')
    SELECT_ALL_CHECKBOX = (By.CSS_SELECTOR, '[aria-label="Select all"]')
    DELETE_STATUS_BTN = (By.CSS_SELECTOR, '[aria-label="Delete"]')
    NO_STATUSES_LOGO = (By.CSS_SELECTOR, '[data-testid="InboxIcon"]')

    def click_create_status(self) -> None:
        self.click(self.CREATE_BTN)

    def check_status_inputs_visible(self) -> bool:
        return self.is_visible(self.NAME_INPUT) and self.is_visible(self.SLUG_INPUT)

    def create_status(self, name: str, slug: str) -> None:
        self.type(self.NAME_INPUT, name)
        self.type(self.SLUG_INPUT, slug)
        self.click(self.SAVE_BUTTON)

    def get_values_from_table(self, name: str, slug: str) -> tuple:
        name_value = self.get_text(self.locator_name_constructor(name))
        slug_value = self.get_text(self.locator_slug_constructor(slug))
        return name_value, slug_value

    def open_status_details(self, name: str) -> tuple[str, str]:
        self.click(self.locator_name_constructor(name))
        return (
            self.get_dom_attribute(self.NAME_INPUT, "value") or "",
            self.get_dom_attribute(self.SLUG_INPUT, "value") or "",
        )

    def get_statuses_text(self) -> list[str]:
        return self.get_texts(self.NAME_COLUMN)

    def get_slugs_text(self) -> list[str]:
        return self.get_texts(self.SLUG_COLUMN)

    def select_all_statuses(self):
        el = self.find_element(self.SELECT_ALL_CHECKBOX)
        self.by_js.click(el)

    def click_delete_btn(self):
        self.click(self.DELETE_STATUS_BTN)

    def no_statuses_logo_visible(self) -> bool:
        return self.is_visible(self.NO_STATUSES_LOGO)
