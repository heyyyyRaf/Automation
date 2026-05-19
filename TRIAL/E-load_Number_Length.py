import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=800)  # 👈 slows down actions (800ms)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://digicoop-sit.traxionpay.com/signin")

    page.get_by_role("textbox", name="your@email.com").click()
    page.get_by_role("textbox", name="your@email.com").fill("blaserna+digicoop@traxiontech.net")
    page.get_by_role("textbox", name="your@email.com").press("Tab")
    page.get_by_role("textbox", name="your password").fill("Traxion123!")
    page.get_by_role("button", name="Sign in").click()

    page.get_by_role("link", name="E-Load").click()
    page.get_by_role("img", name="TM").click()
    page.get_by_role("textbox", name="Enter recipient's number...").click()
    page.get_by_role("textbox", name="Enter recipient's number...").fill("09123567894561")

    page.get_by_text("Telco Non-Telco TM Change").click()
    page.get_by_role("button", name="Proceed").click()
    page.get_by_text("Touch Mobile Amax 25").click()
    page.get_by_role("link", name="Next").click()

    page.locator("#remoteModal").click()
    page.get_by_role("button", name="Submit").click()

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)