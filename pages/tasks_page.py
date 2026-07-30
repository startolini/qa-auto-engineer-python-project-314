from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class TasksPage(BasePage):
    # Локаторы
    @staticmethod
    def locator_column_constructor(column: str) -> tuple:
        return (
            By.XPATH,
            f"//h6[normalize-space()='{column}']/ancestor::div[@class='MuiBox-root css-1xphtog']",
        )

    @staticmethod
    def locator_card_constructor(title: str) -> tuple:
        return (
            By.XPATH,
            f"//div[@data-rfd-draggable-id][.//div[contains(@class, 'MuiTypography-h5')][normalize-space()='{title}']]",
        )

    @staticmethod
    def locator_card_in_column_constructor(title: str, column: str) -> tuple:
        return (
            By.XPATH,
            f"//h6[normalize-space()='{column}']/ancestor::div[@class='MuiBox-root css-1xphtog']"
            f"//div[@data-rfd-draggable-id][.//div[contains(@class, 'MuiTypography-h5')][normalize-space()='{title}']]",
        )

    # MUI Select рендерит скрытый input с именем поля и div[role='combobox'] рядом
    @staticmethod
    def locator_select_constructor(input_name: str) -> tuple:
        return (
            By.XPATH,
            f"//input[@name='{input_name}']/../div[@role='combobox']",
        )

    @staticmethod
    def locator_option_constructor(text: str) -> tuple:
        return (By.XPATH, f"//li[@role='option'][normalize-space()='{text}']")

    CREATE_TASK_BUTTON = (By.CSS_SELECTOR, 'a[aria-label="Create"]')
    TASK_TITLE_INPUT = (By.CSS_SELECTOR, "input[name='title']")
    TASK_CONTENT_INPUT = (By.CSS_SELECTOR, "textarea[name='content']")
    SAVE_BUTTON = (By.CSS_SELECTOR, '[aria-label="Save"]')
    DELETE_BUTTON = (By.CSS_SELECTOR, '[aria-label="Delete"]')
    ASSIGNEE_SELECT = (
        By.XPATH,
        "//input[@name='assignee_id']/../div[@role='combobox']",
    )
    STATUS_SELECT = (By.XPATH, "//input[@name='status_id']/../div[@role='combobox']")
    CLEAR_FILTER_OPTION = (By.CSS_SELECTOR, 'li[aria-label="Clear value"]')

    ALL_TASK_CARDS = (By.XPATH, "//div[@data-rfd-draggable-id]")
    CARD_TITLE = (By.XPATH, ".//div[contains(@class, 'MuiTypography-h5')]")
    CARD_DESCRIPTION = (By.XPATH, ".//p[contains(@class, 'MuiTypography-body2')]")
    CARD_INDEX = (By.XPATH, ".//p[contains(@class, 'MuiTypography-body1')]")
    CARD_EDIT_LINK = (By.CSS_SELECTOR, 'a[aria-label="Edit"]')

    # Создание и форма
    def click_create_task(self):
        """Click the floating Create button"""
        self.click(self.CREATE_TASK_BUTTON)

    def check_task_form_visible(self) -> bool:
        """Check that required fields (title, assignee, status) are visible"""
        return (
            self.is_visible(self.TASK_TITLE_INPUT)
            and self.is_visible(self.ASSIGNEE_SELECT)
            and self.is_visible(self.STATUS_SELECT)
        )

    def select_option(self, input_name: str, option_text: str):
        """Open a MUI select by its hidden input name and pick an option"""
        self.click(self.locator_select_constructor(input_name))
        self.click(self.locator_option_constructor(option_text))

    def create_task(self, title: str, assignee: str, status: str, content: str = ""):
        """Fill the creation form and save"""
        self.by_js.type(self.TASK_TITLE_INPUT, title)
        if content:
            self.by_js.type(self.TASK_CONTENT_INPUT, content)
        self.select_option("assignee_id", assignee)
        self.select_option("status_id", status)
        self.click(self.SAVE_BUTTON)

    # Редактирование и удаление
    def open_card_editing(self, title: str):
        """Open the edit form via the Edit link on a card"""
        card = self.find_element(self.locator_card_constructor(title))
        edit_link = card.find_element(*self.CARD_EDIT_LINK)
        self.by_js.click(edit_link)

    def change_task_title(self, new_title: str):
        self.by_js.type(self.TASK_TITLE_INPUT, new_title)

    def change_task_status(self, status: str):
        self.select_option("status_id", status)

    def save_task(self):
        self.click(self.SAVE_BUTTON)

    def delete_task(self):
        self.click(self.DELETE_BUTTON)

    # Фильтры
    def apply_filter(self, input_name: str, option_text: str):
        self.select_option(input_name, option_text)

    def clear_filter(self, input_name: str):
        self.click(self.locator_select_constructor(input_name))
        self.click(self.CLEAR_FILTER_OPTION)

    # Доска
    def get_board_card_count(self) -> int:
        return len(self.find_elements(self.ALL_TASK_CARDS))

    def wait_for_card_count_change(self, previous: int) -> int:
        self.wait.until(
            lambda d: len(d.find_elements(*self.ALL_TASK_CARDS)) != previous
        )
        return self.get_board_card_count()

    def card_in_column(self, title: str, column: str) -> bool:
        locator = self.locator_card_in_column_constructor(title, column)
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except Exception:
            return False

    def card_not_on_board(self, title: str) -> bool:
        return len(self.find_elements(self.locator_card_constructor(title))) == 0

    def card_not_in_column(self, title: str, column: str) -> bool:
        locator = self.locator_card_in_column_constructor(title, column)
        return len(self.find_elements(locator)) == 0

    def get_all_cards_in_draft(self):
        """Get all task cards in Draft column"""
        draft_column = self.find_element(self.locator_column_constructor("Draft"))
        cards = draft_column.find_elements(By.XPATH, ".//div[@data-rfd-draggable-id]")
        return cards

    def get_card_titles_in_draft(self):
        """Get titles of all cards in Draft column"""
        cards = self.get_all_cards_in_draft()
        titles = []
        for card in cards:
            title_element = card.find_element(*self.CARD_TITLE)
            titles.append(title_element.text)
        return titles

    def get_card_info_in_draft(self):
        """Get complete info for all cards in Draft column"""
        cards = self.get_all_cards_in_draft()
        cards_info = []

        for card in cards:
            try:
                title = card.find_element(*self.CARD_TITLE).text
                description = card.find_element(*self.CARD_DESCRIPTION).text
                index = card.find_element(*self.CARD_INDEX).text
                card_id = card.get_attribute("data-rfd-draggable-id")

                cards_info.append(
                    {
                        "id": card_id,
                        "title": title,
                        "description": description,
                        "index": index,
                        "element": card,
                    }
                )
            except Exception as e:
                print(f"Error getting card info: {e}")
                continue

        return cards_info

    def get_card_count_in_draft(self):
        """Get number of cards in Draft column"""
        return len(self.get_all_cards_in_draft())

    def wait_for_cards_loaded(self, timeout=10):
        """Wait for cards to be loaded on the board"""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.ALL_TASK_CARDS)
        )

    def scroll_to_card(self, card_element):
        """Scroll to specific card using ByJS"""
        self.by_js.scroll_into_view(card_element)
