import os
import pathlib
import pytest
import allure
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


def pytest_configure(config):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_dir = pathlib.Path(f"reports/allure-results-{timestamp}")
    out_dir.mkdir(parents=True, exist_ok=True)
    config.option.allure_report_dir = str(out_dir)

    old_reports = sorted(pathlib.Path("reports").glob("allure-results-*"), key=lambda p: p.stat().st_mtime)
    for report in old_reports[:-5]:
        shutil.rmtree(report)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")

        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG,
            )


@pytest.fixture
def base_url():
    return os.environ.get("APP_BASE_URL")


@pytest.fixture
def login_url():
    base = os.environ.get("APP_BASE_URL") or ""
    path = os.environ.get("LOGIN_PATH") or ""
    return base + path


@pytest.fixture
def driver(request):
    options = Options()
    options.add_argument("--window-size=1366,768")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--disable-web-security")

    chrome_bin = os.environ.get("CHROME_BIN")
    chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")

    if chrome_bin:
        options.binary_location = chrome_bin

    from selenium.webdriver.chrome.service import Service
    service = Service(executable_path=chromedriver_path) if chromedriver_path else Service()

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
    from pages.login_page import LoginPage

    login_page = LoginPage(driver)
    login_page.login("user", "12345")
    driver.get(base_url)
    return driver
