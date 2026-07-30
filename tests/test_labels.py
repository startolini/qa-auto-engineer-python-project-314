import pytest

DEFAULT_LABELS = ["bug", "feature", "enhancement", "task", "critical"]


@pytest.mark.smoke
def test_label_input_visible(labels_page):
    labels_page.click_create()

    assert labels_page.check_label_input_visible(), "Label input should be visible"


@pytest.mark.smoke
def test_create_new_label(labels_page):
    labels_page.click_create()
    labels_page.create_label(name="test")
    labels_page.menu.open_labels()

    assert labels_page.get_value_from_table("test") == "test", (
        "Label should be in the labels list"
    )


@pytest.mark.smoke
def test_check_all_labels(labels_page):
    visible_labels = labels_page.get_labels_text()

    for label in DEFAULT_LABELS:
        assert label in visible_labels, (
            f"Label '{label}' should be visible in the table"
        )


@pytest.mark.smoke
def test_label_editing(labels_page):
    labels_page.open_label_details(name="bug")
    labels_page.create_label(name="test")

    assert labels_page.get_value_from_table(name="test") == "test"


@pytest.mark.smoke
def test_delete_label(labels_page):
    labels_page.select_row_by_value("task")
    labels_page.click_delete_btn()

    assert labels_page.label_not_in_table("task"), (
        "Deleted label should not be visible in the table"
    )


@pytest.mark.regression
def test_delete_all_labels(labels_page):
    labels_page.select_all_rows()
    labels_page.click_delete_btn()

    assert labels_page.no_items_logo_visible(), "No labels should be visible"
