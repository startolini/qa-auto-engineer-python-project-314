import os
import pathlib
import sys
import pytest
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import datetime

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.users_page import UsersPage
from pages.task_statuses_page import TaskStatusesPage
from pages.labels_page import LabelsPage
from pages.tasks_page import TasksPage

# allure и dotenv опциональны: в среде проверки Hexlet их нет
try:
    import allure
except ImportError:
    allure = None

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

DEFAULT_APP_BASE_URL = "http://localhost:5173"
DEFAULT_LOGIN_PATH = "/#/login"


def _headless_enabled() -> bool:
    """HEADLESS=1/0 задаёт режим явно; по умолчанию headless включается
    на Linux без дисплея (CI)."""
    value = os.environ.get("HEADLESS")
    if value is not None:
        return value.lower() in ("1", "true", "yes")
    return sys.platform == "linux" and not os.environ.get("DISPLAY")


def pytest_configure(config):
    if not config.pluginmanager.hasplugin("allure_pytest"):
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_dir = pathlib.Path(f"reports/allure-results-{timestamp}")
    out_dir.mkdir(parents=True, exist_ok=True)
    config.option.allure_report_dir = str(out_dir)

    old_reports = sorted(
        pathlib.Path("reports").glob("allure-results-*"),
        key=lambda p: p.stat().st_mtime,
    )
    for report in old_reports[:-5]:
        shutil.rmtree(report)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if allure and rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")

        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG,
            )


@pytest.fixture
def base_url():
    return os.environ.get("APP_BASE_URL", DEFAULT_APP_BASE_URL)


@pytest.fixture
def login_url(base_url):
    return base_url + os.environ.get("LOGIN_PATH", DEFAULT_LOGIN_PATH)


@pytest.fixture
def driver(request):
    options = Options()
    options.add_argument("--window-size=1366,768")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    if _headless_enabled():
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--disable-web-security")

    chrome_bin = os.environ.get("CHROME_BIN")
    chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")

    if chrome_bin:
        options.binary_location = chrome_bin

    service = (
        Service(executable_path=chromedriver_path) if chromedriver_path else Service()
    )

    driver = webdriver.Chrome(service=service, options=options)
    marker = request.node.get_closest_marker("window_size")
    if marker:
        width, height = marker.args
        driver.set_window_size(width, height)
    yield driver
    driver.quit()


@pytest.fixture
def login_user(base_url, login_url, driver):
    driver.get(login_url)
    LoginPage(driver).login("user", "12345")
    driver.get(base_url)
    return driver


@pytest.fixture
def dashboard_page(login_user):
    return DashboardPage(login_user)


@pytest.fixture
def users_page(dashboard_page):
    dashboard_page.menu.open_users()
    return UsersPage(dashboard_page.driver)


@pytest.fixture
def task_statuses_page(dashboard_page):
    dashboard_page.menu.open_task_statuses()
    return TaskStatusesPage(dashboard_page.driver)


@pytest.fixture
def labels_page(dashboard_page):
    dashboard_page.menu.open_labels()
    return LabelsPage(dashboard_page.driver)


@pytest.fixture
def tasks_page(dashboard_page):
    dashboard_page.menu.open_tasks()
    return TasksPage(dashboard_page.driver)
