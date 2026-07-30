from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_list_page import BaseListPage


class UsersPage(BaseListPage):
    ROW_KEY_COLUMN = "column-email"

    @staticmethod
    def locator_header_constructor(value: str) -> tuple:
        return (
            By.XPATH,
            f"//th[contains(@class, 'column')]//span[normalize-space()='{value}']",
        )

    @staticmethod
    def locator_row_constructor(value: str) -> tuple:
        return (
            By.XPATH,
            f"//td[contains(@class, 'column')]//span[normalize-space()='{value}']",
        )

    EMAIL_INPUT = (By.CSS_SELECTOR, '[name="email"]')
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, '[name="firstName"]')
    LAST_NAME_INPUT = (By.CSS_SELECTOR, '[name="lastName"]')
    VALIDATION_ERROR = (By.CSS_SELECTOR, "p.MuiFormHelperText-root.Mui-error")

    def check_user_inputs_visible(self) -> bool:
        return (
            self.is_visible(self.EMAIL_INPUT)
            and self.is_visible(self.FIRST_NAME_INPUT)
            and self.is_visible(self.LAST_NAME_INPUT)
        )

    def create_user(self, email: str, first_name: str, last_name: str):
        self.type(self.EMAIL_INPUT, email)
        self.type(self.FIRST_NAME_INPUT, first_name)
        self.type(self.LAST_NAME_INPUT, last_name)
        self.click_save()

    def change_user_email(self, new_email: str):
        self.click(self.EMAIL_INPUT)
        self.by_js.type(self.EMAIL_INPUT, new_email)
        self.click_save()

    def get_validation_error_text(self) -> str:
        el = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
        return el.text

    def check_user_in_table(self, email: str, first_name: str, last_name: str) -> bool:
        return (
            email in self.get_text(self.locator_row_constructor(email))
            and first_name in self.get_text(self.locator_row_constructor(first_name))
            and last_name in self.get_text(self.locator_row_constructor(last_name))
        )

    def check_table_header_visible(self) -> bool:
        return (
            self.is_visible(self.locator_header_constructor("Email"))
            and self.is_visible(self.locator_header_constructor("First name"))
            and self.is_visible(self.locator_header_constructor("Last name"))
        )

    def check_all_ids_visible(self, end_id: int) -> bool:
        for row_id in range(1, end_id + 1):
            if not self.is_visible(self.locator_row_constructor(str(row_id))):
                return False
        return True

    def open_user_details(self, email: str) -> tuple[str, str, str]:
        self.click(self.locator_row_constructor(email))
        return (
            self.get_dom_attribute(self.EMAIL_INPUT, "value") or "",
            self.get_dom_attribute(self.FIRST_NAME_INPUT, "value") or "",
            self.get_dom_attribute(self.LAST_NAME_INPUT, "value") or "",
        )

    def email_not_in_table(self, email: str) -> bool:
        elements = self.find_elements(self.locator_row_constructor(email))
        return len(elements) == 0
