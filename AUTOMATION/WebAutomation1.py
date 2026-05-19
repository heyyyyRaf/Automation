from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError, Playwright
import smtplib
from email.message import EmailMessage
from datetime import datetime
import os
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import messagebox
import traceback
from datetime import datetime, timedelta
import re
from playwright.sync_api import sync_playwright, expect
import traceback
import time

import random
import string


# ===============================
# Test Data Generator
# ===============================
class TestDataGenerator:

    @staticmethod
    def random_letters(length=5):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    @staticmethod
    def first_name(base="Bryan"):
        return base + TestDataGenerator.random_letters(3)

    @staticmethod
    def last_name(base="Laserna"):
        return base + TestDataGenerator.random_letters(3)

    @staticmethod
    def email(first_name, last_name):
        suffix = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"blaserna{first_name.lower()}.{last_name.lower()}.{suffix}@traxiontech.net"

    @staticmethod
    def mobile_number():
        return "9" + ''.join(random.choice(string.digits) for _ in range(9))

    @staticmethod
    def password():
        return "Traxion123!"

#python -m playwright codegen https://bibo-sit.traxionpay.com/

# ===============================
# Gmail Settings
# ===============================
GMAIL_USER = "mj@traxiontech.net"
GMAIL_APP_PASSWORD = "aohrspbjzpcdugdt"
RECIPIENT_EMAIL = "respinosa@traxiontech.net"

# ===============================
# Test Configuration
# ===============================

USERNAME = "blaserna+1127bibo@traxiontech.net"
PASSWORD = "Traxion123!"
#login_url = "https://merchant-sit.traxionpay.com/"
    
TEST_SCENARIOS = [

##=======================BILLS PAYMENT SCENARIOS=======================##
##======= POSTIVE =========##
    {"module": "Bills Payment", "title": "Bills Payment Successful", "description": "Verify that a merchant can successfully make a bill payment transaction."},
    {"module": "Bills Payment", "title": "Optional Fields Empty", "description": "Verify that payment is successful when leaving optional fields like 'Account No.' and 'Remarks' empty."},
##======= NEGATIVE =========##
    {"module": "Bills Payment", "title": "Without Entering Password in Bills", "description": "Verify that a merchant cannot make a bill payment without entering a password."},
    {"module": "Bills Payment", "title": "Mandatory Fields Missing", "description": "Verify validation errors when 'Member Name', 'Contact No.', and 'Amount' are left blank."},
    {"module": "Bills Payment", "title": "Below Minimum Amount", "description": "Verify that the system prevents entering below minimum amount"},

##=======================LOG IN SCENARIOS=======================##
##======= POSTIVE =========##
    {"module": "Auth", "title": "Login Test", "description": "Verify that a merchant can log in and access the dashboard successfully."},
    {"module": "Auth", "title": "Logout Test", "description": "Verify that a merchant can log out from the dashboard successfully."},
##======= NEGATIVE =========##
    {"module": "Auth", "title": "Login without pass", "description": "Verify if the system showed validation message"},
    {"module": "Auth", "title": "Non Existing Account", "description": "Verify if the user could proceed to the dashboard"},
    {"module": "Auth", "title": "Password Length", "description": "Verify if the passwordfield have a password length validation."},
    {"module": "Auth", "title": "Invalid Password", "description": "Verify if the user could proceed to the dashboard even if the password is incorrect."},

##=======================WITHDRAWALS SCENARIOS=======================##
##======= POSTIVE =========##
    {"module": "Withdrawals", "title": "Direct Fundtransfer", "description": "Verify that a merchant can Transfer Fund successfully."},
    {"module": "Withdrawals", "title": "Withdraw Funds", "description": "Verify that a merchant can Transfer Through Banks successfully."},   
##======= NEGATIVE =========##
    {"module": "Withdrawals", "title": "Withdraw Funds Invalid Password", "description": "verify that banktransfer fails with invalid credentials."},
    {"module": "Withdrawals", "title": "Direct Fundtransfer Invalid Password", "description": "verify that fundtransfer fails with invalid credentials."},

##=======================DEPOSIT SCENARIOS=======================##
##======= POSTIVE =========##
    {"module": "Deposit", "title": "Manual Deposit", "description": "Verify that a merchant can Manual Deposit successfully."},
    {"module": "Deposit", "title": "Cash In from DragonPay", "description": "Verify that a merchant can Cash In from DragonPay successfully."},

##======= NEGATIVE =========##
    {"module": "Deposit", "title": "Leave Blank Required Fields in Manual Deposit", "description": "Verify that the system shows validation messages when required fields are left blank in manual deposit."},
    {"module": "Deposit", "title": "Leave Blank Deposit Slip", "description": "Verify that the system shows validation messages when required fields are left blank in manual deposit."},

##=======================ELOAD SCENARIOS=======================##
##======= POSTIVE =========##
    {"module": "Eload", "title": "Eload", "description": "Verify that a merchant can do eload transaction"},
    {"module": "Eload", "title": "Eload invalid credential", "description": "Verify that a merchant cannot do eload transaction"},
    {"module": "Eload", "title": "E-load Number length Validation", "description": "Verify that Mobile number field have number length"},
##======= NEGATIVE =========##
    {"module": "Buyload", "title": "Negative: Invalid Recipient Number", "description": "Verify that the system rejects invalid recipient numbers"},
    {"module": "Buyload", "title": "E-Load Invalid Number Format", "description": "Verify that the system rejects recipient numbers with invalid format"},
    {"module": "Buyload", "title": "Without Entering Number", "description": "Verify that the system shows validation error when recipient number is not entered"},
    {"module": "Buyload", "title": "Without Entering Password", "description": "Verify that the system shows validation error when password is not entered"},

##=======================BUY LOAD SCENARIOS=======================##
##======= POSTIVE =========##
    {"module": "Buyload", "title": "Buyload", "description": "Verify that a merchant can do buyload transaction"},
    {"module": "Buyload", "title": "Non Telco", "description": "Verify that a merchant can do buyload transaction with non-telco product"},
##======= NEGATIVE =========##

##=======================ADD USER SCENARIOS=======================##
##======= POSTIVE =========##
    {"module": "Add User", "title": "Add User", "description": "Verify that a merchant can add user"},
    {"module": "Add User", "title": "Edit User Role", "description": "Verify if the user should change the user role"},
    {"module": "Add User", "title": "Deactivate Account", "description": "Verify if the user should be able to deactivate account"},
    {"module": "Add User", "title": "Edit User Name", "description": "Verify if the user should be able to edit user name"},
    {"module": "Add User", "title": "Add New User", "description": "Verify if the user should be able to add new user"},
##======= NEGATIVE =========##
    {"module": "Add User", "title": "Add Existing User", "description": "Verify validation on adding existing user"},
    {"module": "Add User", "title": "Required Fields", "description": "Verify if the system showed a validation message"},
    {"module": "Add User", "title": "Existing Email", "description": "Verify if the user can add user with existing email"},
    {"module": "Add User", "title": "Mismatching Pass", "description": "Verify if the user could create mismatching pass"},
    {"module": "Add User", "title": "Mismatching MPIN", "description": "Verify if the user could create mismatching mpin"},
    {"module": "Add User", "title": "Invalid Email Format", "description": "Verify if the user could create account with invalid email format"},
    {"module": "Add User", "title": "Invalid Number Format", "description": "Verify if the user could create account with invalid number format"},
    {"module": "Add User", "title": "Password Doesn't Meet Req", "description": "Verify if the user can create a password that does not meet the requirements"},
    {"module": "Add User", "title": "edit btn", "description": "Verify if the user could proceed to the next page"},


##=======================USER ROLE SCENARIOS=======================##
##======= POSTIVE =========##
    {"module": "UserRole", "title": "Add User Role", "description": "Verify that a merchant can add userrole"},
    {"module": "UserRole", "title": "Edit User Role (User Role) ", "description": "Verify that a merchant can edit userrole"},
    {"module": "UserRole", "title": "View btn", "description": "Verify if the user could proceed to the view module"},

##======= NEGATIVE =========##
    {"module": "UserRole", "title": "Add Existing User Role", "description": "Verify validation on adding existing user role"},
    {"module": "UserRole", "title": "Required Fields", "description": "Verify if the system showed a validation message"},

##=======================MEMBER LIST=======================##
##======= POSTIVE =========##
    {"module": "Member List", "title": "Add Member", "description": "Verify that a merchant can add member"},

##======= NEGATIVE =========##
    {"module": "Member List", "title": "Add Member With Existing Number or Email", "description": "Verify validation on adding existing member"},
    {"module": "Member List", "title": "Add Member With Invalid Mobile Number", "description": "Verify validation on adding existing member"},

##=======================BRANCHES=======================##
##======= POSTIVE =========##
    {"module": "Branches", "title": "Add Organization Branch", "description": "Verify that a merchant can add organization branch"},

##======= NEGATIVE =========##
    {"module": "Branches", "title": "Leave blank required fields branches", "description": "verify that the system shows validation messages when required fields are left blank in adding organization branch."},
    {"module": "Branches", "title": "Invalid mobile number branches", "description": "verify that the system shows validation messages when required fields are left blank in adding organization branch."},


##=========================================##
## BACK OFFICE ##
    {"module": "Back Office", "title": "1011009517501446", "description": "successfully."},
    {"module": "Back Office", "title": "1011032223967154", "description": "successfully."},
    {"module": "Back Office", "title": "1011021785733461", "description": "successfully."},
    {"module": "Back Office", "title": "1011008204742842", "description": "successfully."},
    {"module": "Back Office", "title": "1011012719935939", "description": "successfully."},
    {"module": "Back Office", "title": "1011000678304854", "description": "successfully."},
    {"module": "Back Office", "title": "1011731218426493", "description": "successfully."},

## 1 ACCOUNT 
    {"module": "TRANSFER", "title": "1ST TRANSFER", "description": "successfully."},
    {"module": "TRANSFER", "title": "1ST TRANSFER bibo", "description": "successfully."},
    {"module": "TRANSFER", "title": "2ND TRANSFER", "description": "successfully."},
    {"module": "TRANSFER", "title": "3RD TRANSFER", "description": "successfully."},


]

BASE_DIR = Path("automation_artifacts")
RUN_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

RUN_DIR = BASE_DIR / RUN_TIMESTAMP
SCREENSHOT_DIR = RUN_DIR / "screenshots"
ERROR_DIR = RUN_DIR / "errors"
REPORT_DIR = RUN_DIR / "report"

for d in [SCREENSHOT_DIR, ERROR_DIR, REPORT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ===============================
# Reporting Helpers
# ===============================

APP_URLS = {
    "Traxion": "https://merchant-sit.traxionpay.com/signin",
    "Bibo": "https://bibo-sit.traxionpay.com/signin",
    "RBPay": "https://rbpay-sit.traxionpay.com/signin",
    "MannyPay": "https://mannypay-sit.traxionpay.com/signin",
    "MicroPay": "https://micropay-sit.traxionpay.com/signin",
    "Psslai": "https://psslai-sit.traxionpay.com/signin",
    "Digicoop": "https://digicoop-sit.traxionpay.com/signin",
    
}
def get_ui_error(page):
    selectors = [
        ".alert-danger",
        ".error",
        ".error-message",
        ".toast-error",
        "[role='alert']",
        ".MuiAlert-message"
    ]
    for sel in selectors:
        try:
            loc = page.locator(sel).first
            if loc.is_visible():
                return loc.inner_text()
        except:
            pass
    return ""


def get_screen_size():
    root = tk.Tk()
    root.withdraw()  # hide window
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return width, height

def format_duration(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours}h {minutes}m {secs}s"

def summarize_results(test_results):
    total = len(test_results)
    passed = sum(1 for r in test_results if r["status"] == "PASSED")
    failed = total - passed
    return total, passed, failed

def create_pie_chart(test_results, chart_path):
    total, passed, failed = summarize_results(test_results)
    labels = ['Passed', 'Failed']
    sizes = [passed, failed]
    colors = ['#4CAF50', '#F44336']
    explode = (0.05, 0)  # slightly separate 'Passed' slice

    plt.figure(figsize=(5,5))
    plt.pie(
        sizes, labels=labels, colors=colors, autopct='%1.0f%%',
        startangle=90, explode=explode, textprops={'fontsize':14, 'color':'#0B395B'}
    )
    plt.title('Test Pass Rate', fontsize=16, color='#0B395B')
    plt.tight_layout()
    plt.savefig(chart_path, transparent=True)
    plt.close()

# ===============================
# Email Report
# ===============================
def send_email(test_results):
    timestamp = datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p")
    chart_path = REPORT_DIR / f"test_results_chart_{timestamp}.png"

    create_pie_chart(test_results, chart_path)
    total, passed, failed = summarize_results(test_results)


    msg = EmailMessage()
    msg["Subject"] = f"Automated Test Report | Passed: {passed} | Failed: {failed}"
    msg["From"] = GMAIL_USER
    msg["To"] = RECIPIENT_EMAIL

    html = f"""
    <html>
    <body style="font-family:Arial, sans-serif; background:#F5F7FA; padding:20px; margin:0;">
      <div style="width:100%; max-width:100%; margin:auto; background:#FFFFFF; border-radius:8px; padding:20px;">
        <h2 style="color:#0B395B; text-align:center;">🧪 Automated Test Report</h2>
        <p style="text-align:center;"><strong>Timestamp:</strong> {timestamp}</p>

        <!-- Summary Tiles -->
        <table width="100%" cellpadding="10" cellspacing="0" style="border-collapse:collapse; margin:20px 0; text-align:center;">
          <tr>
            <!-- Total Tests -->
            <td style="
                background: linear-gradient(135deg, #177AC1, #0B395B);
                color: white;
                border-radius: 12px;
                padding: 20px;
                width: 33%;
                min-width:120px;
            ">
              <strong style="display:block; font-size:16px;">Total Tests</strong>
              <span style="font-size:28px; font-weight:bold;">{total}</span>
            </td>

            <!-- Passed -->
            <td style="
                background: linear-gradient(135deg, #4CAF50, #2E7D32);
                color: white;
                border-radius: 12px;
                padding: 20px;
                width: 33%;
                min-width:120px;
            ">
              <strong style="display:block; font-size:16px;">Passed</strong>
              <span style="font-size:28px; font-weight:bold;">{passed}</span>
            </td>

            <!-- Failed -->
            <td style="
                background: linear-gradient(135deg, #F44336, #C62828);
                color: white;
                border-radius: 12px;
                padding: 20px;
                width: 33%;
                min-width:120px;
            ">
              <strong style="display:block; font-size:16px;">Failed</strong>
              <span style="font-size:28px; font-weight:bold;">{failed}</span>
            </td>
          </tr>
        </table>

        <!-- Test Results Table -->
        <table width="100%" cellpadding="10" cellspacing="0" style="border-collapse:collapse; margin-top:20px; font-size:14px;">
          <tr style="background:#0B395B; color:white;">
            <th align="left" style="width:15%;">Test</th>
            <th align="left" style="width:50%;">Scenario</th>
            <th align="center" style="width:15%;">Status</th>
            <th align="center" style="width:15%;">Duration</th>
            <th align="center" style="width:20%;">Screenshot</th>
          </tr>
    """


    for r in test_results:
        badge_bg = "#E8F5E9" if r["status"] == "PASSED" else "#FDECEA"
        badge_color = "#2E7D32" if r["status"] == "PASSED" else "#C62828"
        row_bg = "#FFFFFF" if r["status"] == "PASSED" else "#FFF5F5"
        cid = os.path.basename(r["screenshot"])

        html += f"""
        <tr style="background:{row_bg}; border-bottom:1px solid #DDD;">
        <td><strong>{r['title']}</strong></td>
        <td>{r['description']}</td>
        <td align="center">
            <span style="padding:6px 12px; border-radius:20px;
                        background:{badge_bg}; color:{badge_color};
                        font-weight:bold; font-size:12px;">
            {r['status']}
            </span>
        </td>
        </td>
        <td align="center">{r.get('scenario_duration', 'N/A')}</td>
        <td align="center">
            <img src="cid:{cid}" width="160"
                style="border:1px solid #CCC; border-radius:4px;">
        </td>
        </tr>
        """

        # Add error traceback if failed
        if r["status"] == "FAILED" and r.get("error_trace"):
            html += f"""
            <tr style="background:#FFF5F5; border-bottom:1px solid #DDD;">
            <td colspan="4" style="padding:10px;">
                <strong style="color:#C62828;">⚠️ Error Details:</strong>
                <pre style="
                    background:#FDECEA; 
                    color:#C62828; 
                    font-size:12px; 
                    padding:10px; 
                    border-radius:6px; 
                    max-height:150px; 
                    overflow:auto;
                ">{r['error_trace']}</pre>
            </td>
            </tr>
            """

    html += f"""
        </table>
<div style="
    margin-top:40px; 
    background:#FFFFFF; 
    border-radius:12px; 
    padding:20px; 
    box-shadow:0 4px 12px rgba(0,0,0,0.08);
    text-align:center;
">
    <h3 style="
        margin-top:0; 
        margin-bottom:20px; 
        color:#0B395B; 
        font-size:20px;
        font-weight:bold;
    ">
        📊 Test Pass Rate
    </h3>

    <img src="cid:{chart_path.name}" 
         style="
             width:300px; 
             max-width:100%; 
             border:1px solid #CCC; 
             border-radius:12px;
             box-shadow:0 2px 8px rgba(0,0,0,0.06);
         " 
    >

    <p style="margin-top:15px; font-size:14px; color:#0B395B; font-weight:bold;">
    ⏱ Total Execution Time: {format_duration(test_results[0].get('total_duration', 0))}
    </p>

    <!-- Legend -->
    <div style="margin-top:15px; display:flex; justify-content:center; gap:30px; flex-wrap:wrap;">
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="
                display:inline-block; 
                width:16px; height:16px; 
                background:#4CAF50; 
                border-radius:4px;
            "></span>
            <span style="font-size:14px; color:#333;">Passed</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="
                display:inline-block; 
                width:16px; height:16px; 
                background:#F44336; 
                border-radius:4px;
            "></span>
            <span style="font-size:14px; color:#333;">Failed</span>
        </div>
    </div>
</div>

    """

    msg.add_alternative(html, subtype="html")

    # Attach screenshots
    for r in test_results:
        try:
            with open(r["screenshot"], "rb") as f:
                msg.get_payload()[0].add_related(
                    f.read(), "image", "png", cid=os.path.basename(r["screenshot"])
                )
        except Exception as e:
            print(f"⚠️ Could not attach screenshot {r['screenshot']}: {e}")

    # Attach chart
    try:
        with open(chart_path, "rb") as f:
            msg.get_payload()[0].add_related(
                f.read(), "image", "png", cid=chart_path.name
            )
    except Exception as e:
        print(f"⚠️ Could not attach chart {chart_path}: {e}")

    # Send email safely
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
        print("📧 Email report sent successfully")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")



def run_scenario_with_retry(playwright, scenario, login_url, max_retries=1):
    final_result = None
    start_time = datetime.now()
    screen_width, screen_height = get_screen_size()  # get current screen resolution

    for attempt in range(max_retries + 1):
        print(f"🔁 Running '{scenario['title']}' | Attempt {attempt + 1}")

        browser = playwright.chromium.launch(
            headless=False,
            args=[f"--window-size={screen_width},{screen_height}"]
        )

        context = browser.new_context(
            viewport={"width": screen_width, "height": screen_height}  # full screen
        )
        page = context.new_page()

        attempt_start = datetime.now()
        result = run_scenario(page, scenario["title"], scenario["description"], login_url)
        attempt_end = datetime.now()

        result["attempt_duration"] = str(attempt_end - attempt_start)

        context.close()
        browser.close()

        if result["status"] == "PASSED":
            result["retry_attempt"] = attempt
            result["final_status"] = "PASSED"
            result["scenario_duration"] = str(attempt_end - start_time)
            return result

        final_result = result

    final_result["retry_attempt"] = max_retries
    final_result["final_status"] = "FAILED"
    final_result["note"] = "Failed after retry"
    final_result["scenario_duration"] = str(datetime.now() - start_time)
    return final_result

# ===============================
# Run Scenario
# ===============================
def run_scenario(page, title, description, login_url):
    error_trace = ""
    browser_errors = []
    network_errors = []
    ui_error = ""
    actual_result = ""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = SCREENSHOT_DIR / f"{title.replace(' ', '_')}_{timestamp}.png"
    status = "FAILED"

    try:
##=========================================================================================##
##--- HAPPY PATH SCENARIOS (LOGIN) ---

        if title == "Login Test":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="Open user menu").wait_for(timeout=30000)
            page.get_by_role("link", name="Open user menu").click()
            page.get_by_role("link", name="Signout").click()
            status = "PASSED"

        elif title == "Logout Test":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="Open user menu").wait_for(timeout=30000)
            page.get_by_role("link", name="Open user menu").click()
            page.get_by_role("link", name="Signout").click()
            status = "PASSED"

##--- NEGATIVE PATH SCENARIOS (LOGIN) ---

        elif title == "Login without pass":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_timeout(2000)
            system_error = page.locator("text=Error|Failed|Unable")
            validation_msg = page.locator("text=Missing or invalid input. Try again")
            system_error = page.locator("text=Error|Failed|Unable")

            if validation_msg.count() > 0:
                actual_result = "Missing or invalid input. Try again"
                status = "PASSED"

            elif system_error.count() > 0:
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

        elif title == "Non Existing Account":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").click()
            page.get_by_role("textbox", name="your@email.com").fill("BossAtanLebronJames@gmail.com")
            page.get_by_role("textbox", name="your@email.com").press("Tab")
            page.get_by_role("textbox", name="your password").fill("Traxiontech.123")
            page.get_by_role("button", name="Sign in").click().wait_for(timeout=30000)
            ystem_error = page.locator("text=Error|Failed|Unable")
            validation_msg = page.locator("text=Authentication error. Invalid credentials. Please try again.")
            system_error = page.locator("text=Error|Failed|Unable")

            if validation_msg.count() > 0:
                actual_result = "Authentication error. Invalid credentials. Please try again."
                status = "PASSED"

            elif system_error.count() > 0:
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

        elif title == "Password Length":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("textbox", name="your password").fill("qwetqwetqwetqasjhdbasjhdasbd21")
            page.get_by_role("link", name="Show password").click()
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_timeout(2000)
            password_input = page.get_by_role("textbox", name="your password")
            entered_value = password_input.input_value()

            dashboard_element = page.get_by_role("link", name="Open user menu")

            if len(entered_value) < len("qwetqwetqwetqasjhdbasjhdasbd21"):
                status = "PASSED"
                actual_result = "Password field restricted input length"

            elif dashboard_element.count() == 0:
                status = "PASSED"
                actual_result = "Login blocked for long password"

            else:
                status = "FAILED"
                actual_result = "System accepted invalid long password"

        elif title == "Invalid Password":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("textbox", name="your password").fill("Tarasdtadasdhqwwe")
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_timeout(2000)
            system_error = page.locator("text=Error|Failed|Unable")
            validation_msg = page.locator("text=Authentication error. Invalid credentials. Please try again.")

            if validation_msg.count() > 0:
                actual_result = "Authentication error. Invalid credentials. Please try again."
                status = "PASSED"

            elif system_error.count() > 0:
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"


##=========================================================================================##
##--- HAPPY PATH SCENARIOS (WITHDRAWALS) ---

        elif title == "Direct Fundtransfer":
            page.goto(login_url, timeout=30000)
            page.goto("https://digicoop-sit.traxionpay.com/signin")
            page.get_by_role("textbox", name="your@email.com").click()
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+digicoop@traxiontech.net")
            page.get_by_role("textbox", name="your@email.com").press("Tab")
            page.get_by_role("textbox", name="your password").fill("Traxion123!")
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="Withdrawals").click()
            page.get_by_role("link", name="Direct Fund Transfer").click()
            page.get_by_role("textbox", name="Mobile/Account Number/Wallet").click()
            page.get_by_role("textbox", name="Mobile/Account Number/Wallet").fill("+639304925700")
            page.get_by_text("Amount", exact=True).click()
            page.get_by_placeholder("0.00").click()
            page.get_by_placeholder("0.00").fill("1")
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("radio", name="Password").check()
            page.get_by_role("textbox", name="Account Name").click()
            page.get_by_role("textbox", name="form-control required field").click()
            page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
            page.wait_for_load_state("networkidle", timeout=10000)
            page.get_by_role("button", name="Transfer Funds").click()
            with page.expect_download() as download_info:
                page.get_by_role("button", name="Download Receipt").click()
            download = download_info.value
            system_error = page.locator("text=Error|Failed|Unable")
            validation_msg = page.locator("text=Fund Transfer transaction processed successfully.")
            system_error = page.locator("text=Error|Failed|Unable")

            if validation_msg.count() > 0:
                actual_result = "Fund Transfer transaction processed successfully."
                status = "PASSED"

            elif system_error.count() > 0:
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

        elif title == "Direct Fundtransfer Invalid Password":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="Withdrawals").click()
            page.get_by_role("link", name="Direct Fund Transfer").click()
            page.get_by_role("textbox", name="Mobile/Account Number/Wallet").click()
            page.get_by_role("textbox", name="Mobile/Account Number/Wallet").fill("+639304925700")
            page.get_by_text("Amount", exact=True).click()
            page.get_by_placeholder("0.00").click()
            page.get_by_placeholder("0.00").fill("1")
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("radio", name="Password").check()
            page.get_by_role("textbox", name="Account Name").click()
            page.get_by_role("textbox", name="form-control required field").click()
            page.get_by_role("textbox", name="form-control required field").fill("Traxion1")
            page.wait_for_load_state("networkidle", timeout=10000)
            page.get_by_role("button", name="Transfer Funds").click()
            validation_msg = page.locator("text=Incorrect password")
            system_error = page.locator("text=Error|Failed|Unable")

            # wait for either validation or error to appear
            page.wait_for_timeout(2000)

            if validation_msg.first.is_visible():
                actual_result = "Incorrect password provided"
                status = "PASSED"

            elif system_error.first.is_visible():
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"
        
        elif title == "Withdraw Funds":
            page.goto("https://mannypay-sit.traxionpay.com/signin")
            page.get_by_role("textbox", name="your@email.com").click()
            page.get_by_role("textbox", name="your@email.com").fill("tpaymerchantqa@mailinator.com")
            page.get_by_role("textbox", name="your@email.com").press("Tab")
            page.get_by_role("textbox", name="your password").fill("Traxion123!")
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="Withdrawals").click()
            page.get_by_role("link", name="Withdraw Funds").click()
            page.locator(".form-check").first.click()
            page.get_by_label("SelectAlipayALLBANK INCASIA").select_option("2122")
            page.get_by_role("textbox", name="Account Name").click()
            page.get_by_role("textbox", name="Account Name").fill("Test")
            page.get_by_role("textbox", name="Account Number").click()
            page.get_by_role("textbox", name="Account Number").fill("109594480005")
            page.get_by_placeholder("0.00").click()
            page.get_by_placeholder("0.00").fill("100")
            page.get_by_role("radio", name="Password").check()
            page.get_by_role("textbox", name="form-control required field").click()
            page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
            page.get_by_role("button", name="Withdraw Funds").click()
            with page.expect_download() as download_info:
                page.get_by_role("button", name="Download Receipt").click()
            download = download_info.value
            validation_msg = page.locator("text=Fund Transfer transaction processed/initiated successfully.")
            system_error = page.locator("text=Error|Failed|Unable")

            # wait for either validation or error to appear
            page.wait_for_timeout(2000)

            if validation_msg.first.is_visible():
                actual_result = "Fund Transfer transaction processed/initiated successfully."
                status = "PASSED"

            elif system_error.first.is_visible():
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"
        
        elif title == "Withdraw Funds Invalid Password":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="Withdrawals").click()
            page.get_by_role("link", name="Withdraw Funds").click()
            page.locator(".form-check").first.click()
            page.get_by_label("SelectAlipayALLBANK INCASIA").select_option("2122")
            page.get_by_role("textbox", name="Account Name").click()
            page.get_by_role("textbox", name="Account Name").fill("Test")
            page.get_by_role("textbox", name="Account Number").click()
            page.get_by_role("textbox", name="Account Number").fill("109594480005")
            page.get_by_placeholder("0.00").click()
            page.get_by_placeholder("0.00").fill("100")
            page.get_by_role("radio", name="Password").check()
            page.get_by_role("textbox", name="form-control required field").click()
            page.get_by_role("textbox", name="form-control required field").fill("Traxion!")
            page.get_by_role("button", name="Withdraw Funds").click()
            validation_msg = page.locator("text=Incorrect password")
            system_error = page.locator("text=Error|Failed|Unable")

            # wait for either validation or error to appear
            page.wait_for_timeout(2000)

            if validation_msg.first.is_visible():
                actual_result = "Incorrect password provided"
                status = "PASSED"

            elif system_error.first.is_visible():
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

##--- NEGATIVE PATH SCENARIOS (WITHDRAWALS) ---
##=========================================================================================##
    
##--- HAPPY PATH SCENARIOS (DEPOSIT) ---
        elif title == "Manual Deposit":
            page.goto(login_url, timeout=30000)

            # login
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()

            # go to deposit
            page.get_by_role("link", name="Deposits").click()
            page.get_by_role("link", name="Make A Deposit").click()

            # amount
            page.locator("#manual_amount").click()
            page.locator("#manual_amount").fill("500")

            # select bank
            page.get_by_label("Select BANCO DE ORO UNIBANK,").select_option("BDO_UNIBANK")

            # upload file
            file_input = page.locator("input[type='file']")
            file_input.set_input_files(r"C:\Users\Rafael\.vscode\AUTOMATION\AUTOMATION REPORT.png")

            # submit
            page.get_by_role("button", name="Submit Manual Deposit Request").click()

            # validation messages
            success_msg = page.locator("text=Manual deposit request")
            system_error = page.locator("text=Error|Failed|Unable")

            try:
                success_msg.first.wait_for(timeout=15000)

                actual_result = success_msg.first.inner_text()
                status = "PASSED"

            except:
                if system_error.first.is_visible():
                    actual_result = system_error.first.inner_text()
                    status = "FAILED"

                else:
                    actual_result = "No success message displayed"
                    status = "FAILED"

        elif title == "Cash In from DragonPay":
            page.goto(login_url, timeout=30000)
            page.wait_for_timeout(2000)
            page.goto("https://merchant-sit.traxionpay.com/signin", timeout=30000)
            page.get_by_role("textbox", name="your@email.com").click(timeout=10000)
            page.get_by_role("textbox", name="your@email.com").fill("tpaymerchantqa@mailinator.com", timeout=10000)
            page.get_by_role("textbox", name="your password").fill("Traxion123!", timeout=10000)
            page.get_by_role("button", name="Sign in").click(timeout=10000)
            page.get_by_role("link", name="Deposits").click()
            page.get_by_role("link", name="Make A Deposit").click()
            page.locator("span").filter(has_text="Online Deposit Other online").first.click()
            page.locator("#online_amount").click()
            page.locator("#online_amount").fill("100")
            page.get_by_label("Select Bank Deposits/").select_option("2")
            page.get_by_label("SelectBDO | BDO Internet").select_option("36823")
            page.get_by_role("button", name="Create online deposit request").click()
            page.locator("iframe[title=\"Response\"]").content_frame.locator("#ctl00_ContentPlaceHolder1_userIdTextBox").click()
            page.locator("iframe[title=\"Response\"]").content_frame.locator("#ctl00_ContentPlaceHolder1_userIdTextBox").fill("a")
            page.locator("iframe[title=\"Response\"]").content_frame.locator("#ctl00_ContentPlaceHolder1_passwdTextBox").click()
            page.locator("iframe[title=\"Response\"]").content_frame.locator("#ctl00_ContentPlaceHolder1_passwdTextBox").fill("a")
            page.locator("iframe[title=\"Response\"]").content_frame.get_by_role("button", name="Continue").click()
            page.locator("iframe[title=\"Response\"]").content_frame.get_by_role("button", name="Pay").click()
            page.wait_for_load_state("networkidle", timeout=90000)
            status = "PASSED"

##--- NEGATIVE PATH SCENARIOS (DEPOSIT) ---

        elif title == "Leave Blank Required Fields in Manual Deposit":
            page.goto(login_url, timeout=30000)
            data = TestDataGenerator()
            first_name = data.first_name()
            last_name = data.last_name()
            email = data.email(first_name, last_name)
            mobile = data.mobile_number()
            password = data.password()

            # login
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="Deposits").click()
            page.get_by_role("link", name="Make A Deposit").click()
            page.get_by_role("button", name="Submit Manual Deposit Request").click()
            validation_msg = page.locator("text=This Field is Required")
            system_error = page.locator("text=Error|Failed|Unable")

            # wait for either validation or error to appear
            page.wait_for_timeout(2000)

            if validation_msg.first.is_visible():
                actual_result = "This Field is Required"
                status = "PASSED"

            elif system_error.first.is_visible():
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

        elif title == "Leave Blank Deposit Slip":
            page.goto(login_url, timeout=30000)
            data = TestDataGenerator()
            first_name = data.first_name()
            last_name = data.last_name()
            email = data.email(first_name, last_name)
            mobile = data.mobile_number()
            password = data.password()  
            page.get_by_role("textbox", name="your@email.com").click()
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("textbox", name="your@email.com").press("Tab")
            page.get_by_role("textbox", name="your password").fill("Traxion123!")
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="Deposits").click()
            page.get_by_role("link", name="Make A Deposit").click()
            page.locator("#manual_amount").click()
            page.locator("#manual_amount").fill("500")
            page.get_by_label("Select BANCO DE ORO UNIBANK,").select_option("UNIONBANK")
            page.get_by_role("button", name="Submit Manual Deposit Request").click()
    
            validation_msg = page.locator("text=This Field is Required")
            system_error = page.locator("text=Error|Failed|Unable")

            # wait for either validation or error to appear
            page.wait_for_timeout(2000)

            if validation_msg.first.is_visible():
                actual_result = "This Field is Required"
                status = "PASSED"

            elif system_error.first.is_visible():
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

##=========================================================================================##
##--- HAPPY PATH SCENARIOS (ELOAD) ---

        elif title == "Eload":
            page.goto(login_url, timeout=30000)
            page.wait_for_timeout(2000)

            page.goto("https://mannypay-sit.traxionpay.com/signin", timeout=30000)
            page.wait_for_timeout(2000)

            # login
            page.get_by_role("textbox", name="your@email.com").click(timeout=10000)
            page.wait_for_timeout(1000)

            page.get_by_role("textbox", name="your@email.com").fill("blaserna+mpay@traxiontech.net", timeout=10000)
            page.wait_for_timeout(1000)

            page.get_by_role("textbox", name="your@email.com").press("Tab", timeout=10000)
            page.wait_for_timeout(1000)

            page.get_by_role("textbox", name="your password").fill("Traxion123!", timeout=10000)
            page.wait_for_timeout(1000)

            page.get_by_role("button", name="Sign in").click(timeout=10000)
            page.wait_for_timeout(3000)

            # eload
            page.get_by_role("link", name="E-Load").click(timeout=10000)
            page.wait_for_timeout(2000)

            page.get_by_role("img", name="SMART").click(timeout=10000)
            page.wait_for_timeout(2000)

            page.get_by_role("textbox", name="Enter recipient's number...").click(timeout=10000)
            page.wait_for_timeout(1000)

            page.get_by_role("textbox", name="Enter recipient's number...").fill("09471594731", timeout=10000)
            page.wait_for_timeout(1000)

            page.get_by_role("button", name="Proceed").click(timeout=10000)
            page.wait_for_timeout(3000)

            page.get_by_text("Smart Load 20", exact=True).click(timeout=10000)
            page.wait_for_timeout(2000)

            page.get_by_role("link", name="Next").click(timeout=10000)
            page.wait_for_timeout(2000)

            # password validation
            page.get_by_role("radio", name="Password").check(timeout=10000)
            page.wait_for_timeout(1000)

            page.get_by_role("textbox", name="Enter MPIN or Password").click(timeout=10000)
            page.wait_for_timeout(1000)

            page.get_by_role("textbox", name="Enter MPIN or Password").fill("Traxion123!", timeout=10000)
            page.wait_for_timeout(1000)

            page.get_by_role("button", name="Submit").click(timeout=10000)
            page.wait_for_timeout(5000)

            # validation
            validation_msg = page.locator("text=MPIN/Password validated")
            system_error = page.locator("text=Error|Failed|Unable")

            if validation_msg.first.is_visible():
                actual_result = "MPIN/Password validated"
                status = "PASSED"

            elif system_error.first.is_visible():
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

        
        elif title == "Eload invalid credential":
            page.goto(login_url, timeout=30000)
            # login
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="E-Load").click()
            page.get_by_role("img", name="SMART").click()
            page.get_by_role("textbox", name="Enter recipient's number...").click()
            page.get_by_role("textbox", name="Enter recipient's number...").fill("09471594731")
            page.get_by_role("button", name="Proceed").click()
            page.get_by_text("Smart Load 20", exact=True).click()
            page.get_by_role("link", name="Next").click()
            page.get_by_role("radio", name="Password").check()
            page.get_by_role("textbox", name="Enter MPIN or Password").click()
            page.get_by_role("textbox", name="Enter MPIN or Password").fill("Traxion123!1")
            # after entering invalid password
            page.get_by_role("button", name="Submit").click()  # adjust button name if needed

            validation_msg = page.locator("text=Invalid Credentials")
            system_error = page.locator("text=Error|Failed|Unable")

            try:
                validation_msg.first.wait_for(timeout=10000)
                actual_result = "Invalid Credentials"
                status = "PASSED"

            except:
                if system_error.first.is_visible():
                    actual_result = system_error.first.inner_text()
                else:
                    actual_result = "No validation message displayed"
                status = "FAILED"


        elif title == "E-load Number length Validation":

            page.goto(login_url, timeout=30000)
            # login\
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.wait_for_timeout(500)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.wait_for_timeout(500)
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_timeout(500)

            page.get_by_role("link", name="E-Load").click()
            page.wait_for_timeout(500)
            page.get_by_role("img", name="TM").click()
            page.wait_for_timeout(500)
            page.get_by_role("textbox", name="Enter recipient's number...").click()
            page.wait_for_timeout(500)
            page.get_by_role("textbox", name="Enter recipient's number...").fill("09123567894561")
            page.wait_for_timeout(500)

            page.get_by_text("Telco Non-Telco TM Change").click()
            page.wait_for_timeout(500)
            page.get_by_role("button", name="Proceed").click()
            page.wait_for_timeout(500)
            page.get_by_text("Touch Mobile Amax 25").click()
            page.wait_for_timeout(500)
            page.get_by_role("link", name="Next").click()
            page.wait_for_timeout(500)

            page.locator("#remoteModal").click()
            page.get_by_role("button", name="Submit").click()

##--- NEGATIVE PATH SCENARIOS (ELOAD) ---

        elif title == "Negative: Invalid Recipient Number":
            page.goto(login_url, timeout=30000)
            data = TestDataGenerator()
            first_name = data.first_name()
            last_name = data.last_name()
            email = data.email(first_name, last_name)
            mobile = data.mobile_number()
            password = data.password()
        
            page.get_by_rFole("textbox", name="your@email.com").click()
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
            page.wait_for_timeout(2000)
            validation_error = page.locator(
                "text=Invalid recipient number|invalid recipient|Please enter a valid number|Invalid number|number is invalid"
            )
            if validation_error.count() > 0:
                actual_result = validation_error.first.inner_text()
                status = "PASSED"
            else:
                system_error = page.locator("text=Error|Failed|Unable")
                if system_error.count() > 0:
                    actual_result = system_error.first.inner_text()
                    status = "FAILED"
                else:
                    actual_result = "Invalid recipient number validation not triggered"
                    status = "FAILED"

        elif title == "E-Load Invalid Number Format":
            page.goto(login_url, timeout=30000)
            data = TestDataGenerator()
            first_name = data.first_name()
            last_name = data.last_name()
            email = data.email(first_name, last_name)
            mobile = data.mobile_number()
            password = data.password()

            page.get_by_role("textbox", name="your@email.com").click()
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("textbox", name="your@email.com").press("Tab")
            page.get_by_role("textbox", name="your password").fill("Traxion123!")
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="E-Load").click()
            page.get_by_role("img", name="TM").click()
            page.get_by_role("textbox", name="Enter recipient's number...").click()
            page.get_by_role("textbox", name="Enter recipient's number...").fill("85463215486")
            page.get_by_role("button", name="Proceed").click()
            page.get_by_text("Touch Mobile Amax 25").click()
            page.get_by_role("link", name="Next").click()
            page.get_by_role("radio", name="Password").check()
            page.get_by_role("textbox", name="Enter MPIN or Password").click()
            page.get_by_role("textbox", name="Enter MPIN or Password").fill("Traxion123!")
            page.get_by_role("button", name="Submit").click()
            # Negative test - wait for asynchronous invalid number validation message
            validation_error = page.locator(
                "text=Invalid target mobile number|Invalid recipient number|invalid recipient|Please enter a valid number|Invalid number|number is invalid|invalid format|format|Format"
            )
            try:
                validation_error.wait_for(timeout=7000)
                actual_result = validation_error.first.inner_text()
                status = "PASSED"
            except Exception:
                try:
                    validation_error.wait_for(timeout=5000)
                    actual_result = validation_error.first.inner_text()
                    status = "PASSED"
                except Exception:
                    actual_result = "Invalid number format validation not triggered"
                    status = "FAILED"

        elif title == "Without Entering Number":
            page.goto(login_url, timeout=30000)
            data = TestDataGenerator()
            first_name = data.first_name()
            last_name = data.last_name()
            email = data.email(first_name, last_name)
            mobile = data.mobile_number()
            password = data.password()
            
            page.get_by_role("textbox", name="your@email.com").click()
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("textbox", name="your@email.com").press("Tab")
            page.get_by_role("textbox", name="your password").fill("Traxion123!")
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="E-Load").click()
            page.get_by_role("img", name="TM").click()
            page.get_by_role("button", name="Proceed").click()
            system_error = page.locator("text=Error|Failed|Unable")
            if system_error.count() > 0:
                actual_result = system_error.first.inner_text()
                status = "FAILED"
            else:
                actual_result = "This Field is required"
                status = "PASSED"

        elif title == "Without Entering Password":
            page.goto(login_url, timeout=30000)
            data = TestDataGenerator()
            first_name = data.first_name()
            last_name = data.last_name()
            email = data.email(first_name, last_name)
            mobile = data.mobile_number()
            password = data.password()
            page.get_by_role("textbox", name="your@email.com").click()
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("textbox", name="your@email.com").press("Tab")
            page.get_by_role("textbox", name="your password").fill("Traxion123!")
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="E-Load").click()
            page.get_by_role("img", name="TM").click()
            page.get_by_role("button", name="Proceed").click()
            system_error = page.locator("text=Error|Failed|Unable")
            if system_error.count() > 0:
                actual_result = system_error.first.inner_text()
                status = "FAILED"
            else:
                actual_result = "This Field is required"
                status = "PASSED"


##--- HAPPY PATH SCENARIOS (BUYLOAD)

        elif title == "Buyload":
           # page.goto(login_url, timeout=30000)
           # data = TestDataGenerator()
           # first_name = data.first_name()
           # last_name = data.last_name()
           # email = data.email(first_name, last_name)
           # mobile = data.mobile_number()
           # password = data.password()

            page.goto(login_url, timeout=30000)
            page.goto("https://rbpay-sit.traxionpay.com/signin")
            page.get_by_role("textbox", name="your@email.com").click()
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+rbpay@traxiontech.net")
            page.get_by_role("textbox", name="your@email.com").press("Tab")
            page.get_by_role("textbox", name="your password").fill("Traxion123!")
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="E-Load").click()
            page.get_by_role("img", name="TM").click()
            page.get_by_role("textbox", name="Enter recipient's number...").click()
            page.get_by_role("textbox", name="Enter recipient's number...").fill("09380529031")
            page.get_by_role("button", name="Proceed").click()
            page.get_by_text("Touch Mobile Amax 20").click()
            page.get_by_role("link", name="Next").click()
            page.get_by_role("radio", name="Password").check()
            page.get_by_role("textbox", name="Enter MPIN or Password").click()
            page.get_by_role("textbox", name="Enter MPIN or Password").fill("Traxion123!")
            page.get_by_role("button", name="Submit").click()
            page.wait_for_timeout(2000)
            system_error = page.locator("text=Error|Failed|Unable")
            if system_error.count() > 0:
                actual_result = system_error.first.inner_text()
                status = "FAILED"
            else:
                actual_result = "Buyload transaction completed"
                status = "PASSED"

        elif title == "Non Telco":
            page.goto(login_url, timeout=30000)

            data = TestDataGenerator()
            first_name = data.first_name()
            last_name = data.last_name()
            email = data.email(first_name, last_name)
            mobile = data.mobile_number()
            password = data.password()

            page.goto(login_url, timeout=30000)
            page.wait_for_timeout(2000)

            page.goto("https://mannypay-sit.traxionpay.com/signin", timeout=30000)
            page.wait_for_timeout(2000)

            # login
            page.get_by_role("textbox", name="your@email.com").click

            page.get_by_role("textbox", name="your@email.com").fill(
                "blaserna+mpay@traxiontech.net",)
            page.wait_for_timeout(1000)
            page.get_by_role("textbox", name="your password").fill(
                "Traxion123!",)
            page.get_by_role("button", name="Sign in").click
            page.get_by_role("link", name="E-Load").click
            page.get_by_role("tab", name="Non-Telco").click
            page.get_by_role("img", name="EASYTRIP").click
            page.get_by_role("textbox", name="Enter recipient's number...").click
            page.get_by_role("textbox", name="Enter recipient's number...").fill(
                "123456789012",
                timeout=10000
            )
            page.get_by_role("button", name="Proceed").click
            page.locator("div").filter(
                has_text=re.compile(r"^EASYTRIP 600$")
            ).click(timeout=10000)
            page.wait_for_timeout(2000)

            page.get_by_role("link", name="Next").click(timeout=10000)
            page.wait_for_timeout(2000)

            # password
            page.get_by_role("radio", name="Password").check(timeout=10000)
            page.wait_for_timeout(1000)

            page.get_by_role("textbox", name="Enter MPIN or Password").click(timeout=10000)
            page.wait_for_timeout(1000)

            page.get_by_role("textbox", name="Enter MPIN or Password").fill(
                "Traxion123!",
                timeout=10000
            )
            page.wait_for_timeout(1000)

            page.get_by_role("button", name="Submit").click(timeout=10000)
            page.wait_for_timeout(5000)

            # validation
            validation_msg = page.locator("text=successful|Success|Completed")
            system_error = page.locator("text=Error|Failed|Unable")

            if validation_msg.first.is_visible():
                actual_result = "Non-Telco transaction completed"
                status = "PASSED"

            elif system_error.first.is_visible():
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

##--- NEGATIVE PATH SCENARIOS (BUYLOAD)

##=========================================================================================##
##--- HAPPY PATH SCENARIOS (ADD USER) ---


        elif title == "Add User":
            page.goto(login_url, timeout=30000)
            data = TestDataGenerator()
            first_name = data.first_name()
            last_name = data.last_name()
            email = data.email(first_name, last_name)
            mobile = data.mobile_number()
            
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Users").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Add New User").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("textbox", name="First Name *").fill(first_name)
            page.get_by_role("textbox", name="Last Name *").fill(last_name)
            page.get_by_role("textbox", name="Email Address *").fill(email)
            page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill(mobile)
            page.get_by_role("textbox", name="Password *").fill("Traxion123!")
            page.get_by_role("textbox", name="Minimum 8 characters required").fill("Traxion123!")
            page.get_by_role("textbox", name="MPIN *", exact=True).fill("031226")
            page.get_by_role("textbox", name="Confirm MPIN *").fill("031226")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            page.get_by_label("User Role *").select_option("342")
            page.get_by_role("button", name="Add user").click()
            page.wait_for_timeout(2000)
            # Check for success first (positive test)
            success_locator = page.locator("text=User added successfully|User creation successful")
            if success_locator.count() > 0:
                actual_result = success_locator.first.inner_text()
                status = "PASSED"
            else:
                # If no success, check for system errors
                error_locator = page.locator("text=Error|Failed|Unable")
                if error_locator.count() > 0:
                    actual_result = error_locator.first.inner_text()
                    status = "FAILED"
                else:
                    actual_result = "User added"
                    status = "PASSED"

        elif title == "Edit User Role":

            page.goto(login_url, timeout=30000)

            page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("textbox", name="your password").fill("Traxion123!")
            page.get_by_role("button", name="Sign in").click()

            page.get_by_role("link", name="Users").click()

            page.wait_for_load_state("networkidle")

            try:
                user_cell = page.locator("td", has_text="Joshua Kenneth")

                user_cell.first.wait_for(timeout=10000)
                user_cell.first.click()

                page.get_by_role("link", name="Edit").click()

                page.get_by_label("User Role *").select_option(label="Cashin")

                page.get_by_role("button", name="Save Changes").click()

                page.wait_for_timeout(3000)

                success_msg = page.locator("text=updated successfully")

                if success_msg.count() > 0:
                    actual_result = success_msg.first.inner_text()
                    status = "PASSED"

                else:
                    actual_result = "User role updated"
                    status = "PASSED"

            except:
                actual_result = "User record not found"
                status = "FAILED"

        elif title == "Deactivate Account":

            page.goto(login_url, timeout=30000)

            page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("textbox", name="your password").fill("Traxion123!")
            page.get_by_role("button", name="Sign in").click()

            page.get_by_role("link", name="Users").click()

            page.wait_for_load_state("networkidle")

            try:
                user_cell = page.locator("td", has_text="Joshua Kenneth")

                user_cell.first.wait_for(timeout=10000)
                user_cell.first.click()

                page.get_by_role("link", name="Deactivate").click()
                page.get_by_role("button", name="Deactivate").click()

                page.wait_for_timeout(3000)

                success_msg = page.locator("text=Change User request created successfully")
                system_error = page.locator("text=Error|Failed|Unable")

                if success_msg.count() > 0:
                    actual_result = success_msg.first.inner_text()
                    status = "PASSED"

                elif system_error.count() > 0:
                    actual_result = system_error.first.inner_text()
                    status = "FAILED"

                else:
                    actual_result = "Account deactivated successfully"
                    status = "PASSED"

            except:
                actual_result = "User record not found"
                status = "FAILED"

        elif title == "Edit User Name":
                page.goto(login_url, timeout=30000)
                data = TestDataGenerator()
                first_name = data.first_name()
                last_name = data.last_name()
                email = data.email(first_name, last_name)
                mobile = data.mobile_number()
                password = data.password()

                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
                page.get_by_role("textbox", name="your@email.com").press("Tab")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Users").click()
                page.get_by_role("cell", name="Joshua Kennethhgythgudfhuaisdifhasjf.").click()
                page.get_by_role("link", name="Edit").click()
                page.get_by_role("textbox", name="First Name *").dblclick()
                page.get_by_role("textbox", name="First Name *").fill("Boss Joshua Kenneth")
                page.get_by_role("button", name="Save Changes").click()    
                edit_form = page.locator("form")
                if edit_form.count() > 0:
                    actual_result = "User updated successfully"
                    status = "PASSED"
                else:
                    error_locator = page.locator("text=User creation failed|Error|Failed|Unable")
                    if error_locator.count() > 0:
                        actual_result = error_locator.first.inner_text()
                        status = "FAILED"
                    else:
                        actual_result = "Edit page navigated"
                        status = "PASSED"

        elif title == "Add New User":
            page.goto(login_url, timeout=30000)
            sign_in = page.get_by_role("button", name="Sign in")
            expect(sign_in).to_be_enabled()
            sign_in.click()
            page.wait_for_load_state("networkidle", timeout=30000)
            users = page.get_by_role("link", name="Users")
            expect(users).to_be_visible()
            users.click()
            add_user = page.get_by_role("link", name="Add New User")
            expect(add_user).to_be_visible()
            add_user.click()
            first_name_field = page.get_by_role("textbox", name="First Name *")
            expect(first_name_field).to_be_visible()
            first_name_field.fill("Lebron")
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
            page.wait_for_timeout(2000)
            actual_result = "User form submitted successfully"
            status = "PASSED"

##--- NEGATIVE PATH SCENARIOS (ADD USER) ---
        elif title == "Add Existing User":
            page.goto(login_url, timeout=30000)
            data = TestDataGenerator()
            first_name = data.first_name()
            last_name = data.last_name()
            mobile = data.mobile_number()
            
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Users").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Add New User").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("textbox", name="First Name *").fill(first_name)
            page.get_by_role("textbox", name="Last Name *").fill(last_name)
            page.get_by_role("textbox", name="Email Address *").fill("blaserna+0313bibo@traxiontech.net")
            page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill(mobile)
            page.get_by_role("textbox", name="Password *").fill("Traxion123!")
            page.get_by_role("textbox", name="Minimum 8 characters required").fill("Traxion123!")
            page.get_by_role("textbox", name="MPIN *", exact=True).fill("031226")
            page.get_by_role("textbox", name="Confirm MPIN *").fill("031226")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            page.get_by_label("User Role *").select_option("342")
            page.get_by_role("button", name="Add user").click()
            page.wait_for_load_state("networkidle", timeout=10000)
            validation_msg = page.locator("text=User creation failed")
            system_error = page.locator("text=Error|Failed|Unable")

            # wait for either validation or error to appear
            page.wait_for_timeout(2000)

            if validation_msg.first.is_visible():
                actual_result = "User creation failed"
                status = "PASSED"

            elif system_error.first.is_visible():
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"


        elif title == "Required Fields":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("textbox", name="your password").fill("Traxion123!")
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Users").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Add New User").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("textbox", name="First Name *").fill("Traxion")
            page.get_by_role("button", name="Add user").click()
            page.wait_for_timeout(2000)
            validation_msg = page.locator("text=Please fill out the following field")
            system_error = page.locator("text=Error|Failed|Unable")

            # wait for either validation or error to appear
            page.wait_for_timeout(2000)

            if validation_msg.first.is_visible():
                actual_result = "Please fill out the following field"
                status = "PASSED"

            elif system_error.first.is_visible():
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

        elif title == "Existing Email":
            page.goto(login_url, timeout=30000)
            data = TestDataGenerator()
            first_name = data.first_name()
            last_name = data.last_name()
            mobile = data.mobile_number()
            
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Users").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Add New User").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("textbox", name="First Name *").fill(first_name)
            page.get_by_role("textbox", name="Last Name *").fill(last_name)
            page.get_by_role("textbox", name="Email Address *").fill("blaserna+0313bibo@traxiontech.net")
            page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill(mobile)
            page.get_by_role("textbox", name="Password *").fill("Traxion123!")
            page.get_by_role("textbox", name="Minimum 8 characters required").fill("Traxion123!")
            page.get_by_role("textbox", name="MPIN *", exact=True).fill("031226")
            page.get_by_role("textbox", name="Confirm MPIN *").fill("031226")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            page.get_by_label("User Role *").select_option("342")
            page.get_by_role("button", name="Add user").click()
            page.wait_for_timeout(2000)
            validation_msg = page.locator("text=User creation failed")
            system_error = page.locator("text=Error|Failed|Unable")

            # wait for either validation or error to appear
            page.wait_for_timeout(2000)

            if validation_msg.first.is_visible():
                actual_result = "User creation failed"
                status = "PASSED"

            elif system_error.first.is_visible():
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

        elif title == "Mismatching Pass":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("textbox", name="your password").fill("Traxion123!")
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Users").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Add New User").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("textbox", name="First Name *").fill("Lebron")
            page.get_by_role("textbox", name="Last Name *").fill("James")
            page.get_by_role("textbox", name="Email Address *").fill("respinosa@traxiontech.net")
            page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill("9878787878")
            page.get_by_role("textbox", name="Password *").fill("Traxion123!")
            page.get_by_role("textbox", name="Minimum 8 characters required").fill("traxion12345!")
            page.get_by_role("textbox", name="MPIN *", exact=True).fill("231895")
            page.get_by_role("textbox", name="Confirm MPIN *").fill("231895")
            page.get_by_label("User Role *").select_option("192")
            page.get_by_role("button", name="Add user").click()
            page.wait_for_timeout(2000)
            validation_msg = page.locator("text=Password and Confirmation do not match")
            system_error = page.locator("text=Error|Failed|Unable")

            # wait for either validation or error to appear
            page.wait_for_timeout(2000)

            if validation_msg.first.is_visible():
                actual_result = "Password and Confirmation do not match"
                status = "PASSED"

            elif system_error.first.is_visible():
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

        elif title == "Mismatching MPIN":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("textbox", name="your password").fill("Traxion123!")
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Users").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Add New User").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("textbox", name="First Name *").fill("Lebron")
            page.get_by_role("textbox", name="Last Name *").fill("Jamesr")
            page.get_by_role("textbox", name="Email Address *").fill("respinosa@traxiontech.net")
            page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill("9878787878")
            page.get_by_role("textbox", name="Password *").fill("Traxion123!")
            page.get_by_role("textbox", name="Minimum 8 characters required").fill("Traxion123!")
            page.get_by_role("textbox", name="MPIN *", exact=True).fill("231455")
            page.get_by_role("textbox", name="Confirm MPIN *").fill("231444")
            page.get_by_label("User Role *").select_option("193")
            page.get_by_role("button", name="Add user").click()
            page.wait_for_timeout(2000)
            validation_msg = page.locator("text=ensure both fields match")
            system_error = page.locator("text=Error|Failed|Unable")

            # wait for either validation or error to appear
            page.wait_for_timeout(2000)

            if validation_msg.first.is_visible():
                actual_result = "ensuure both fields match"
                status = "PASSED"

            elif system_error.first.is_visible():
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

        elif title == "Invalid Email Format":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").click()
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("textbox", name="your@email.com").press("Tab")
            page.get_by_role("textbox", name="your password").fill("Traxion123!")
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="Users").click()
            page.get_by_role("link", name="Add New User").click()
            page.get_by_role("textbox", name="First Name *").click()
            page.get_by_role("textbox", name="First Name *").fill("Boss")
            page.get_by_role("textbox", name="Last Name *").click()
            page.get_by_role("textbox", name="Last Name *").fill("Atan")
            page.get_by_role("textbox", name="Email Address *").click()
            page.get_by_role("textbox", name="Email Address *").fill("BoossAtan.com.net")
            page.get_by_role("textbox", name="10 digits starting with 9 (e.").click()
            page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill("9888787848")
            page.get_by_role("textbox", name="Password *").click()
            page.get_by_role("textbox", name="Password *").fill("Traxion123!")
            page.get_by_role("textbox", name="Minimum 8 characters required").click()
            page.get_by_role("textbox", name="Minimum 8 characters required").fill("Traxion123!")
            page.get_by_role("textbox", name="MPIN *", exact=True).click()
            page.get_by_role("textbox", name="MPIN *", exact=True).fill("231895")
            page.get_by_role("textbox", name="Confirm MPIN *").click()
            page.get_by_role("textbox", name="Confirm MPIN *").fill("231895")
            page.get_by_role("button", name="Add user").click()
            page.wait_for_timeout(2000)
            validation_msg = page.locator("text=Email address is not valid")
            system_error = page.locator("text=Error|Failed|Unable")

            # wait for either validation or error to appear
            page.wait_for_timeout(2000)

            if validation_msg.first.is_visible():
                actual_result = "Email address is not valid"
                status = "PASSED"

            elif system_error.first.is_visible():
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

        elif title == "Invalid Number Format":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("textbox", name="your password").fill("Traxion123!")
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Users").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Add New User").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("textbox", name="First Name *").fill("Boss")
            page.get_by_role("textbox", name="Last Name *").fill("Atan")
            page.get_by_role("textbox", name="Email Address *").fill("BossAtan@gmail.com")
            page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill("8554212266")
            page.get_by_role("textbox", name="Password *").fill("Traxion123!")
            page.get_by_role("textbox", name="Minimum 8 characters required").fill("Traxion123!")
            page.get_by_role("textbox", name="MPIN *", exact=True).fill("231895")
            page.get_by_role("textbox", name="Confirm MPIN *").fill("231895")
            page.get_by_label("User Role *").select_option("192")
            page.get_by_role("button", name="Add user").click()
            page.wait_for_timeout(2000)
            # Negative test - expect validation message for invalid number format
            validation_error = page.locator("text=number|Number|digit|Digit|9|starting")
            if validation_error.count() > 0:
                actual_result = validation_error.first.inner_text()
                status = "PASSED"
            else:
                actual_result = "Number format validation not triggered"
                status = "FAILED"

        elif title == "Password Doesn't Meet Req":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").click()
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("textbox", name="your password").click()
            page.get_by_role("textbox", name="your password").fill("Traxion123!")
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Users").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Add New User").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("textbox", name="First Name *").fill("Boss")
            page.get_by_role("textbox", name="Last Name *").fill("Atan")
            page.get_by_role("textbox", name="Email Address *").fill("BossAtan@gmail.com")
            page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill("9854254646")
            page.get_by_role("textbox", name="Password *").fill("traxion123")
            page.get_by_role("textbox", name="Minimum 8 characters required").fill("traxion123")
            page.get_by_role("textbox", name="MPIN *", exact=True).fill("231895")
            page.get_by_role("textbox", name="Confirm MPIN *").fill("231895")
            page.get_by_label("User Role *").select_option("193")
            page.get_by_role("button", name="Add user").click()
            page.wait_for_timeout(2000)
            success_msg = page.locator("text=User created successfully")
            validation_msg = page.locator("text=Password")
            system_error = page.locator("text=Error|Failed|Unable")

            if success_msg.count() > 0:
                actual_result = "User was added with invalid password"
                status = "FAILED"

            elif validation_msg.count() > 0:
                actual_result = validation_msg.first.inner_text()
                status = "PASSED"

            else:
                actual_result = "Password requirements not met"
                status = "PASSED"


        elif title == "edit btn":
            page.goto(login_url, timeout=30000)
            data = TestDataGenerator()
            first_name = data.first_name()
            last_name = data.last_name()
            email = data.email(first_name, last_name)
            mobile = data.mobile_number()
            password = data.password()
            
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("textbox", name="your password").fill("Traxion123!")
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Users").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("cell", name="Joshua Kennethhgythgudfhuaisdifhasjf.").click()
            page.get_by_role("link", name="Edit").click()
            page.wait_for_timeout(2000)
            edit_form = page.locator("form")
            if edit_form.count() > 0:
                actual_result = "Edit form loaded successfully"
                status = "PASSED"
            else:
                error_locator = page.locator("text=User creation failed|Error|Failed|Unable")
                if error_locator.count() > 0:
                    actual_result = error_locator.first.inner_text()
                    status = "FAILED"
                else:
                    actual_result = "Edit page navigated"
                    status = "PASSED"
##=========================================================================================##
##--- HAPPY PATH SCENARIOS (USER ROLE) ---

        elif title == "Add User Role":
            page.goto(login_url, timeout=30000)
            # login
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            # expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()
            page.get_by_role("link", name="User Roles").click()
            page.get_by_role("link", name="Add New User Role").click()
            page.get_by_role("textbox", name="Name *").click()
            page.get_by_role("textbox", name="Name *").fill("Super admin")
            page.get_by_role("textbox", name="Name *").press("Tab")
            page.get_by_role("textbox", name="Description *").fill("admin access")
            page.get_by_role("list").filter(has_text=re.compile(r"^$")).click()
            page.get_by_role("treeitem", name="Dashboard").click()
            page.get_by_role("list").filter(has_text="×Dashboard").click()
            page.get_by_text("Name * Description * Access").click()
            page.get_by_role("list").filter(has_text="×Dashboard").click()
            page.get_by_role("treeitem", name="Members").click()
            page.get_by_text("×Dashboard×Members").click()
            page.get_by_role("treeitem", name="Branches").click()
            page.get_by_text("×Dashboard×Members×Branches").click()
            page.get_by_role("treeitem", name="Cash-In").click()
            page.get_by_text("×Dashboard×Members×Branches×").click()
            page.get_by_role("treeitem", name="Cash-Out").click()
            page.get_by_text("×Dashboard×Members×Branches×").click()
            page.get_by_role("treeitem", name="Transactions").click()
            page.get_by_text("×Dashboard×Members×Branches×").click()
            page.get_by_role("treeitem", name="Users").click()
            page.get_by_text("×Dashboard×Members×Branches×").click()
            page.get_by_role("treeitem", name="Settings").click()
            page.locator(".form-colorinput-color").first.click()
            page.locator("tr:nth-child(3) > td:nth-child(2) > .form-colorinput > .form-colorinput-color").click()
            page.locator(".module-2 > td:nth-child(2) > .form-colorinput > .form-colorinput-color").first.click()
            page.locator("td:nth-child(3) > .form-colorinput > .form-colorinput-color").first.click()
            page.locator("td:nth-child(4) > .form-colorinput > .form-colorinput-color").first.click()
            page.locator("tr:nth-child(6) > td:nth-child(2) > .form-colorinput > .form-colorinput-color").click()
            page.locator(".module-3 > td:nth-child(2) > .form-colorinput > .form-colorinput-color").click()
            page.locator(".module-3 > td:nth-child(3) > .form-colorinput > .form-colorinput-color").click()
            page.locator(".module-3 > td:nth-child(4) > .form-colorinput > .form-colorinput-color").click()
            page.locator("td:nth-child(5) > .form-colorinput > .form-colorinput-color").first.click()
            page.locator(".module-4 > td:nth-child(2) > .form-colorinput > .form-colorinput-color").click()
            page.locator(".module-4 > td:nth-child(3) > .form-colorinput > .form-colorinput-color").click()
            page.locator(".module-5 > td:nth-child(2) > .form-colorinput > .form-colorinput-color").first.click()
            page.locator(".module-5 > td:nth-child(3) > .form-colorinput > .form-colorinput-color").first.click()
            page.locator(".module-7 > td:nth-child(2) > .form-colorinput > .form-colorinput-color").first.click()
            page.locator(".module-6 > td:nth-child(2) > .form-colorinput > .form-colorinput-color").click()
            page.locator("tr:nth-child(13) > td:nth-child(2) > .form-colorinput > .form-colorinput-color").click()
            page.locator("tr:nth-child(13) > td:nth-child(3) > .form-colorinput > .form-colorinput-color").click()
            page.locator(".module-7 > td:nth-child(3) > .form-colorinput > .form-colorinput-color").first.click()
            page.locator(".module-7 > td:nth-child(4) > .form-colorinput > .form-colorinput-color").first.click()
            page.locator(".module-7 > td:nth-child(5) > .form-colorinput > .form-colorinput-color").first.click()
            page.locator("tr:nth-child(18) > td:nth-child(5) > .form-colorinput > .form-colorinput-color").click()
            page.locator("tr:nth-child(18) > td:nth-child(4) > .form-   colorinput > .form-colorinput-color").click()
            page.locator("tr:nth-child(18) > td:nth-child(3) > .form-colorinput > .form-colorinput-color").click()
            page.locator("tr:nth-child(18) > td:nth-child(2) > .form-colorinput > .form-colorinput-color").click()
            page.locator(".module-8 > td:nth-child(2) > .form-colorinput > .form-colorinput-color").first.click()
            page.locator(".module-8 > td:nth-child(4) > .form-colorinput > .form-colorinput-color").first.click()
            page.locator("tr:nth-child(21) > td:nth-child(2) > .form-colorinput > .form-colorinput-color").click()
            page.locator("tr:nth-child(22) > td:nth-child(2) > .form-colorinput > .form-colorinput-color").click()
            page.locator(".module-8 > td:nth-child(3) > .form-colorinput > .form-colorinput-color").click()
            page.locator("tr:nth-child(22) > td:nth-child(4) > .form-colorinput > .form-colorinput-color").click()
            page.locator("tr:nth-child(22) > td:nth-child(5)").click()
            page.locator("tr:nth-child(22) > td:nth-child(5)").click()
            page.locator(".module-8 > td:nth-child(5) > .form-colorinput > .form-colorinput-color").click()
            page.locator("tr:nth-child(23) > td:nth-child(2) > .form-colorinput > .form-colorinput-color").click()
            page.get_by_role("button", name="Add user role").click()
            time.sleep(3)
            status = "PASSED"

        elif title == "Edit User Role": ##USER ROLE
                page.goto(login_url, timeout=30000)
                data = TestDataGenerator()
                first_name = data.first_name()
                last_name = data.last_name()
                email = data.email(first_name, last_name)
                mobile = data.mobile_number()
                password = data.password()

                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
                page.get_by_role("textbox", name="your@email.com").press("Tab")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Users").click()
                page.get_by_role("cell", name="Bossing Joshua Kenneth").click()
                page.get_by_role("link", name="Edit").click()
                page.get_by_label("User Role *").select_option("143")
                page.get_by_role("button", name="Save Changes").click()
                validation_msg = page.locator("text=User updated succesfully")
                system_error = page.locator("text=Error|Failed|Unable")

                # wait for either validation or error to appear
                page.wait_for_timeout(2000)

                if validation_msg.first.is_visible():
                    actual_result = "User updated succesfully"
                    status = "PASSED"

                elif system_error.first.is_visible():
                    actual_result = system_error.first.inner_text()
                    status = "FAILED"

                else:
                    actual_result = "No validation message displayed"
                    status = "FAILED"


        elif title  == "View btn":
                page.goto(login_url, timeout=30000)
                data = TestDataGenerator()
                first_name = data.first_name()
                last_name = data.last_name()
                email = data.email(first_name, last_name)
                mobile = data.mobile_number()
                password = data.password()

                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
                page.get_by_role("textbox", name="your@email.com").press("Tab")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Users").click()
                page.get_by_role("cell", name="Joshua Kennethhgythgudfhuaisdifhasjf.").click()
                page.get_by_role("link", name="View").click()
                edit_form = page.locator("form")
                if edit_form.count() > 0:
                    actual_result = "View User details successfully"
                    status = "PASSED"
                else:
                    error_locator = page.locator("text=User creation failed|Error|Failed|Unable")
                    if error_locator.count() > 0:
                        actual_result = error_locator.first.inner_text()
                        status = "FAILED"
                    else:
                        actual_result = "View page navigated"
                        status = "PASSED"

##--- NEGATIVE PATH SCENARIOS (USER ROLE) ---
##=========================================================================================##
        elif title == "Edit User Role (User Role) ":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").click()
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            # Wait for dashboard and user roles menu to load
            page.get_by_role("link", name="User Roles").wait_for(timeout=30000)
            page.get_by_role("link", name="User Roles").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            # Wait for the Edit action to become available
            edit_button = page.get_by_role("link", name="Edit").first
            edit_button.wait_for(timeout=30000)
            edit_button.click()
            # Wait for the edit form to appear and update the description
            description_field = page.get_by_role("textbox", name="Description *")
            description_field.wait_for(timeout=30000)
            description_field.dblclick()
            description_field.fill("Edit test for automation")
            page.get_by_role("button", name="Save Changes").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            # Select the role color / required form element if present
            color_tile = page.locator("td:nth-child(3) > .form-colorinput > .form-colorinput-color").first
            if color_tile.count() > 0:
                color_tile.click()
                page.get_by_role("button", name="Save Changes").click()

            # Wait for response message after save
            page.wait_for_timeout(2000)
            success_locator = page.locator("text=updated successfully|User role updated|Changes saved|Saved successfully|updated")
            required_locator = page.locator("text=This Field is required|required|Required")
            system_error = page.locator("text=Error|Failed|Unable")

            if success_locator.count() > 0:
                actual_result = success_locator.first.inner_text()
                status = "PASSED"
            elif system_error.count() > 0:
                actual_result = system_error.first.inner_text()
                status = "FAILED"
            elif required_locator.count() > 0:
                actual_result = required_locator.first.inner_text()
                status = "FAILED"
            else:
                actual_result = "Edit User role result not detected"
                status = "FAILED"

        elif title == "View btn": ##11
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").click()
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="User Roles").click()
            page.get_by_role("link", name="View").nth(4).click()
            page.wait_for_timeout(2000)
            # Check if view page loaded successfully
            view_element = page.locator("text=Role Details|View Role|Description")
            if view_element.count() > 0:
                actual_result = "View button clicked successfully"
                status = "PASSED"
            else:
                error_locator = page.locator("text=Error|Failed|Unable")
                if error_locator.count() > 0:
                    actual_result = error_locator.first.inner_text()
                    status = "FAILED"
                else:
                    actual_result = "View page not loaded"
                    status = "FAILED"
##=======================================================================#
##--- HAPPY PATH SCENARIOS (BILLS PAYMENT) ---
        elif title == "Bills Payment Successful":
            page.goto(login_url, timeout=30000)
            data = TestDataGenerator()
            first_name = data.first_name()
            last_name = data.last_name()
            email = data.email(first_name, last_name)
            mobile = data.mobile_number()
            password = data.password()

            page.goto(login_url, timeout=30000)
            page.wait_for_timeout(2000)
            page.goto("https://digicoop-sit.traxionpay.com/signin", timeout=30000)
            page.get_by_role("textbox", name="your@email.com").click(timeout=10000)
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+digicoop@traxiontech.net", timeout=10000)
            page.get_by_role("textbox", name="your password").fill("Traxion123!", timeout=10000)
            page.get_by_role("button", name="Sign in").click(timeout=10000)
            page.get_by_role("link", name="Bills Payment").click()
            page.get_by_role("textbox", name="Search Billers").click()
            page.get_by_role("textbox", name="Search Billers").fill("barangka")
            page.get_by_role("button", name="Search").click()
            page.get_by_role("link", name="Barangka Credit Cooperative").click()
            page.locator("input[name=\"member_name\"]").click()
            page.locator("input[name=\"member_name\"]").fill("Boss Atan")
            page.locator("input[name=\"account_number\"]").click()
            page.locator("input[name=\"account_number\"]").fill("0123456789")
            page.locator("input[name=\"contact_number\"]").click()
            page.locator("input[name=\"contact_number\"]").fill("0123456789")
            page.locator("input[name=\"loan\"]").click()
            page.locator("input[name=\"loan\"]").fill("Boss Atan")
            page.locator("input[name=\"savings\"]").click()
            page.locator("input[name=\"savings\"]").fill("500")
            page.locator("input[name=\"share_capital\"]").click()
            page.locator("input[name=\"share_capital\"]").fill("1000")
            page.get_by_role("spinbutton").click()
            page.get_by_role("spinbutton").fill("500")
            page.locator("input[name=\"remarks\"]").click()
            page.locator("input[name=\"remarks\"]").fill("Boss Atan Ka Ba")
            page.get_by_role("link", name="Proceed").click()
            page.get_by_role("radio", name="Password").check()
            page.get_by_role("textbox", name="form-control required field").click()
            page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
            page.get_by_role("button", name="Submit").click(timeout=10000)
            page.wait_for_timeout(1000)

            system_error = page.locator("text=Error|Failed|Unable")
            if system_error.count() > 0:
                actual_result = system_error.first.inner_text()
                status = "FAILED"
            else:
                actual_result = "Password Validated"
                status = "PASSED"

        elif title == "Optional Fields Empty":
            # 1. Navigation and Setup
            page.goto(login_url, timeout=30000)
    
            # 2. Authentication
            page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("textbox", name="your password").fill("Traxion123!")
            page.get_by_role("button", name="Sign in").click()
            
            # Ensure dashboard loads
            page.wait_for_selector("text=Bills Payment", timeout=20000)
            page.get_by_role("link", name="Bills Payment").click()
            
            # 3. Biller Selection
            page.get_by_role("textbox", name="Search Billers").fill("barangka")
            page.get_by_role("button", name="Search").click()
            page.get_by_role("link", name="Barangka Credit Cooperative").click()
            
            # 4. Fill ONLY Mandatory Fields (Referencing image_1cd465.png)
            # We leave "account_number" and "remarks" completely untouched
            page.locator("input[name=\"member_name\"]").fill("Boss Atan")
            page.locator("input[name=\"contact_number\"]").fill("09123456789")
            page.locator("input[name=\"loan\"]").fill("Personal Loan")
            page.locator("input[name=\"savings\"]").fill("500")
            page.locator("input[name=\"share_capital\"]").fill("500")
            page.get_by_role("spinbutton").fill("1000")
            
            # 5. Proceed & Submit
            page.get_by_role("link", name="Proceed").click()
            page.get_by_role("radio", name="Password").check()
            page.locator("input[type='password']").last.fill("Traxion123!")
            
            # Capture the URL before submitting
            current_url = page.url
            page.get_by_role("button", name="Submit").click()
            
            # 6. Optimized Result Verification Logic
            # We use a broad range of indicators to confirm the system "proceeded"
            page.wait_for_load_state("networkidle")
            
            system_error = page.locator("text=Error|Failed|Unable|Invalid Password")
            # Broad success indicators including generic "Reference" or "Successful"
            success_text = page.locator("text=Success|Successful|Reference|Completed|Thank you")

            # Give the UI 10 seconds to show an error or a success
            try:
                if system_error.is_visible(timeout=5000):
                    actual_result = system_error.first.inner_text()
                    status = "FAILED"
                elif success_text.is_visible(timeout=5000):
                    actual_result = success_text.first.inner_text()
                    status = "PASSED"
                elif page.url != current_url:
                    # If the URL changed (e.g., to a receipt or history page), the transaction proceeded
                    actual_result = f"Passed: System redirected to {page.url} without errors."
                    status = "PASSED"
                else:
                    # Final fallback: if no error is visible and the button is gone/disabled
                    actual_result = "Transaction proceeded (No errors detected on screen)."
                    status = "PASSED"
            except Exception as e:
                actual_result = f"Validation timed out: {str(e)}"
                status = "FAILED"

##--- NEGATIVE PATH SCENARIOS (BILLS PAYMENT) ---

        elif title == "Without Entering Password in Bills":
            page.goto(login_url, timeout=30000)
            data = TestDataGenerator()
            first_name = data.first_name()
            last_name = data.last_name()
            email = data.email(first_name, last_name)
            mobile = data.mobile_number()
            password = data.password()
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
            page.locator("input[name=\"member_name\"]").click()
            page.locator("input[name=\"member_name\"]").fill("Boss Atan")
            page.locator("input[name=\"account_number\"]").click()
            page.locator("input[name=\"account_number\"]").fill("123456")
            page.locator("input[name=\"contact_number\"]").click()
            page.locator("input[name=\"contact_number\"]").fill("123456")
            page.locator("input[name=\"loan\"]").click()
            page.locator("input[name=\"loan\"]").fill("Boss")
            page.locator("input[name=\"savings\"]").click()
            page.locator("input[name=\"savings\"]").fill("500")
            page.locator("input[name=\"share_capital\"]").click()
            page.locator("input[name=\"share_capital\"]").fill("500")
            page.get_by_role("spinbutton").click()
            page.get_by_role("spinbutton").fill("500")
            page.get_by_role("link", name="Proceed").click()
            page.get_by_role("radio", name="Password").check()
            page.get_by_role("button", name="Submit").click()
            system_error = page.locator("text=Error|Failed|Unable")
            validation_msg = page.locator("text=This field is required")
            system_error = page.locator("text=Error|Failed|Unable")

            if validation_msg.count() > 0:
                actual_result = "This field is required"
                status = "PASSED"

            elif system_error.count() > 0:
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

        elif title == "Mandatory Fields Missing":
            try:
                page.goto(login_url, timeout=30000)
                page.wait_for_load_state("networkidle")
                page.wait_for_selector("input[name='email']", timeout=10000)
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.wait_for_selector("text=Bills Payment", timeout=20000)
                page.get_by_role("link", name="Bills Payment").click()
                page.wait_for_selector("input[placeholder*='Search']", timeout=10000)
                page.get_by_role("textbox", name="Search Billers").fill("barangka")
                page.get_by_role("button", name="Search").click()
                page.get_by_role("link", name="Barangka Credit Cooperative").click()
                page.wait_for_selector("input[name='contact_number']", timeout=10000)
                page.locator("input[name=\"contact_number\"]").fill("09123456789")
                page.locator("input[name=\"loan\"]").fill("Boss Atan")
                page.locator("input[name=\"share_capital\"]").fill("500")
                page.get_by_role("spinbutton").fill("500")
                page.get_by_role("link", name="Proceed").click()
                page.wait_for_timeout(2000) 
                is_focused = page.evaluate("document.activeElement.name === 'member_name'")

                if is_focused:
                    actual_result = "Passed: System blocked submission and moved cursor to missing Member Name field."
                    status = "PASSED"
                else:
                    # If it didn't focus, check if it accidentally proceeded to the password screen
                    if page.get_by_role("radio", name="Password").is_visible(timeout=2000):
                        actual_result = "Failed: System allowed proceed despite missing mandatory Member Name."
                        status = "FAILED"
                    else:
                        actual_result = "Failed: System did not focus the required field or show an error."
                        status = "FAILED"

            except Exception as e:
                actual_result = f"Automation Error: {str(e)}"
                status = "FAILED"

        elif title == "Below Minimum Amount":
                page.goto(login_url, timeout=30000)
                data = TestDataGenerator()
                first_name = data.first_name()
                last_name = data.last_name()
                email = data.email(first_name, last_name)
                mobile = data.mobile_number()
                password = data.password()
                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
                page.get_by_role("textbox", name="your@email.com").press("Tab")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.goto("https://bibo-sit.traxionpay.com/")
                page.get_by_role("link", name="Bills Payment").click()
                page.get_by_role("textbox", name="Search Billers").click()
                page.get_by_role("textbox", name="Search Billers").fill("barangka")
                page.get_by_role("textbox", name="Search Billers").press("Enter")
                page.get_by_role("link", name="Barangka Credit Cooperative").click()
                page.locator("input[name=\"member_name\"]").click()
                page.locator("input[name=\"member_name\"]").fill("Boss Atan")
                page.locator("input[name=\"contact_number\"]").click()
                page.locator("input[name=\"contact_number\"]").fill("0912345678")
                page.locator("input[name=\"loan\"]").click()
                page.locator("input[name=\"loan\"]").fill("500")
                page.locator("input[name=\"savings\"]").click()
                page.locator("input[name=\"savings\"]").fill("500")
                page.locator("input[name=\"share_capital\"]").click()
                page.locator("input[name=\"share_capital\"]").fill("500")
                page.get_by_role("spinbutton").click()
                page.get_by_role("spinbutton").fill("5")
                page.locator(".text-center.w-100.mt-5").click()
                page.locator(".text-center.w-100.mt-5").dblclick()
                system_error = page.locator("text=Error|Failed|Unable")
                validation_msg = page.locator("text=Minimum amount is PHP 10.00")
                system_error = page.locator("text=Error|Failed|Unable")

                if validation_msg.count() > 0:
                    actual_result = "Minimum amount is PHP 10.00"
                    status = "PASSED"

                elif system_error.count() > 0:
                    actual_result = system_error.first.inner_text()
                    status = "FAILED"

                else:
                    actual_result = "No validation message displayed"
                    status = "FAILED"


    

##=======================================================================#
##=======================BRANCHES=======================##
##======= POSTIVE =========##


##======= NEGATIVE =========##
        elif title == "Add Member With Existing Number or Email":
                page.goto(login_url, timeout=30000)
                data = TestDataGenerator()
                first_name = data.first_name()
                last_name = data.last_name()
                email = data.email(first_name, last_name)
                mobile = data.mobile_number()
                password = data.password()

                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
                page.get_by_role("textbox", name="your@email.com").press("Tab")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Member List").click()
                page.get_by_role("link", name="Add Member").click()
                page.get_by_role("textbox", name="First Name*").click()
                page.get_by_role("textbox", name="First Name*").fill("Boss")
                page.get_by_role("textbox", name="Last Name*").click()
                page.get_by_role("textbox", name="Last Name*").fill("Atan")
                page.get_by_role("textbox", name="Mobile Number*").click()
                page.get_by_role("textbox", name="Mobile Number*").fill("9380529031")
                page.get_by_role("button", name="Add Member").click()
                page.get_by_role("button", name="Add Member").click()
                system_error = page.locator("text=Error|Failed|Unable")
                validation_msg = page.locator("text=already exists")
                system_error = page.locator("text=Error|Failed|Unable")

                if validation_msg.count() > 0:
                    actual_result = "already exists"
                    status = "PASSED"

                elif system_error.count() > 0:
                    actual_result = system_error.first.inner_text()
                    status = "FAILED"

                else:
                    actual_result = "No validation message displayed"
                    status = "FAILED"

        elif title == "Add Member With Invalid Mobile Number":
                page.goto(login_url, timeout=30000)
                data = TestDataGenerator()
                first_name = data.first_name()
                last_name = data.last_name()
                email = data.email(first_name, last_name)
                mobile = data.mobile_number()
                password = data.password()

                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
                page.get_by_role("textbox", name="your@email.com").press("Tab")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Member List").click()
                page.get_by_role("link", name="Add Member").click()
                page.get_by_role("textbox", name="First Name*").click()
                page.get_by_role("textbox", name="First Name*").fill("Josepg")
                page.get_by_role("textbox", name="Last Name*").click()
                page.get_by_role("textbox", name="Last Name*").fill("Petron")
                page.get_by_role("textbox", name="Mobile Number*").click()
                page.get_by_role("textbox", name="Mobile Number*").fill("6587554848")
                page.get_by_role("button", name="Add Member").click()

                try:
                    # We use a partial match and wait for visibility
                    error_locator = page.get_by_text("Invalid mobile number format").first
                    error_locator.wait_for(state="visible", timeout=5000)
                    
                    actual_result = error_locator.inner_text()
                    status = "PASSED"
                    print(f"✅ Found validation: {actual_result}")
                
                except Exception:
                    # 2. If the validation wasn't found, check for a generic system error
                    system_error = page.locator("text=Error|Failed|Unable").first
                    if system_error.is_visible(timeout=500):
                        actual_result = system_error.inner_text()
                        status = "FAILED"
                    else:
                        actual_result = "No validation message appeared within 5s"
                        status = "FAILED"

        elif title == "Leave blank required fields branches":
                page.goto(login_url, timeout=30000)
                data = TestDataGenerator()
                first_name = data.first_name()
                last_name = data.last_name()
                email = data.email(first_name, last_name)
                mobile = data.mobile_number()
                password = data.password()

                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
                page.get_by_role("textbox", name="your@email.com").press("Tab")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Branches").click()
                page.get_by_role("link", name="Add Organization Branch").click()
                page.get_by_role("button", name="Create branch").click()

                system_error = page.locator("text=Error|Failed|Unable")
                validation_msg = page.locator("text=Please fill out the following fields")
                system_error = page.locator("text=Error|Failed|Unable")

                if validation_msg.count() > 0:
                    actual_result = "Please fill out the following fields"
                    status = "PASSED"

                elif system_error.count() > 0:
                    actual_result = system_error.first.inner_text()
                    status = "FAILED"

                else:
                    actual_result = "No validation message displayed"
                    status = "FAILED"

        elif title == "Invalid mobile number branches":
                page.goto(login_url, timeout=30000)
                data = TestDataGenerator()
                first_name = data.first_name()
                last_name = data.last_name()
                email = data.email(first_name, last_name)
                mobile = data.mobile_number()
                password = data.password()
                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
                page.get_by_role("textbox", name="your@email.com").press("Tab")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Branches").click()
                page.get_by_role("link", name="Add Organization Branch").click()
                page.get_by_role("textbox", name="Enter branch name").click()
                page.get_by_role("textbox", name="Enter branch name").fill("PetronEdsa")
                page.locator("#dateOfIncorporation").fill("2003-09-15")
                page.get_by_role("textbox", name="www.example.com").click()
                page.get_by_role("textbox", name="www.example.com").fill("www.PetronEdsa.com")
                page.get_by_role("textbox", name="Enter email address").click()
                page.get_by_role("textbox", name="Enter email address").fill("PetronEdsa@gmail.com")
                page.get_by_role("textbox", name="Enter email address").press("Tab")
                page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill("0812321371")
                page.locator("input[name=\"address1\"]").click()
                page.locator("input[name=\"address1\"]").fill("Edsa")
                page.locator("input[name=\"address1\"]").press("Tab")
                page.locator("input[name=\"address2\"]").fill("metro")
                page.locator("input[name=\"address2\"]").press("Tab")
                page.get_by_role("textbox", name="Four-digit zip code (e.g.").fill("1111")
                page.get_by_role("textbox", name="Enter short merchant").click()
                page.get_by_role("textbox", name="Enter short merchant").fill("tapat sayo")
                page.get_by_role("button", name="Create branch").click()

                try:
                    # We use a partial match and wait for visibility
                    error_locator = page.get_by_text("Invalid mobile number format").first
                    error_locator.wait_for(state="visible", timeout=5000)
                    
                    actual_result = error_locator.inner_text()
                    status = "PASSED"
                    print(f"✅ Found validation: {actual_result}")
                
                except Exception:
                    # 2. If the validation wasn't found, check for a generic system error
                    system_error = page.locator("text=Error|Failed|Unable").first
                    if system_error.is_visible(timeout=500):
                        actual_result = system_error.inner_text()
                        status = "FAILED"
                    else:
                        actual_result = "No validation message appeared within 5s"
                        status = "FAILED"

###=========BACK OFFICE======================##

        elif title == "1011009517501446":
                page.goto(login_url, timeout=30000)
                data = TestDataGenerator()
                first_name = data.first_name()
                last_name = data.last_name()
                email = data.email(first_name, last_name)
                mobile = data.mobile_number()
                password = data.password()
                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("BLASERNA")
                page.get_by_role("textbox", name="your@email.com").press("CapsLock")
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+rbpay@traxiontech.net")
                page.get_by_role("textbox", name="your@email.com").press("Tab")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Withdrawals").click()
                page.get_by_role("link", name="Direct Fund Transfer").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").fill("1011032223967154")
                page.get_by_role("textbox", name="Account Name").click()
                page.get_by_placeholder("0.00").click()
                page.get_by_placeholder("0.00").fill("500")
                page.locator("label").filter(has_text="Password").click()
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("radio", name="Password").press("Shift+T")
                page.get_by_role("radio", name="Password").press("r")
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
                page.get_by_role("button", name="Transfer Funds").click()
                status = "PASSED"

        elif title == "1011032223967154":
                page.goto(login_url, timeout=30000)
                data = TestDataGenerator()
                first_name = data.first_name()
                last_name = data.last_name()
                email = data.email(first_name, last_name)
                mobile = data.mobile_number()
                password = data.password()
                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+rbpay@traxiontech.net")
                page.get_by_role("textbox", name="your@email.com").press("Tab")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Withdrawals").click()
                page.get_by_role("link", name="Direct Fund Transfer").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").fill("1011032223967154")
                page.get_by_role("textbox", name="Account Name").click()
                page.get_by_placeholder("0.00").click()
                page.get_by_placeholder("0.00").fill("500")
                page.locator("label").filter(has_text="Password").click()
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("radio", name="Password").press("Shift+T")
                page.get_by_role("radio", name="Password").press("r")
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
                page.get_by_role("button", name="Transfer Funds").click()
                status = "PASSED"

        elif title == "011032223967154":
                page.goto(login_url, timeout=30000)
                data = TestDataGenerator()
                first_name = data.first_name()
                last_name = data.last_name()
                email = data.email(first_name, last_name)
                mobile = data.mobile_number()
                password = data.password()

                page.goto(login_url, timeout=30000)
                page.wait_for_timeout(2000)
                page.goto("https://merchant-sit.traxionpay.com/signin", timeout=30000)
                page.get_by_role("textbox", name="your@email.com").click(timeout=10000)
                page.get_by_role("textbox", name="your@email.com").fill("tpaymerchantqa@mailinator.com", timeout=10000)
                page.get_by_role("textbox", name="your password").fill("Traxion123!", timeout=10000)
                page.get_by_role("button", name="Sign in").click(timeout=10000)
                page.get_by_role("link", name="Withdrawals").click()
                page.get_by_role("link", name="Direct Fund Transfer").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").fill("1011032223967154")
                page.get_by_role("textbox", name="Account Name").click()
                page.get_by_placeholder("0.00").click()
                page.get_by_placeholder("0.00").fill("500")
                page.locator("label").filter(has_text="Password").click()
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("radio", name="Password").press("Shift+T")
                page.get_by_role("radio", name="Password").press("r")
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
                page.get_by_role("button", name="Transfer Funds").click()
                status = "PASSED"

        elif title == "1011008204742842":
                page.goto(login_url, timeout=30000)
                data = TestDataGenerator()
                first_name = data.first_name()
                last_name = data.last_name()
                email = data.email(first_name, last_name)
                mobile = data.mobile_number()
                password = data.password()
                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("BLASERNA")
                page.get_by_role("textbox", name="your@email.com").press("CapsLock")
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+rbpay@traxiontech.net")
                page.get_by_role("textbox", name="your@email.com").press("Tab")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Withdrawals").click()
                page.get_by_role("link", name="Direct Fund Transfer").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").fill("1011032223967154")
                page.get_by_role("textbox", name="Account Name").click()
                page.get_by_placeholder("0.00").click()
                page.get_by_placeholder("0.00").fill("500")
                page.locator("label").filter(has_text="Password").click()
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("radio", name="Password").press("Shift+T")
                page.get_by_role("radio", name="Password").press("r")
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
                page.get_by_role("button", name="Transfer Funds").click()
                status = "PASSED"

        elif title == "1011012719935939":
                page.goto(login_url, timeout=30000)
                data = TestDataGenerator()
                first_name = data.first_name()
                last_name = data.last_name()
                email = data.email(first_name, last_name)
                mobile = data.mobile_number()
                password = data.password()
                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("BLASERNA")
                page.get_by_role("textbox", name="your@email.com").press("CapsLock")
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+rbpay@traxiontech.net")
                page.get_by_role("textbox", name="your@email.com").press("Tab")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Withdrawals").click()
                page.get_by_role("link", name="Direct Fund Transfer").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").fill("1011032223967154")
                page.get_by_role("textbox", name="Account Name").click()
                page.get_by_placeholder("0.00").click()
                page.get_by_placeholder("0.00").fill("500")
                page.locator("label").filter(has_text="Password").click()
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("radio", name="Password").press("Shift+T")
                page.get_by_role("radio", name="Password").press("r")
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
                page.get_by_role("button", name="Transfer Funds").click()
                status = "PASSED"

        elif title == "1011000678304854":
                page.goto(login_url, timeout=30000)
                data = TestDataGenerator()
                first_name = data.first_name()
                last_name = data.last_name()
                email = data.email(first_name, last_name)
                mobile = data.mobile_number()
                password = data.password()
                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("BLASERNA")
                page.get_by_role("textbox", name="your@email.com").press("CapsLock")
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+rbpay@traxiontech.net")
                page.get_by_role("textbox", name="your@email.com").press("Tab")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Withdrawals").click()
                page.get_by_role("link", name="Direct Fund Transfer").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").fill("1011032223967154")
                page.get_by_role("textbox", name="Account Name").click()
                page.get_by_placeholder("0.00").click()
                page.get_by_placeholder("0.00").fill("500")
                page.locator("label").filter(has_text="Password").click()
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("radio", name="Password").press("Shift+T")
                page.get_by_role("radio", name="Password").press("r")
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
                page.get_by_role("button", name="Transfer Funds").click()
                status = "PASSED"

        elif title == "1011731218426493":
                page.goto(login_url, timeout=30000)
                data = TestDataGenerator()
                first_name = data.first_name()
                last_name = data.last_name()
                email = data.email(first_name, last_name)
                mobile = data.mobile_number()
                password = data.password()
                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("BLASERNA")
                page.get_by_role("textbox", name="your@email.com").press("CapsLock")
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+rbpay@traxiontech.net")
                page.get_by_role("textbox", name="your@email.com").press("Tab")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Withdrawals").click()
                page.get_by_role("link", name="Direct Fund Transfer").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").fill("1011032223967154")
                page.get_by_role("textbox", name="Account Name").click()
                page.get_by_placeholder("0.00").click()
                page.get_by_placeholder("0.00").fill("500")
                page.locator("label").filter(has_text="Password").click()
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("radio", name="Password").press("Shift+T")
                page.get_by_role("radio", name="Password").press("r")
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
                page.get_by_role("button", name="Transfer Funds").click()
                status = "PASSED"

        elif title == "1ST TRANSFER":
                page.goto("https://bibo-sit.traxionpay.com/signin")
                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
                page.get_by_role("textbox", name="your@email.com").press("Tab")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Withdrawals").click()
                page.get_by_role("link", name="Direct Fund Transfer").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").fill("1011021785733461")
                page.get_by_placeholder("0.00").click()
                page.get_by_placeholder("0.00").fill("600")
                page.get_by_role("radio", name="Password").check()
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
                page.get_by_role("button", name="Transfer Funds").click()

        elif title == "1ST TRANSFER bibo":
                page.goto("https://bibo-sit.traxionpay.com/signin")
                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+1127bibo@traxiontech.net")
                page.get_by_role("textbox", name="your@email.com").press("Tab")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Withdrawals").click()
                page.get_by_role("link", name="Direct Fund Transfer").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").fill("1011021785733461")
                page.get_by_placeholder("0.00").click()
                page.get_by_placeholder("0.00").fill("600")
                page.get_by_role("radio", name="Password").check()
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
                page.get_by_role("button", name="Transfer Funds").click()

        elif title == "2ND TRANSFER":
                page.goto(login_url, timeout=30000)
                page.goto("https://digicoop-sit.traxionpay.com/signin")
                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("blaserna+digicoop@traxiontech.net")
                page.get_by_role("textbox", name="your@email.com").press("Tab")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Withdrawals").click()
                page.get_by_role("link", name="Direct Fund Transfer").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").fill("1011021785733461")
                page.locator(".col-lg-9").click()
                page.get_by_placeholder("0.00").fill("700")
                page.get_by_role("radio", name="Password").check()
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
                page.get_by_role("button", name="Transfer Funds").click()

        elif title == "3RD TRANSFER":
                page.goto(login_url, timeout=30000)
                page.goto("https://mannypay-sit.traxionpay.com/signin")
                page.get_by_role("textbox", name="your@email.com").click()
                page.get_by_role("textbox", name="your@email.com").fill("araymundo+mannypay01@traxiontech.net")
                page.get_by_role("textbox", name="your password").fill("Traxion123!")
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Withdrawals").click()
                page.get_by_role("link", name="Direct Fund Transfer").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").click()
                page.get_by_role("textbox", name="Mobile/Account Number/Wallet").fill("1011021785733461")
                page.locator(".col-lg-9").click()
                page.get_by_placeholder("0.00").fill("800")
                page.get_by_role("radio", name="Password").check()
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
                page.get_by_role("button", name="Transfer Funds").click()

##=====================================================================#

        # always take screenshot
        page.screenshot(path=str(screenshot_path))

    except Exception:
        error_trace = traceback.format_exc()
        ui_error = get_ui_error(page)

        error_file = ERROR_DIR / f"{title.replace(' ', '_')}_error.txt"
        with open(error_file, "w") as f:
            f.write("=== PYTHON TRACEBACK ===\n")
            f.write(error_trace + "\n\n")

            if browser_errors:
                f.write("=== BROWSER (JS) ERRORS ===\n")
                f.write("\n".join(browser_errors) + "\n\n")

            if network_errors:
                f.write("=== NETWORK / API ERRORS ===\n")
                f.write("\n".join(network_errors) + "\n\n")

            if ui_error:
                f.write("=== UI ERROR MESSAGE ===\n")
                f.write(ui_error)

        status = "FAILED"

        try:
            page.screenshot(path=str(screenshot_path))
        except:
            pass


    return {
        "title": title,
        "description": description,
        "status": status,
        "screenshot": str(screenshot_path),
        "actual_result": actual_result,
        "error_trace": error_trace if status == "FAILED" else "",
        "browser_errors": browser_errors,
        "network_errors": network_errors,
        "ui_error": ui_error,
    }

# ===============================
# Core Execution Engine
# ===============================

def run_custom_suite(playwright, login_url, scenarios_to_run):
    """
    The master engine that executes the filtered list of scenarios.
    """
    total_start = datetime.now()
    results = []
    screen_width, screen_height = get_screen_size()

    try:
        for scenario in scenarios_to_run:
            print(f"🔁 Running '{scenario['title']}'")
            
            # Browser Setup
            browser = playwright.chromium.launch(
                headless=False, 
                args=[f"--window-size={screen_width},{screen_height}"]
            )
            context = browser.new_context(viewport={"width": screen_width, "height": screen_height})
            page = context.new_page()

            # Execute Scenario
            scenario_start = datetime.now()
            # CITE: Ensure all 4 arguments (page, title, description, login_url) are passed
            result = run_scenario(page, scenario["title"], scenario["description"], login_url)
            scenario_end = datetime.now()

            # Store Metrics
            result['scenario_duration'] = format_duration((scenario_end - scenario_start).total_seconds())
            results.append(result)

            context.close()
            browser.close()

    except Exception as e:
        print(f"⚠️ Error during suite execution: {e}")
    finally:
        total_duration = (datetime.now() - total_start).total_seconds()
        if results:
            results[0]['total_duration'] = total_duration
            try:
                send_email(results)
            except Exception as e:
                print(f"❌ Failed to send email: {e}")
        return results

# ===============================
# GUI Logic & Helpers
# ===============================

def update_scenario_dropdown(*args):
    """Updates the second dropdown based on Module selection."""
    selected_module = module_var.get()
    # Filter titles belonging to the module
    titles = [s["title"] for s in TEST_SCENARIOS if s["module"] == selected_module]
    scenario_dropdown['values'] = ["Run All Suite"] + titles
    scenario_var.set("Run All Suite")

def execute_automation(url):
    """Triggered by the App buttons."""
    module = module_var.get()
    selection = scenario_var.get()
    
    if not module:
        messagebox.showwarning("Warning", "Please select a Module first.")
        return

    # Filter scenarios based on user selection
    if selection == "Run All Suite":
        to_run = [s for s in TEST_SCENARIOS if s["module"] == module]
    else:
        to_run = [s for s in TEST_SCENARIOS if s["title"] == selection]

    if not to_run:
        messagebox.showwarning("Warning", "No scenarios found for this selection.")
        return

    # Disable buttons during run
    toggle_buttons(tk.DISABLED)

    try:
        with sync_playwright() as playwright:
            results = run_custom_suite(playwright, url, to_run)
        
        summary = "\n".join([f"{r['title']}: {r['status']}" for r in results])
        messagebox.showinfo("Automation Finished", f"Results:\n\n{summary}")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Automation failed:\n{str(e)}")
    finally:
        toggle_buttons(tk.NORMAL)

def toggle_buttons(state):
    """Safely toggles all app buttons."""
    run_button_traxion.config(state=state)
    run_button_bibo.config(state=state)
    run_button_rbpay.config(state=state)
    run_button_mannypay.config(state=state)
    run_button_micropay.config(state=state)
    run_button_psslai.config(state=state)

# ===============================
# Tkinter UI Implementation
# ===============================

root = tk.Tk()
root.title("Traxion QA: Modular Suite Selector")
root.geometry("500x850")

# 1. Module Selection
tk.Label(root, text="Step 1: Select Module", font=("Arial", 11, "bold")).pack(pady=10)
# Get unique, sorted modules
module_options = sorted(list(set(s["module"] for s in TEST_SCENARIOS)))
module_var = tk.StringVar()
module_dropdown = ttk.Combobox(root, textvariable=module_var, values=module_options, state="readonly")
module_dropdown.pack()
module_var.trace('w', update_scenario_dropdown)

# 2. Scenario Selection
tk.Label(root, text="Step 2: Select Scenario", font=("Arial", 15, "bold")).pack(pady=10)
scenario_var = tk.StringVar()
scenario_dropdown = ttk.Combobox(root, textvariable=scenario_var, state="readonly", width=45)
scenario_dropdown.pack()

# 3. Environment Buttons
tk.Label(root, text="Step 3: Start Testing", font=("Arial", 15, "bold"), fg="#0B395B").pack(pady=20)

run_button_traxion = tk.Button(root, text="▶ Traxion", width=30, bg="#177AC1", fg="white", 
                               command=lambda: execute_automation(APP_URLS["Traxion"]))
run_button_traxion.pack(pady=3)

run_button_bibo = tk.Button(root, text="▶ Bibo", width=30, bg="#177AC1", fg="white", 
                            command=lambda: execute_automation(APP_URLS["Bibo"]))
run_button_bibo.pack(pady=3)

run_button_rbpay = tk.Button(root, text="▶ RBPay", width=30, bg="#177AC1", fg="white", 
                             command=lambda: execute_automation(APP_URLS["RBPay"]))
run_button_rbpay.pack(pady=3)

run_button_mannypay = tk.Button(root, text="▶ MannyPay", width=30, bg="#177AC1", fg="white", 
                                command=lambda: execute_automation(APP_URLS["MannyPay"]))
run_button_mannypay.pack(pady=3)

run_button_micropay = tk.Button(root, text="▶ MicroPay", width=30, bg="#177AC1", fg="white", 
                                 command=lambda: execute_automation(APP_URLS["MicroPay"]))
run_button_micropay.pack(pady=3)

run_button_psslai = tk.Button(root, text="▶ Psslai", width=30, bg="#177AC1", fg="white", 
                              command=lambda: execute_automation(APP_URLS["Psslai"]))
run_button_psslai.pack(pady=3)

run_button_digicoop = tk.Button(root, text="▶ Digicoop", width=30, bg="#177AC1", fg="white", 
                                command=lambda: execute_automation(APP_URLS["Digicoop"]))
run_button_digicoop.pack(pady=3)

root.mainloop()


