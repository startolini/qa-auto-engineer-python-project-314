from selenium.webdriver.common.by import By


class MenuItems:
    DASHBOARD = (By.XPATH, "//a[.='Dashboard']")
    TASKS = (By.XPATH, "//a[.='Tasks']")
    USERS = (By.XPATH, "//a[.='Users']")
    LABELS = (By.XPATH, "//a[.='Labels']")
    TASK_STATUSES = (By.XPATH, "//a[.='Task statuses']")


class SideMenuWidget:
    def __init__(self, page):
        self.page = page
        self.driver = page.driver

    def open_tasks(self):
        self.page.click(MenuItems.TASKS)

    def open_users(self):
        self.page.click(MenuItems.USERS)

    def open_labels(self):
        self.page.click(MenuItems.LABELS)

    def open_task_statuses(self):
        self.page.click(MenuItems.TASK_STATUSES)

    def open_dashboard(self):
        self.page.click(MenuItems.DASHBOARD)
