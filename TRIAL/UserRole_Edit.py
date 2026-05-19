import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=800)
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://digicoop-sit.traxionpay.com/signin")
    page.get_by_role("textbox", name="your@email.com").click()
    page.get_by_role("textbox", name="your@email.com").fill("blaserna+digicoop@traxiontech.net")
    page.get_by_role("textbox", name="your password").click()
    page.get_by_role("textbox", name="your password").fill("Traxion123!")
    page.get_by_role("button", name="Sign in").click()
    page.get_by_role("link", name="User Roles").click()
    page.get_by_role("link", name="Edit").first.click()
    page.get_by_text("×").nth(1).click()
    page.get_by_role("button", name="Save Changes").click()
    page.locator(".form-colorinput-color").first.click()
    page.locator("tr:nth-child(3) > td:nth-child(2) > .form-colorinput > .form-colorinput-color").click()
    page.get_by_role("button", name="Save Changes").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
