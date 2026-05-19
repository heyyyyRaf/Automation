import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rbpay-sit.traxionpay.com/signin")
    page.get_by_role("textbox", name="your@email.com").click()
    page.get_by_role("textbox", name="your@email.com").fill("blaserna+rbpay@traxiontech.net")
    page.get_by_role("textbox", name="your@email.com").press("Tab")
    page.get_by_role("textbox", name="your password").fill("Traxion123!")
    page.get_by_role("button", name="Sign in").click()
    page.get_by_role("link", name="Withdrawals").click()
    page.get_by_role("link", name="Direct Fund Transfer").click()
    page.get_by_role("textbox", name="Mobile/Account Number/Wallet").click()
    page.get_by_role("textbox", name="Mobile/Account Number/Wallet").fill("1011009517501446")
    page.get_by_role("textbox", name="Account Name").click()
    page.get_by_placeholder("0.00").click()
    page.get_by_placeholder("0.00").press("Clear")
    page.get_by_placeholder("0.00").press("NumLock")
    page.get_by_placeholder("0.00").fill("500")
    page.get_by_role("radio", name="Password").check()
    page.get_by_role("textbox", name="form-control required field").click()
    page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
    page.get_by_role("button", name="Transfer Funds").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
