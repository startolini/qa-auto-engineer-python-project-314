from selenium.webdriver.common.by import By
from pages.base_list_page import BaseListPage


class LabelsPage(BaseListPage):
    @staticmethod
    def locator_name_constructor(value: str) -> tuple:
        return (
            By.XPATH,
            f"//td[contains(@class, 'column-name')]//span[normalize-space()='{value}']",
        )

    NAME_INPUT = (By.CSS_SELECTOR, '[name="name"]')
    NAME_COLUMN = (By.CSS_SELECTOR, '[class*="column-name"]')

    def check_label_input_visible(self) -> bool:
        return self.is_visible(self.NAME_INPUT)

    def create_label(self, name: str) -> None:
        self.by_js.type(self.NAME_INPUT, name)
        self.click_save()

    def get_value_from_table(self, name: str) -> str:
        return self.get_text(self.locator_name_constructor(name))

    def open_label_details(self, name: str) -> str:
        self.click(self.locator_name_constructor(name))
        return self.get_dom_attribute(self.NAME_INPUT, "value") or ""

    def get_labels_text(self) -> list[str]:
        return self.get_texts(self.NAME_COLUMN)
