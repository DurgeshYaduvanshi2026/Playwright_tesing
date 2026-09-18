import pytest
from playwright.sync_api import expect, Page
import csv

login_csv_data = []  # empty list

# Read CSV file
csvfile = open("testdata/data.csv", newline="", encoding="utf-8")
reader = csv.DictReader(csvfile, delimiter="\t")
for row in reader:
    login_csv_data.append((row["email"], row["password"], row["validity"]))


@pytest.mark.parametrize("email, password,validity", login_csv_data)
def test_login_data_driven_csv(email, password, validity, page: Page):
    page.goto("https://demowebshop.tricentis.com/")

    # Fill the login data
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
        error_message = page.locator(
            ".validation-summary-errors, .field-validation-error"
        ).first
        expect(error_message).to_be_visible(timeout=5000)  # Checking error message
        expect(page).to_have_url(
            "https://demowebshop.tricentis.com/login"
        )  # Checking same login page
