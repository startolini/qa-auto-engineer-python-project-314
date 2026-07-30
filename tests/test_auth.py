import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@pytest.mark.smoke
def test_login_successful(driver, login_url, base_url):
    login_page = LoginPage(driver)
    login_page.open(login_url)
    login_page.login("user", "password")

    assert driver.current_url == base_url + "/#/", (
        "Should redirect to dashboard after login"
    )
    assert driver.title == "Task manager", "Page title should be 'Task manager'"

    dashboard = DashboardPage(driver)
    assert dashboard.get_title_text() == "Welcome to the administration", (
        "Dashboard header should be visible after login"
    )
    assert dashboard.get_welcome_card_text() == "Lorem ipsum sic dolor amet...", (
        "Dashboard welcome card should be visible after login"
    )
    assert dashboard.profile_button_visible(), (
        "Profile button should be visible after login"
    )


@pytest.mark.smoke
def test_logout_successful(dashboard_page):
    dashboard_page.logout()

    assert dashboard_page.profile_button_not_visible(), (
        "Profile button should not be visible after logout"
    )
