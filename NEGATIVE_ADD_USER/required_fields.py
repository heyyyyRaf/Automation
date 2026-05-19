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
    page.get_by_role("textbox", name="First Name *").click()
    page.get_by_role("textbox", name="First Name *").fill("Traxion")
    page.get_by_role("button", name="Add user").click()
    page.get_by_role("button", name="Add user").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
