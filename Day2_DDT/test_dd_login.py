import pytest
from playwright.sync_api import expect, Page

login_test_data = [
    ("durgeshtesting@gmail.com", "durgeshtesting", "valid"),
    ("invaliduser@example.com", "testingdurgesh", "invalid"),
    ("", "", "invalid"),
]


@pytest.mark.parametrize("email, password,validity", login_test_data)
def test_login_data_driven(email, password, validity, page: Page):
    page.goto("https://demowebshop.tricentis.com/")
    page.get_by_text("Log in").click()
    page.locator("#Email").fill(email)
    page.locator("#Password").fill(password)
    page.locator("#RememberMe").click()
    page.locator("input.button-1.login-button").click()

    # Validation
    if validity == "valid":
        logout_link = page.locator("a[href='/logout']")
        expect(logout_link).to_be_visible(timeout=3000)
    else:
        error_message=page.locator(".validation-summary-errors")
        expect(error_message).to_be_visible(timeout=5000)
        expect(page).to_have_url("https://demowebshop.tricentis.com/login")
