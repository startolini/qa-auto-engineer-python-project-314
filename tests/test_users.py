import pytest


@pytest.mark.smoke
def test_create_user(users_page):
    users_page.click_create()
    assert users_page.check_user_inputs_visible(), (
        "Create user form inputs should be visible"
    )

    users_page.create_user(
        first_name="test", email="test@test.com", last_name="test1234"
    )
    users_page.menu.open_users()

    assert users_page.check_user_in_table(
        first_name="test", email="test@test.com", last_name="test1234"
    )


@pytest.mark.regression
def test_users_header_visible(users_page):
    assert users_page.check_table_header_visible(), "Table header should be visible"


@pytest.mark.regression
def test_all_ids_visible(users_page):
    assert users_page.check_all_ids_visible(8), "All ids should be visible"


@pytest.mark.smoke
def test_open_user_card(users_page):
    actual_email, actual_first_name, actual_last_name = users_page.open_user_details(
        email="peter@outlook.com"
    )

    assert actual_email == "peter@outlook.com"
    assert actual_first_name == "Peter"
    assert actual_last_name == "Brown"


@pytest.mark.smoke
def test_change_user_card(users_page):
    initial_email = "peter@outlook.com"
    invalid_email = "peter.gmail.com"
    changed_email = "peter@gmail.com"

    users_page.open_user_details(email=initial_email)

    users_page.change_user_email(invalid_email)
    assert users_page.get_validation_error_text() == "Incorrect email format", (
        "Invalid email should be rejected with a validation error"
    )

    users_page.change_user_email(changed_email)

    assert users_page.check_user_in_table(
        first_name="Peter", email=changed_email, last_name="Brown"
    )


@pytest.mark.smoke
def test_delete_user(users_page):
    users_page.select_row_by_value("jane@gmail.com")
    users_page.click_delete_btn()

    assert users_page.email_not_in_table(email="jane@gmail.com"), (
        "Deleted email should not be in the table"
    )


@pytest.mark.regression
def test_delete_all_users(users_page):
    users_page.select_all_rows()
    users_page.click_delete_btn()

    assert users_page.no_items_logo_visible(), "Users list should be empty"
