import pytest


@pytest.mark.smoke
def test_task_creation_form_visible(tasks_page):
    """Task creation form shows required fields: title, assignee, status"""
    tasks_page.click_create_task()

    assert tasks_page.check_task_form_visible(), (
        "Title, assignee and status fields should be visible"
    )


@pytest.mark.smoke
def test_create_task(tasks_page):
    """Create a task and verify it appears in the chosen column"""
    tasks_page.click_create_task()
    tasks_page.create_task(
        title="New test task",
        assignee="john@google.com",
        status="To Review",
        content="Created by autotest",
    )

    # После сохранения приложение открывает страницу созданной задачи —
    # возвращаемся на доску
    tasks_page.menu.open_tasks()

    assert tasks_page.card_in_column("New test task", "To Review"), (
        "Created task should appear in the 'To Review' column"
    )


@pytest.mark.smoke
def test_view_all_tasks(tasks_page):
    """Cards in every column are loaded with their key fields"""
    tasks_page.wait_for_cards_loaded()

    columns = tasks_page.get_column_names()
    assert columns, "Board should have at least one column"

    total_cards = 0
    for column in columns:
        for card_info in tasks_page.get_card_info_in_column(column):
            total_cards += 1
            assert card_info["title"], f"Card in '{column}' should have title"
            assert card_info["description"], (
                f"Card in '{column}' should have description"
            )
            assert card_info["index"], f"Card in '{column}' should have index"
            assert card_info["id"], f"Card in '{column}' should have id"

    assert total_cards > 0, "Board should have at least one task card"
    assert total_cards == tasks_page.get_board_card_count(), (
        "Cards in columns should account for all cards on the board"
    )


@pytest.mark.smoke
def test_edit_task(tasks_page):
    """Edit an existing task and verify changes are displayed"""
    tasks_page.wait_for_cards_loaded()

    tasks_page.open_card_editing("Task 2")
    tasks_page.change_task_title("Task 2 edited")
    tasks_page.save_task()

    assert tasks_page.card_in_column("Task 2 edited", "To Review"), (
        "Edited title should be displayed on the board"
    )


@pytest.mark.smoke
def test_move_task_between_columns(tasks_page):
    """Move a task to another column by changing its status"""
    tasks_page.wait_for_cards_loaded()

    tasks_page.open_card_editing("Task 11")
    tasks_page.change_task_status("Published")
    tasks_page.save_task()

    assert tasks_page.card_in_column("Task 11", "Published"), (
        "Task should be displayed in the 'Published' column"
    )
    assert tasks_page.card_not_in_column("Task 11", "Draft"), (
        "Task should no longer be in the 'Draft' column"
    )


@pytest.mark.smoke
def test_delete_task(tasks_page):
    """Delete a task and verify it disappears from the board"""
    tasks_page.wait_for_cards_loaded()

    tasks_page.open_card_editing("Task 5")
    tasks_page.delete_task()

    tasks_page.wait_for_cards_loaded()
    assert tasks_page.card_not_on_board("Task 5"), (
        "Deleted task should not be on the board"
    )


@pytest.mark.smoke
def test_task_filters(tasks_page):
    """Filters by status, assignee and label update the board"""
    tasks_page.wait_for_cards_loaded()
    total = tasks_page.get_board_card_count()

    # По статусу: на доске остаются только карточки колонки Draft
    tasks_page.apply_filter("status_id", "Draft")
    filtered = tasks_page.wait_for_card_count_change(total)
    assert 0 < filtered < total, "Status filter should reduce the card count"
    assert filtered == tasks_page.get_card_count_in_draft(), (
        "With the Draft filter all cards should be in the Draft column"
    )
    tasks_page.clear_filter("status_id")
    assert tasks_page.wait_for_card_count_change(filtered) == total

    # По исполнителю
    tasks_page.apply_filter("assignee_id", "john@google.com")
    filtered = tasks_page.wait_for_card_count_change(total)
    assert 0 < filtered < total, "Assignee filter should reduce the card count"
    tasks_page.clear_filter("assignee_id")
    assert tasks_page.wait_for_card_count_change(filtered) == total

    # По метке
    tasks_page.apply_filter("label_id", "bug")
    filtered = tasks_page.wait_for_card_count_change(total)
    assert 0 < filtered < total, "Label filter should reduce the card count"
    tasks_page.clear_filter("label_id")
    assert tasks_page.wait_for_card_count_change(filtered) == total


@pytest.mark.regression
@pytest.mark.window_size(875, 612)
def test_scroll_to_specific_card(tasks_page):
    """The last card in the Draft column is visible after scrolling to it"""
    tasks_page.wait_for_cards_loaded()

    cards = tasks_page.get_all_cards_in_draft()
    assert cards, "Draft column should contain at least one card"

    last_card = cards[-1]
    tasks_page.scroll_to_card(last_card)

    assert last_card.is_displayed(), "Card should be visible after scrolling"
