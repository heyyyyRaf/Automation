import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://digicoop-sit.traxionpay.com/signin")

    email_input = page.get_by_role("textbox", name="your@email.com")
    expect(email_input).to_be_visible()
    email_input.fill("blaserna+digicoop@traxiontech.net")

    password_input = page.get_by_role("textbox", name="your password")
    expect(password_input).to_be_visible()
    password_input.fill("Traxion123!")

    sign_in_btn = page.get_by_role("button", name="Sign in")
    expect(sign_in_btn).to_be_enabled()
    sign_in_btn.click()

    page.wait_for_load_state("networkidle")

    deposits_btn = page.get_by_role("link", name="Deposits")
    expect(deposits_btn).to_be_visible()
    deposits_btn.click()

    page.wait_for_load_state("networkidle")

    member_list = page.get_by_role("link", name="Member List")
    expect(member_list).to_be_visible()
    member_list.click()

    page.wait_for_timeout(1000)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
