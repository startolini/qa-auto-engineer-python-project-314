import pytest

DEFAULT_STATUSES = ["Draft", "To Review", "To Be Fixed", "To Publish", "Published"]


@pytest.mark.smoke
def test_status_inputs_visible(task_statuses_page):
    task_statuses_page.click_create()

    assert task_statuses_page.check_status_inputs_visible(), "Inputs should be visible"


@pytest.mark.smoke
def test_status_creation(task_statuses_page):
    task_statuses_page.click_create()
    task_statuses_page.create_status(name="test", slug="test1234")
    task_statuses_page.menu.open_task_statuses()

    name, slug = task_statuses_page.get_values_from_table(name="test", slug="test1234")

    assert name == "test" and slug == "test1234", (
        "Status name and slug should be visible in the table"
    )


@pytest.mark.smoke
def test_status_editing(task_statuses_page):
    task_statuses_page.open_status_details(name="Published")
    task_statuses_page.create_status(name="test", slug="test1234")

    name, slug = task_statuses_page.get_values_from_table(name="test", slug="test1234")

    assert name == "test" and slug == "test1234", (
        "Status name and slug should be visible in the table"
    )


@pytest.mark.smoke
def test_statuses_texts(task_statuses_page):
    visible_statuses = task_statuses_page.get_statuses_text()

    for status in DEFAULT_STATUSES:
        assert status in visible_statuses, (
            f"Status '{status}' should be visible in the table"
        )


@pytest.mark.smoke
def test_delete_status(task_statuses_page):
    task_statuses_page.select_row_by_value("Draft")
    task_statuses_page.click_delete_btn()

    assert task_statuses_page.status_not_in_table("Draft"), (
        "Deleted status should not be in the table"
    )


@pytest.mark.smoke
def test_delete_all_statuses(task_statuses_page):
    task_statuses_page.select_all_rows()
    task_statuses_page.click_delete_btn()

    assert task_statuses_page.no_items_logo_visible(), (
        "No task statuses should be visible"
    )
