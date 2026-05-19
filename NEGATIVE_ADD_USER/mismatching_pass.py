import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://bibo-sit.traxionpay.com/signin")
    page.get_by_role("textbox", name="your@email.com").click()
    page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
    page.get_by_role("textbox", name="your@email.com").press("Tab")
    page.get_by_role("textbox", name="your password").fill("Traxion123!")
    page.get_by_role("button", name="Sign in").click()
    page.get_by_role("link", name="Users").click()
    page.get_by_role("link", name="Add New User").click()
    page.get_by_role("textbox", name="First Name *").click()
    page.get_by_role("textbox", name="First Name *").fill("Lebron")
    page.get_by_role("textbox", name="Last Name *").click()
    page.get_by_role("textbox", name="Last Name *").fill("James")
    page.get_by_role("textbox", name="Email Address *").click()
    page.get_by_role("textbox", name="Email Address *").fill("respinosa@traxiontech.net")
    page.get_by_role("textbox", name="10 digits starting with 9 (e.").click()
    page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill("9878787878")
    page.get_by_role("textbox", name="Password *").click()
    page.get_by_role("textbox", name="Password *").fill("Traxion123!")
    page.get_by_role("textbox", name="Minimum 8 characters required").click()
    page.get_by_role("textbox", name="Minimum 8 characters required").fill("traxion12345!")
    page.get_by_role("textbox", name="MPIN *", exact=True).click()
    page.get_by_role("textbox", name="MPIN *", exact=True).fill("231895")
    page.get_by_role("textbox", name="Confirm MPIN *").click()
    page.get_by_role("textbox", name="Confirm MPIN *").fill("231895")
    page.get_by_label("User Role *").select_option("192")
    page.get_by_role("button", name="Add user").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
