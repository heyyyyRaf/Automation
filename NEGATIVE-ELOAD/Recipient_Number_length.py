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
    page.get_by_role("textbox", name="your password").press("Enter")
    page.get_by_role("button", name="Sign in").click()
    page.get_by_role("link", name="E-Load").click()
    page.get_by_role("tab", name="Non-Telco").click()
    page.locator("div:nth-child(6) > div:nth-child(3) > .card > .card-body").click()
    page.get_by_role("textbox", name="Enter recipient's number...").click()
    page.get_by_role("textbox", name="Enter recipient's number...").fill("659519494959529529498498496525929598498492952629529849848452959859849849529525295959898989849989")
    page.get_by_role("button", name="Proceed").click()
    page.locator("div").filter(has_text=re.compile(r"^EASYTRIP 400$")).click()
    page.get_by_role("link", name="Next").click()
    page.get_by_role("textbox", name="Enter MPIN or Password").click()
    page.get_by_role("textbox", name="Enter MPIN or Password").fill("Traxion123!")
    page.get_by_role("button", name="Submit").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)