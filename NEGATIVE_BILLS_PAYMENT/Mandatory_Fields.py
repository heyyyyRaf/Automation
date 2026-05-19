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
    page.get_by_role("link", name="Bills Payment").click()
    page.get_by_role("textbox", name="Search Billers").click()
    page.get_by_role("textbox", name="Search Billers").fill("barangka")
    page.get_by_role("button", name="Search").click()
    page.get_by_role("link", name="Barangka Credit Cooperative").click()
    page.locator("input[name=\"contact_number\"]").click()
    page.locator("input[name=\"contact_number\"]").fill("09123456789")
    page.locator("input[name=\"loan\"]").click()
    page.locator("input[name=\"loan\"]").fill("Boss Atan")
    page.locator("input[name=\"share_capital\"]").click()
    page.locator("input[name=\"share_capital\"]").fill("500")
    page.get_by_role("spinbutton").click()
    page.get_by_role("spinbutton").fill("500")
    page.get_by_role("link", name="Proceed").click()
    page.get_by_role("link", name="Proceed").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)