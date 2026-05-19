import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://digicoop-sit.traxionpay.com/signin")

    email = page.get_by_role("textbox", name="your@email.com")
    expect(email).to_be_visible()
    email.fill("blaserna+digicoop@traxiontech.net")

    password = page.get_by_role("textbox", name="your password")
    expect(password).to_be_visible()
    password.fill("Traxion123!")

    sign_in = page.get_by_role("button", name="Sign in")
    expect(sign_in).to_be_enabled()
    sign_in.click()

    page.wait_for_load_state("networkidle")

    users = page.get_by_role("link", name="Users")
    expect(users).to_be_visible()
    users.click()

    add_user = page.get_by_role("link", name="Add New User")
    expect(add_user).to_be_visible()
    add_user.click()

    first_name = page.get_by_role("textbox", name="First Name *")
    expect(first_name).to_be_visible()

    first_name.fill("Lebron")
    page.get_by_role("textbox", name="Last Name *").fill("Carry")
    page.get_by_role("textbox", name="Email Address *").fill("lebroncarry_test@gmail.com")
    page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill("9888755665")
    page.get_by_role("textbox", name="Password *").fill("Traxion123!")
    page.get_by_role("textbox", name="Minimum 8 characters required").fill("Traxion123!")
    page.get_by_role("textbox", name="MPIN *", exact=True).fill("231895")
    page.get_by_role("textbox", name="Confirm MPIN *").fill("231895")

    page.get_by_label("User Role *").select_option("296")

    submit = page.get_by_role("button", name="Add user")
    expect(submit).to_be_enabled()
    submit.click()

    page.wait_for_load_state("networkidle")

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)