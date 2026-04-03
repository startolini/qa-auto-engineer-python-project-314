import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.users_page import UsersPage
from pages.task_statuses_page import TaskStatusesPage
from pages.labels_page import LabelsPage


@pytest.mark.smoke
def test_login_successfull(driver, login_url):

    login_page = LoginPage(driver)
    login_page.open(login_url)
    login_page.login("user", "password")

    assert login_page.submit_button_not_visile(), (
        "Submit button should not be visible after login"
    )


@pytest.mark.smoke
def test_logout_successfull(login_user):
    dashboard_page = DashboardPage(login_user)
    dashboard_page.logout()

    assert dashboard_page.profile_button_not_visile(), (
        "Profile button should not be visible after logout"
    )


@pytest.mark.smoke
def test_create_user(login_user):
    page = DashboardPage(login_user)
    page.menu.open_users()
    users = UsersPage(login_user)
    users.creat_user(first_name="test", email="test@test.com", last_name="test1234")
    page.menu.open_users()
    assert users.check_user_in_table(
        first_name="test", email="test@test.com", last_name="test1234"
    )


@pytest.mark.regression
def test_users_header_visible(login_user):
    page = DashboardPage(login_user)
    page.menu.open_users()
    users = UsersPage(login_user)
    assert users.check_table_header_visible(), "Table header should be visible"


@pytest.mark.regression
def test_all_ids_visible(login_user):
    page = DashboardPage(login_user)
    page.menu.open_users()
    users = UsersPage(login_user)
    assert users.check_all_ids_visible(8), "All ids should be visible"


@pytest.mark.smoke
def test_open_user_card(login_user):
    page = DashboardPage(login_user)
    page.menu.open_users()
    users = UsersPage(login_user)

    actual_email, actual_first_name, actual_last_name = users.open_user_details(
        email="peter@outlook.com"
    )

    assert actual_email == "peter@outlook.com"
    assert actual_first_name == "Peter"
    assert actual_last_name == "Brown"


@pytest.mark.smoke
def test_change_user_card(login_user):
    page = DashboardPage(login_user)
    page.menu.open_users()
    users = UsersPage(login_user)

    initial_email = "peter@outlook.com"
    changed_email = "peter@gmail.com"

    users.open_user_details(email=initial_email)
    users.change_user_email(changed_email)

    assert users.check_user_in_table(
        first_name="Peter", email=changed_email, last_name="Brown"
    )


@pytest.mark.smoke
def test_delete_user(login_user):
    page = DashboardPage(login_user)
    page.menu.open_users()
    users = UsersPage(login_user)

    users.select_user_by_email("jane@gmail.com")
    users.click_delete_btn()

    assert users.email_not_in_table(email="jane@gmail.com"), (
        "Deleted email should not be in the table"
    )


@pytest.mark.regression
def test_delete_all_users(login_user):
    page = DashboardPage(login_user)
    page.menu.open_users()
    users = UsersPage(login_user)

    users.select_all_users()
    users.click_delete_btn()

    assert users.no_users_logo_visible(), "Deleted email should not be in the table"


@pytest.mark.smoke
def test_status_inputs_visible(login_user):
    page = DashboardPage(login_user)
    page.menu.open_task_statuses()
    statuses = TaskStatusesPage(login_user)
    statuses.click_create_status()

    assert statuses.check_status_inputs_visible(), "Inputs should be visible"


@pytest.mark.smoke
def test_status_creation(login_user):
    page = DashboardPage(login_user)
    page.menu.open_task_statuses()
    statuses = TaskStatusesPage(login_user)
    statuses.click_create_status()

    statuses.create_status(name="test", slug="test1234")
    page.menu.open_task_statuses()

    a, b = statuses.get_values_from_table(name="test", slug="test1234")

    assert a == "test" and b == "test1234", (
        "Status name and slug should be visible in the table"
    )


@pytest.mark.smoke
def test_status_editing(login_user):
    page = DashboardPage(login_user)
    page.menu.open_task_statuses()
    statuses = TaskStatusesPage(login_user)
    statuses.open_status_details(name="Published")

    statuses.create_status(name="test", slug="test1234")
    a, b = statuses.get_values_from_table(name="test", slug="test1234")

    assert a == "test" and b == "test1234", (
        "Status name and slug should be visible in the table"
    )


@pytest.mark.smoke
def test_statuses_texts(login_user):
    STATUSES = ["Draft", "To Review", "To Be Fixed", "To Publish", "Published"]
    page = DashboardPage(login_user)
    page.menu.open_task_statuses()
    statuses = TaskStatusesPage(login_user)

    for status in STATUSES:
        assert status in statuses.get_statuses_text(), (
            f"Status '{status}' should be visible in the table"
        )


@pytest.mark.smoke
def test_delete_all_statuses(login_user):
    page = DashboardPage(login_user)
    page.menu.open_task_statuses()
    statuses = TaskStatusesPage(login_user)

    statuses.select_all_statuses()
    statuses.click_delete_btn()

    assert statuses.no_statuses_logo_visible(), "No tasks statuses should be visible"


@pytest.mark.smoke
def test_label_input_visible(login_user):
    page = DashboardPage(login_user)
    page.menu.open_labels()
    labels = LabelsPage(login_user)

    labels.click_create_label()

    assert labels.check_label_input_visible(), "Label input should be visible"


@pytest.mark.smoke
def test_create_new_label(login_user):
    page = DashboardPage(login_user)
    page.menu.open_labels()
    labels = LabelsPage(login_user)

    labels.click_create_label()
    labels.create_label(name="test")
    page.menu.open_labels()

    assert "test" in labels.get_value_from_table("test"), (
        "Label should be in the labels list"
    )


@pytest.mark.smoke
def test_check_all_labels(login_user):
    LABELS = ["bug", "feature", "enhancement", "task", "critical"]
    page = DashboardPage(login_user)
    page.menu.open_labels()
    labels = LabelsPage(login_user)

    for label in LABELS:
        assert label in labels.get_labels_text(), (
            f"Label '{label}' should be visible in the table"
        )


@pytest.mark.smoke
def test_label_editing(login_user):
    page = DashboardPage(login_user)
    page.menu.open_labels()
    labels = LabelsPage(login_user)
    labels.open_label_details(name="bug")
    labels.create_label(name="test")

    a = labels.get_value_from_table(name="test")

    assert a == "test"


@pytest.mark.one
def test_delete_label(login_user):
    page = DashboardPage(login_user)
    page.menu.open_labels()
    labels = LabelsPage(login_user)
    labels.select_label_by_name(name="task")
    labels.click_delete_btn()

    assert "task" not in labels.get_labels_text(), (
        "Deleted label should not be visible in the table"
    )
