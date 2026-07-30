from selenium.webdriver.common.by import By
from pages.base_list_page import BaseListPage


class TaskStatusesPage(BaseListPage):
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

    NAME_INPUT = (By.CSS_SELECTOR, '[name="name"]')
    SLUG_INPUT = (By.CSS_SELECTOR, '[name="slug"]')
    NAME_COLUMN = (By.CSS_SELECTOR, '[class*="column-name"]')

    def check_status_inputs_visible(self) -> bool:
        return self.is_visible(self.NAME_INPUT) and self.is_visible(self.SLUG_INPUT)

    def create_status(self, name: str, slug: str) -> None:
        self.by_js.type(self.NAME_INPUT, name)
        self.by_js.type(self.SLUG_INPUT, slug)
        self.click_save()

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

    def status_not_in_table(self, name: str) -> bool:
        return len(self.find_elements(self.locator_name_constructor(name))) == 0
