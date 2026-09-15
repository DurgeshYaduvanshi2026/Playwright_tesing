import pytest

from playwright.sync_api import expect, Playwright, Page

search_items = ["laptop", "Gift card", "smartphone", "camera"]


@pytest.mark.parametrize("item", search_items)
def test_search_item(item, page: Page):
    # Enter the url
    page.goto("https://demowebshop.tricentis.com/")
    # Enter the value in search field
    page.locator("#small-searchterms").fill(item)
    # Click on Search button after entering the product
    page.locator("input.button-1.search-box-button").click()

    # Assertion
    first_result = page.locator("h2 a").nth(0)
    expect(first_result).to_contain_text(item, ignore_case=True)
