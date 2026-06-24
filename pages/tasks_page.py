from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class TasksPage(BasePage):
    # Локаторы
    DRAFT_COLUMN = (By.XPATH, "//h6[text()='Draft']/ancestor::div[@class='MuiBox-root css-1xphtog']")
    DRAFT_CARDS = (By.XPATH, "//h6[text()='Draft']/ancestor::div[@class='MuiBox-root css-1xphtog']//div[@data-rfd-draggable-id]")
    
    # Альтернативные локаторы
    ALL_TASK_CARDS = (By.XPATH, "//div[@data-rfd-draggable-id]")
    CARD_TITLE = (By.XPATH, ".//div[@class='MuiTypography-root MuiTypography-h5']")
    CARD_DESCRIPTION = (By.XPATH, ".//p[@class='MuiTypography-root MuiTypography-body2']")
    CARD_INDEX = (By.XPATH, ".//p[@class='MuiTypography-root MuiTypography-body1']")
    
    def get_all_cards_in_draft(self):
        """Get all task cards in Draft column"""
        draft_column = self.find_element(self.DRAFT_COLUMN)
        cards = draft_column.find_elements(By.XPATH, ".//div[@data-rfd-draggable-id]")
        return cards
    
    def get_all_task_cards(self):
        """Get all task cards from all columns"""
        return self.find_elements(self.ALL_TASK_CARDS)
    
    def get_card_titles_in_draft(self):
        """Get titles of all cards in Draft column"""
        cards = self.get_all_cards_in_draft()
        titles = []
        for card in cards:
            title_element = card.find_element(By.XPATH, ".//div[@class='MuiTypography-root MuiTypography-h5']")
            titles.append(title_element.text)
        return titles
    
    def get_card_info_in_draft(self):
        """Get complete info for all cards in Draft column"""
        cards = self.get_all_cards_in_draft()
        cards_info = []
        
        for card in cards:
            try:
                title = card.find_element(By.XPATH, ".//div[@class='MuiTypography-root MuiTypography-h5']").text
                description = card.find_element(By.XPATH, ".//p[@class='MuiTypography-root MuiTypography-body2']").text
                index = card.find_element(By.XPATH, ".//p[@class='MuiTypography-root MuiTypography-body1']").text
                card_id = card.get_attribute("data-rfd-draggable-id")
                
                cards_info.append({
                    'id': card_id,
                    'title': title,
                    'description': description,
                    'index': index,
                    'element': card
                })
            except Exception as e:
                print(f"Error getting card info: {e}")
                continue
                
        return cards_info
    
    def get_card_by_title(self, title):
        """Find a card by its title in Draft column"""
        cards = self.get_all_cards_in_draft()
        for card in cards:
            try:
                card_title = card.find_element(By.XPATH, ".//div[@class='MuiTypography-root MuiTypography-h5']").text
                if card_title == title:
                    return card
            except:
                continue
        return None
    
    def get_card_count_in_draft(self):
        """Get number of cards in Draft column"""
        return len(self.get_all_cards_in_draft())
    
    def wait_for_cards_loaded(self, timeout=10):
        """Wait for cards to be loaded in Draft column"""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.DRAFT_CARDS)
        )

    def scroll_to_card(self, card_element):
        """Scroll to specific card using ByJS"""
        self.by_js.scroll_into_view(card_element)
    
    def get_card_by_title_and_scroll(self, title):
        """Find card by title and scroll to it"""
        cards = self.get_all_cards_in_draft()
        for card in cards:
            try:
                card_title = card.find_element(By.XPATH, ".//div[@class='MuiTypography-root MuiTypography-h5']").text
                if card_title == title:
                    # Скроллим к карточке
                    self.by_js.scroll_into_view(card)
                    return card
            except:
                continue
        return None