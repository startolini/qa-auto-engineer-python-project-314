class ByJS:
    def __init__(self, driver):
        self.driver = driver

    def click(self, element) -> None:
        self.driver.execute_script("arguments[0].click();", element)

    def scroll_into_view(self, element) -> None:
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
