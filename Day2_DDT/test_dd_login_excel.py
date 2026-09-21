"""
openpyxl
   pip install openpyxl

"""

import openpyxl
import pytest
from playwright.sync_api import expect, Page

login_data = []  # storing data in empty list
workbook = openpyxl.load_workbook("testdata/data.xlsx")
sheet = workbook.active  # or worksheet ["sheetname"]

# reading data from xlsx using for loop
for row in sheet.iter_rows(min_row=2, values_only=True):
    email, password, validity = row
    login_data.append((str(email or ""), str(password or ""), str(validity or "")))
    workbook.close()


@pytest.mark.parametrize("email, password, validity", login_data)
def test_login_data_driven_excel_file(email, password, validity, page: Page):
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
