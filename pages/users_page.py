from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.utils import is_valid_email


class UsersPage(BasePage):
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

    @staticmethod
    def locator_checkbox_constructor(value: str) -> tuple:
        return (
            By.XPATH,
            f"//tr[.//td[contains(@class, 'column-email')]//span[normalize-space()='{value}']]//input[@type='checkbox']",
        )

    CREATE_USER_BTN = (By.CSS_SELECTOR, '[aria-label="Create"]')
    SELECT_ALL_CHECKBOX = (By.CSS_SELECTOR, '[aria-label="Select all"]')
    EMAIL_INPUT = (By.CSS_SELECTOR, '[name="email"]')
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, '[name="firstName"]')
    LAST_NAME_INPUT = (By.CSS_SELECTOR, '[name="lastName"]')
    SAVE_BUTTON = (By.CSS_SELECTOR, '[aria-label="Save"]')
    SNACKBAR = (By.CSS_SELECTOR, '[role="alert"]')
    DELETE_USER_BTN = (By.CSS_SELECTOR, '[aria-label="Delete"]')
    SELECT_ALL_CHECKBOX = (By.CSS_SELECTOR, '[aria-label="Select all"]')
    NO_USERS_LOGO = (By.CSS_SELECTOR, '[data-testid="InboxIcon"]')

    def creat_user(self, email: str, first_name: str, last_name: str):
        self.click(self.CREATE_USER_BTN)
        self.type(self.EMAIL_INPUT, email)
        self.type(self.FIRST_NAME_INPUT, first_name)
        self.type(self.LAST_NAME_INPUT, last_name)
        self.click(self.SAVE_BUTTON)

    def snackbar_visible(self) -> bool:
        return self.is_visible(self.SNACKBAR)

    def change_user_email(self, new_email: str):
        self.click(self.EMAIL_INPUT)
        assert is_valid_email(new_email), f"Invalid email: {new_email}"
        self.type(self.EMAIL_INPUT, new_email)
        self.click(self.SAVE_BUTTON)

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

    def select_user_by_email(self, email: str):
        el = self.find_element(self.locator_checkbox_constructor(email))
        self.by_js.click(el)

    def select_all_users(self):
        el = self.find_element(self.SELECT_ALL_CHECKBOX)
        self.by_js.click(el)

    def click_delete_btn(self):
        self.click(self.DELETE_USER_BTN)

    def email_not_in_table(self, email: str) -> bool:
        elements = self.find_elements(self.locator_row_constructor(email))
        return len(elements) == 0

    def no_users_logo_visible(self) -> bool:
        return self.is_visible(self.NO_USERS_LOGO)
