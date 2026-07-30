import pytest
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_login_successful(driver, login_url, base_url):
    login_page = LoginPage(driver)
    login_page.open(login_url)
    login_page.login("user", "password")

    assert driver.current_url == base_url + "/#/", (
        "Should redirect to dashboard after login"
    )


@pytest.mark.smoke
def test_logout_successful(dashboard_page):
    dashboard_page.logout()

    assert dashboard_page.profile_button_not_visible(), (
        "Profile button should not be visible after logout"
    )
