import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=800)
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://digicoop-sit.traxionpay.com/signin")
    page.locator(".mb-3").first.click()
    page.get_by_role("textbox", name="your@email.com").click()
    page.get_by_role("textbox", name="your@email.com").fill("blaserna+digicoop@traxiontech.net")
    page.get_by_role("textbox", name="your@email.com").press("Tab")
    page.get_by_role("textbox", name="your password").fill("Traxion123!")
    page.get_by_role("button", name="Sign in").click()
    page.get_by_role("link", name="Member List").click()
    page.get_by_role("link", name="Pending Members").click()
    page.get_by_role("link", name="Resend Code").first.click()
    page.get_by_role("button", name="Yes, Resend").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
