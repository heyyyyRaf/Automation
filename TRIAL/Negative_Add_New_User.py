import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://digicoop-sit.traxionpay.com/signin")
    page.get_by_role("textbox", name="your@email.com").click()
    page.get_by_role("textbox", name="your@email.com").fill("blaserna+digicoop@traxiontech.net")
    page.get_by_role("textbox", name="your@email.com").press("Tab")
    page.get_by_role("textbox", name="your password").fill("Traxion123!")
    page.get_by_role("button", name="Sign in").click()
    page.get_by_role("link", name="Users").click()
    page.get_by_role("link", name="Add New User").click()
    page.get_by_role("textbox", name="First Name *").click()
    page.get_by_role("textbox", name="First Name *").fill("Lebron")
    page.get_by_role("textbox", name="First Name *").press("Tab")
    page.get_by_role("textbox", name="Middle Name").fill("Jordan")
    page.get_by_role("textbox", name="Middle Name").press("Tab")
    page.get_by_role("textbox", name="Last Name *").fill("Bronny")
    page.get_by_role("textbox", name="Last Name *").press("Tab")
    page.get_by_role("textbox", name="Email Address *").fill("LebronJordanBronny@gmail.com")
    page.get_by_role("textbox", name="Email Address *").press("Tab")
    page.get_by_role("textbox", name="10 digits starting with 9 (e.").press("PageUp")
    page.get_by_role("textbox", name="10 digits starting with 9 (e.").press("ArrowUp")
    page.get_by_role("textbox", name="10 digits starting with 9 (e.").press("Home")
    page.get_by_role("textbox", name="10 digits starting with 9 (e.").press("NumLock")
    page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill("9559564648")
    page.get_by_role("textbox", name="Password *").click()
    page.get_by_role("textbox", name="Password *").fill("Ta")
    page.get_by_role("textbox", name="Password *").click()
    page.get_by_role("textbox", name="Password *").fill("Traxion123!")
    page.get_by_role("textbox", name="Password *").press("Tab")
    page.get_by_role("textbox", name="Minimum 8 characters required").fill("Traxion123!")
    page.get_by_role("textbox", name="MPIN *", exact=True).click()
    page.get_by_role("textbox", name="MPIN *", exact=True).fill("231895")
    page.get_by_role("textbox", name="MPIN *", exact=True).press("Tab")
    page.get_by_role("textbox", name="Confirm MPIN *").fill("231895")
    page.get_by_label("User Role *").select_option("296")
    page.get_by_role("button", name="Add user").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
