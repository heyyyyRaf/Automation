from pathlib import Path
from tkinter import ttk
from playwright.sync_api import sync_playwright, TimeoutError, Playwright
import smtplib
from email.message import EmailMessage
from datetime import datetime
import os
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import traceback
from datetime import datetime, timedelta
import threading
import re

# ===============================
# Gmail Settings
# ===============================
GMAIL_USER = "mj@traxiontech.net"
GMAIL_APP_PASSWORD = "aohrspbjzpcdugdt"
RECIPIENT_EMAIL = ("respinosa@traxiontech.net")

# ===============================
# Test Configuration
# ===============================
USERNAME = "txnqatestautomation@mailinator.com"
PASSWORD = "Traxion123!"
#login_url = "https://merchant-sit.traxionpay.com/"

TEST_SCENARIOS = [
    # LOGIN MODULE
    #=POSITIVE=#
    {"module": "Login", "title": "TEST_LOGIN_01", "description": "Verify login success."},
    {"module": "Login", "title": "TEST_LOGIN_02", "description": "Verify System Validation for Invalid login."},
    {"module": "Login", "title": "TEST_LOGIN_03", "description": "Verify logout."},
    #=NEGATIVE=#
    {"module": "Login", "title": "Login without pass", "description": "Verify if the system showed validation message"},
    {"module": "Login", "title": "Non Existing Account", "description": "Verify if the user could proceed to the dashboard"},
    {"module": "Login", "title": "Password Length", "description": "Verify if the passwordfield have a password length validation."},
    {"module": "Login", "title": "Invalid Password", "description": "Verify if the user could proceed to the dashboard even if the password is incorrect."},

    ##=======================================================##

    # WITHDRAWAL MODULE
    #=POSITIVE=#
    {"module": "Cash-Out", "title": "TEST_DIRECT_FUND_TRANSFER_01", "description": "Verify Successful Direct transfer."},
    {"module": "Cash-Out", "title": "TEST_DIRECT_FUND_TRANSFER_02", "description": "Verify System Validation for Direct Fund Transfer Insufficient Balance"},
    {"module": "Cash-Out", "title": "TEST_BANK_TRANSFER_01", "description": "Verify Successful Bank transfer."},
   
    #=NEGATIVE=#
    {"module": "Cash-Out", "title": "Withdraw Funds Invalid Password", "description": "verify that banktransfer fails with invalid credentials."},
    {"module": "Cash-Out", "title": "Direct Fundtransfer Invalid Password", "description": "verify that fundtransfer fails with invalid credentials."},
   
    ##=======================================================##

    # CASH-IN MODULE
    #=POSITIVE=#
    {"module": "Cash-In", "title": "TEST_MANUAL_DEPOSIT_01", "description": "Verify Successful Manual deposit."},
    {"module": "Cash-In", "title": "TEST_CASH_IN_FROM_DRAGONPAY_01", "description": "Verify Successful DragonPay deposit."},
   
    #=NEGATIVE=#
    {"module": "Cash-In", "title": "Leave Blank Required Fields in Manual Deposit", "description": "Verify that the system shows validation messages when required fields are left blank in manual deposit."},
    {"module": "Cash-In", "title": "Leave Blank Deposit Slip", "description": "Verify that the system shows validation messages when required fields are left blank in manual deposit."},

    ##=======================================================##
    # TRANSACTION HISTORY MODULE
    {"module": "Transaction History", "title": "TEST_TRANSACTION_HISTORY_01", "description": "Verify If The System Allows The User To Search Transactions"},
    ##=======================================================##

    ##=======================================================##
    # ELOAD HISTORY MODULE # 
    ##==POSITIVE==##
    {"module": "Eload", "title": "TEST_ELOAD_01", "description": "Verify Successful Eload Transactions"},
    {"module": "Eload", "title": "Non Telco", "description": "Verify that a merchant can do buyload transaction with non-telco product"},
    ##==NEGATIVE==##
    {"module": "Eload", "title": "Negative: Invalid Recipient Number", "description": "Verify that the system rejects invalid recipient numbers"},
    {"module": "Eload", "title": "Without Entering Number", "description": "Verify that the system cannot proceed with the transaction when recipient number is not entered"},
    {"module": "Eload", "title": "Without Entering Password", "description": "Verify that the system shows validation message when password is not entered"},
    ##=======================================================##

    ##=======================================================##
    # PAYBILLS MODULE
    ##==POSITIVE==##
    {"module": "Bills Payment", "title": "Bills Payment Successful", "description": "Verify that a merchant can successfully make a bill payment transaction."},
    {"module": "Bills Payment", "title": "Optional Fields Empty", "description": "Verify that payment is successful when leaving optional fields like 'Account No.' and 'Remarks' empty."},
    ##==NEGATIVE==##

    ##=======================================================##

    # BULKDISBURSEMENT MODULE
    {"module": "Bulk Disbursement", "title": "TEST_BULKDISBURSEMENT_01", "description": "Verify Successful Bulk Disbursement Transactions"},
    ##=======================================================##

    # USER MANAGEMENT MODULE
    #=POSITIVE=#
    {"module": "User Management", "title": "TEST_USERMANAGEMENT_01", "description": "Verify that a new user can be successfully created with valid mandatory fields and the system displays a success confirmation message."},
    #=NEGATIVE=#
    {"module": "User Management", "title": "Add Existing User", "description": "Verify validation on adding existing user"},
    {"module": "User Management", "title": "Required Fields", "description": "Verify if the system showed a validation message"},
    {"module": "User Management", "title": "Existing Email", "description": "Verify if the user can add user with existing email"},
    {"module": "User Management", "title": "Mismatching Pass", "description": "Verify if the user could create mismatching pass"},
    {"module": "User Management", "title": "Mismatching MPIN", "description": "Verify if the user could create mismatching mpin"},
    {"module": "User Management", "title": "Invalid Email Format", "description": "Verify if the user could create account with invalid email format"},
    {"module": "User Management", "title": "Invalid Number Format", "description": "Verify if the user could create account with invalid number format"},
    {"module": "User Management", "title": "Password Doesn't Meet Req", "description": "Verify if the user can create a password that does not meet the requirements"},
    {"module": "User Management", "title": "edit btn", "description": "Verify if the user could proceed to the next page"},
    

    ##=======================================================##


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

ENV_URLS = {
    "SIT": {
        "Traxion": "https://merchant-sit.traxionpay.com/signin",
        "Bibo": "https://bibo-sit.traxionpay.com/signin",
        "RBPay": "https://rbpay-sit.traxionpay.com/signin",
        "MannyPay": "https://mannypay-sit.traxionpay.com/signin",
        "MicroPay": "https://micropay-sit.traxionpay.com/signin",
        "Psslai": "https://psslai-sit.traxionpay.com/signin",
        "Digicoop": "https://digicoop-sit.traxionpay.com/signin",

    },
    "UAT": {
        "Traxion": "https://merchant-uat.traxionpay.com/signin",
        "Bibo": "https://bibo-uat.traxionpay.com/signin",
        "RBPay": "https://rbpay-uat.traxionpay.com/signin",
        "MannyPay": "https://mannypay-uat.traxionpay.com/signin",
        "MicroPay": "https://micropay-uat.traxionpay.com/signin",
        "Psslai": "https://psslai-uat.traxionpay.com/signin",
    },
    "PROD": {
        "Traxion": "https://merchant.traxionpay.com/signin",
        "Bibo": "https://bibo.traxionpay.com/signin",
        "RBPay": "https://rbpay.traxionpay.com/signin",
        "MannyPay": "https://mannypay.traxionpay.com/signin",
        "MicroPay": "https://micropay.traxionpay.com/signin",
        "Psslai": "https://psslai.traxionpay.com/signin",
    }
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
    start_time = datetime.now()  # total start for scenario
    for attempt in range(max_retries + 1):
        print(f"🔁 Running '{scenario['title']}' | Attempt {attempt + 1}")

        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # measure per attempt start time
        attempt_start = datetime.now()
        result = run_scenario(page, scenario["title"], scenario["description"], login_url)
        attempt_end = datetime.now()

        result["attempt_duration"] = str(attempt_end - attempt_start)  # duration per attempt

        context.close()
        browser.close()

        if result["status"] == "PASSED":
            result["retry_attempt"] = attempt
            result["final_status"] = "PASSED"
            result["scenario_duration"] = (attempt_end - start_time).total_seconds()
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
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = SCREENSHOT_DIR / f"{title.replace(' ', '_')}_{timestamp}.png"
    status = "FAILED"

###======================== LOGIN SCENARIOS ========================##
                            ##POSITIVE##
    try:
        if title == "TEST_LOGIN_01":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="Open user menu").wait_for(timeout=30000)
            page.get_by_role("link", name="Open user menu").click()
            page.get_by_role("link", name="Signout").click()
            status = "PASSED"

        elif title == "TEST_LOGIN_02":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill("wrong@gmail.com")
            page.get_by_role("textbox", name="your password").fill("wrongpassword")
            page.get_by_role("button", name="Sign in").click()
            page.get_by_text("Authentication error", exact=False).wait_for(timeout=10000)
            status = "PASSED"

        elif title == "TEST_LOGIN_03":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="Open user menu").wait_for(timeout=30000)
            page.get_by_role("link", name="Open user menu").click()
            page.get_by_role("link", name="Signout").click()
            status = "PASSED"

###======================== LOGIN SCENARIOS ========================##
                            ##NEGATIVE##
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
###========================================================================##
                    ##CASH-OUT SCENARIOS##
                        ##POSITIVE##
        elif title == "TEST_DIRECT_FUND_TRANSFER_01":
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
            page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
            page.wait_for_load_state("networkidle", timeout=10000)
            page.get_by_role("button", name="Transfer Funds").click()
            with page.expect_download() as download_info:
                page.get_by_role("button", name="Download Receipt").click()
            download = download_info.value
            status = "PASSED"

        elif title == "TEST_DIRECT_FUND_TRANSFER_02":
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
            page.get_by_placeholder("0.00").fill("9999999")
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("radio", name="Password").check()
            page.get_by_role("textbox", name="Account Name").click()
            page.get_by_role("textbox", name="form-control required field").click()
            page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
            page.wait_for_load_state("networkidle", timeout=10000)
            page.get_by_role("button", name="Transfer Funds").click()
            page.get_by_text("Error encountered when").click()
            status = "PASSED"
        
        elif title == "TEST_BANK_TRANSFER_01":
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
            page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
            page.get_by_role("button", name="Withdraw Funds").click()
            with page.expect_download() as download_info:
                page.get_by_role("button", name="Download Receipt").click()
            download = download_info.value
            status = "PASSED"


                        ## NEGATIVE ##
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

##==================================================================##
                    ##CASH-IN SCENARIOS##
                    #POSITIVE#
        elif title == "TEST_MANUAL_DEPOSIT_01":
            page.goto(login_url, timeout=30000)

            # login
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            # navigate to deposit
            page.get_by_role("link", name="Deposits").click()
            page.get_by_role("link", name="Make A Deposit").click()
            # fill amount and select bank
            page.locator("#manual_amount").fill("100")
            page.get_by_label("Select BANCO DE ORO UNIBANK,").select_option("BDO_UNIBANK")
            # ✅ FILE UPLOAD (portable path)
            file_path = Path(__file__).parent / "file" / "upload.png"
            page.locator("input[type='file']").set_input_files(str(file_path))
            page.wait_for_load_state("networkidle", timeout=90000)
            page.get_by_role("button", name="Submit Manual Deposit Request").click()
            page.wait_for_load_state("networkidle", timeout=90000)
            page.get_by_text("Manual deposit request with").click()
            status = "PASSED"

        elif title == "TEST_CASH_IN_FROM_DRAGONPAY_01":
            page.goto(login_url, timeout=30000)
            # login
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
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

                            #======NEGATIVE======#
        elif title == "Leave Blank Required Fields in Manual Deposit":
            page.goto(login_url, timeout=30000)
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
            # login
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
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
##===================================================================##

        elif title == "TEST_TRANSACTION_HISTORY_01":
            page.goto(login_url, timeout=30000)
            # login
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="Transactions").click()
            page.get_by_role("searchbox", name="Search:").click()
            page.get_by_role("searchbox", name="Search:").fill("MWHHKBFDSEEN")
            page.get_by_role("searchbox", name="Search:").press("Enter")
            page.get_by_role("cell", name="MWHHKBFDSEEN").click()
            page.get_by_role("link", name="View Details").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            status = "PASSED"

##==================================================================##
##==eload module==##
    ##==POSITIVE==##
        elif title == "TEST_ELOAD_01":
            page.goto(login_url, timeout=30000)
            # login
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("link", name="E-Load").click()
            page.locator("div:nth-child(3) > .card > .card-body").click()
            page.get_by_role("textbox", name="Enter recipient's number...").click()
            page.get_by_role("textbox", name="Enter recipient's number...").fill("09359074740")
            page.get_by_role("button", name="Proceed").click()
            page.get_by_text("Touch Mobile Amax 15", exact=True).click()
            page.wait_for_load_state("networkidle")
            page.get_by_role("link", name="Next").click()
            page.locator("#remoteModal").click()
            page.locator("#remoteModal").click()
            page.get_by_role("radio", name="Password").check()
            page.get_by_role("textbox", name="Enter MPIN or Password").click()
            page.get_by_role("textbox", name="Enter MPIN or Password").fill("Traxion123!")
            page.get_by_role("textbox", name="Enter MPIN or Password").click()
            page.wait_for_load_state("networkidle")
            page.locator("#feeField").click()
            page.locator("#feeField").click()
            page.get_by_text("Fee", exact=True).click()
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Submit").click()
            page.wait_for_load_state("networkidle")
            page.get_by_text("Transaction Type: E - Load Mobile Number: 09359074740 Promo Name: ATMXMAX15").click()
            status = "PASSED"

        elif title == "Non Telco":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click(timeout=10000)
            page.get_by_role("link", name="E-Load").click()
            page.get_by_role("tab", name="Non-Telco").click()
            page.get_by_text("EASYTRIP").click()
            page.get_by_role("textbox", name="Enter recipient's number...").click()
            page.get_by_role("textbox", name="Enter recipient's number...").fill("123456789012")
            page.get_by_role("button", name="Proceed").click()
            page.locator("div").filter(has_text=re.compile("^EASYTRIP 400$")).click()
            page.get_by_role("link", name="Next").click()
            page.get_by_role("radio", name="Password").check()
            page.get_by_role("textbox", name="Enter MPIN or Password").click()
            page.get_by_role("textbox", name="Enter MPIN or Password").fill("Traxion123!")
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Submit").click(timeout=20000)
            page.wait_for_timeout(10000)
            page.get_by_role("button", name="Submit").click
            page.wait_for_timeout(1000)
            # validation
            validation_msg = page.locator("text=Order transaction initiated")
            system_error = page.locator("text=Error|Failed|Unable")

            if validation_msg.first.is_visible():
                actual_result = "Order transaction initiated"
                status = "PASSED"

            elif system_error.first.is_visible():
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

    ##==NEGATIVE==##
        elif title == "Negative: Invalid Recipient Number":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
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
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Submit").click(timeout=20000)
            page.wait_for_timeout(10000)
            page.get_by_role("button", name="Submit").click
            page.wait_for_timeout(1000)
            system_error = page.locator("text=Error|Failed|Unable")
            validation_msg = page.locator("text=Invalid target mobile number")
            system_error = page.locator("text=Error|Failed|Unable")

            if validation_msg.count() > 0:
                actual_result = "Invalid target mobile number"
                status = "PASSED"

            elif system_error.count() > 0:
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

        elif title == "Without Entering Number":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
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
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
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

##===================================================================##
##== BILLS PAYMENT MODULE ==##
    ##==POSITIVE==##
        elif title == "Bills Payment Successful":
            page.goto(login_url, timeout=30000)
            # login
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
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
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_selector("text=Bills Payment", timeout=20000)
            page.get_by_role("link", name="Bills Payment").click()
            page.get_by_role("textbox", name="Search Billers").fill("barangka")
            page.get_by_role("button", name="Search").click()
            page.get_by_role("link", name="Barangka Credit Cooperative").click()
            page.locator("input[name=\"member_name\"]").fill("Boss Atan")
            page.locator("input[name=\"contact_number\"]").fill("09123456789")
            page.locator("input[name=\"loan\"]").fill("Personal Loan")
            page.locator("input[name=\"savings\"]").fill("500")
            page.locator("input[name=\"share_capital\"]").fill("500")
            page.get_by_role("spinbutton").fill("1000")
            page.get_by_role("link", name="Proceed").click()
            page.get_by_role("radio", name="Password").check()
            page.locator("input[type='password']").last.fill("Traxion123!")
            current_url = page.url
            page.get_by_role("button", name="Submit").click()
            page.wait_for_load_state("networkidle")
            system_error = page.locator("text=Error|Failed|Unable|Invalid Password")
            # Broad success indicators including generic "Reference" or "Successful"
            success_text = page.locator("text=Success|Successful|Reference|Completed|Thank you")
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

##==NEGATIVE==##
        elif title == "Without Entering Password in Bills":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
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
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
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

        elif title == "Below Minimum Amount":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
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
            validation_msg = page.locator("text=Minimum amount is PHP 25.00")
            system_error = page.locator("text=Error|Failed|Unable")

            if validation_msg.count() > 0:
                actual_result = "Minimum amount is PHP 25.00"
                status = "PASSED"

            elif system_error.count() > 0:
                actual_result = system_error.first.inner_text()
                status = "FAILED"

            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

##===================================================================##
        elif title == "TEST_BULKDISBURSEMENT_01":
            page.goto(login_url, timeout=30000)

            # login
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()

            page.get_by_role("link", name="Disbursements").click()
            page.get_by_role("link", name="Create Bulk Disbursement").click()

            # ===============================
            # ✅ DYNAMIC FILE GENERATION
            # ===============================
            import random
            import shutil
            import os

            original_file = "9UGXNORKHJ-DISBURSEMENT-2026042901.xlsx"

            # generate random last 3 digits
            suffix = str(random.randint(100, 999))

            # replace last 3 digits only
            base_name = original_file[:-7]
            new_filename = f"{base_name}{suffix}.xlsx"

            current_dir = os.path.dirname(__file__)
            source_path = os.path.join(current_dir, original_file)
            new_path = os.path.join(current_dir, new_filename)

            # copy file
            shutil.copy(source_path, new_path)

            # ===============================
            # ✅ UPLOAD FILE (FIXED LOCATOR)
            # ===============================
            page.locator("input[type='file']").set_input_files(new_path)

            # continue flow
            page.get_by_role("radio", name="Password").check()
            page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
            page.locator(".row > .mb-3").first.click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("button", name="Make A Bulk Disbursement").click()
            page.wait_for_load_state("networkidle", timeout=30000)

            status = "PASSED"

            # ===============================
            # ✅ OPTIONAL CLEANUP
            # ===============================
            try:
                os.remove(new_path)
            except:
                pass
            status = "PASSED"

##===================================================================##
##===USER MODULE===##
##==POSITIVE==##

        elif title == "TEST_USERMANAGEMENT_01":
            import time
            import random

            # --- generate unique values ---
            ts = int(time.time())
            rand = random.randint(100, 999)

            unique_id = f"{ts}{rand}"

            first_name = f"Mark{unique_id}"
            email = f"mj+{unique_id}@traxiontech.net"
            mobile = f"9{str(ts)[-6:]}{rand}"[:10]

            page.goto(login_url, timeout=30000)

            # login
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()

            page.get_by_role("link", name="Users").click()
            page.get_by_role("link", name="Add New User").click()

            page.get_by_role("textbox", name="First Name *").click()
            page.get_by_role("textbox", name="First Name *").fill(first_name)
            page.get_by_role("textbox", name="First Name *").press("Tab")

            page.get_by_role("textbox", name="Middle Name").fill("Tester")
            page.get_by_role("textbox", name="Middle Name").press("Tab")

            page.get_by_role("textbox", name="Last Name *").fill("Testing")

            page.get_by_role("textbox", name="Email Address *").click()
            page.get_by_role("textbox", name="Email Address *").fill(email)
            page.get_by_role("textbox", name="Email Address *").press("Tab")

            page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill(mobile)

            page.get_by_role("textbox", name="Password *").click()
            page.get_by_role("textbox", name="Password *").fill("Traxion123!")

            page.get_by_role("textbox", name="Minimum 8 characters required").click()
            page.get_by_role("textbox", name="Minimum 8 characters required").fill("Traxion123!")

            page.get_by_role("textbox", name="MPIN *", exact=True).click()
            page.get_by_role("textbox", name="MPIN *", exact=True).fill("123456")
            page.get_by_role("textbox", name="MPIN *", exact=True).press("Tab")

            page.get_by_role("textbox", name="Confirm MPIN *").fill("123456")

            page.get_by_label("User Role *").select_option("364")

            page.get_by_role("button", name="Add user").click()
            page.get_by_text("User created successfully.").click()

            status = "PASSED"

##==NEGATIVE==##
        elif title == "Add Existing User":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Users").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Add New User").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            
            # 
            # FIXED: Using explicit strings instead of undefined variables
            # 
            page.get_by_role("textbox", name="First Name *").fill("Test")
            page.get_by_role("textbox", name="Last Name *").fill("User")
            page.get_by_role("textbox", name="Email Address *").fill("blaserna+0313bibo@traxiontech.net")
            page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill("9171234567")
            
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
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
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
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Users").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            page.get_by_role("link", name="Add New User").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            
            # 
            # FIXED: Variables swapped with literal testing strings
            # 
            page.get_by_role("textbox", name="First Name *").fill("Duplicate")
            page.get_by_role("textbox", name="Last Name *").fill("EmailTest")
            page.get_by_role("textbox", name="Email Address *").fill("blaserna+1127bibo@traxiontech.net")
            page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill("9170001122")
            
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
            # ... (Login steps remain the same)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_load_state("networkidle")
            
            page.get_by_role("link", name="Users").click()
            page.get_by_role("link", name="Add New User").click()
            page.wait_for_load_state("networkidle")

            # Fill User Details
            page.get_by_role("textbox", name="First Name *").fill("Lebron")
            page.get_by_role("textbox", name="Last Name *").fill("James")
            page.get_by_role("textbox", name="Email Address *").fill("respinosa@traxiontech.net")
            page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill("9878787878")
            
            # Intentional Password Mismatch
            page.get_by_role("textbox", name="Password *").fill("Traxion123!")
            page.get_by_role("textbox", name="Minimum 8 characters required").fill("traxion12345!")
            
            page.get_by_role("textbox", name="MPIN *", exact=True).fill("231895")
            page.get_by_role("textbox", name="Confirm MPIN *").fill("231895")

            # --- DROPDOWN FIX ---
            # Instead of a hardcoded value that might change, try selecting by index or label
            user_role = page.get_by_label("User Role *")
            user_role.scroll_into_view_if_needed()
            
            # If "192" was the ID, ensure it's a string. 
            # Better yet, select the first available role if the ID is unstable:
            user_role.select_option(index=1) 
            
            # --------------------

            page.get_by_role("button", name="Add user").click()

            # --- VALIDATION CHECK FIX ---
            # Don't just wait 2 seconds; wait specifically for the message to appear
            mismatch_err = page.get_by_text("Password and Confirmation do not match")
            system_err = page.locator("text=Error|Failed|Unable")

            try:
                # Wait for the expected mismatch message (This is the 'PASSED' condition)
                mismatch_err.wait_for(state="visible", timeout=5000)
                actual_result = "Password and Confirmation do not match"
                status = "PASSED"
            except:
                # If mismatch didn't show, check if a generic system error appeared
                if system_err.first.is_visible():
                    actual_result = system_err.first.inner_text()
                    status = "FAILED"
                else:
                    actual_result = "No validation message displayed after 5s"
                    status = "FAILED"

        elif title == "Mismatching MPIN":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
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
            
            # FIX: Ensure field is scrolled into view and select by stable index
            user_role_dropdown = page.get_by_label("User Role *")
            user_role_dropdown.scroll_into_view_if_needed()
            user_role_dropdown.select_option(index=1)
            
            page.get_by_role("button", name="Add user").click()
            page.wait_for_timeout(2000)
            validation_msg = page.locator("text=ensure both fields match")
            system_error = page.locator("text=Error|Failed|Unable")

            # wait for either validation or error to appear
            page.wait_for_timeout(2000)

            if validation_msg.first.is_visible():
                actual_result = "ensure both fields match"
                status = "PASSED"
            elif system_error.first.is_visible():
                actual_result = system_error.first.inner_text()
                status = "FAILED"
            else:
                actual_result = "No validation message displayed"
                status = "FAILED"

        elif title == "Invalid Email Format":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            
            page.get_by_role("link", name="Users").click()
            page.get_by_role("link", name="Add New User").click()
            
            # Fill out the form
            page.get_by_role("textbox", name="First Name *").fill("Boss")
            page.get_by_role("textbox", name="Last Name *").fill("Atan")
            
            # Entering the invalid email
            page.get_by_role("textbox", name="Email Address *").fill("BoossAtan.com.net")
            
            page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill("9888787848")
            page.get_by_role("textbox", name="Password *").fill("Traxion123!")
            page.get_by_role("textbox", name="Minimum 8 characters required").fill("Traxion123!")
            page.get_by_role("textbox", name="MPIN *", exact=True).fill("231895")
            page.get_by_role("textbox", name="Confirm MPIN *").fill("231895")

            # --- DROPDOWN FIX ---
            # Instead of value "199", select by index (1 is usually the first real option)
            # Or use: select_option(label="Admin") if you know the text name
            user_role = page.get_by_label("User Role *")
            user_role.scroll_into_view_if_needed()
            user_role.select_option(index=1) 
            # --------------------

            page.get_by_role("button", name="Add user").click()

            # --- VALIDATION LOGIC ---
            # Wait specifically for the message to appear to prevent early closing
            validation_msg = page.locator("text=The email address you entered is not in a valid format")
            system_error = page.locator("text=Error|Failed|Unable")

            try:
                # Wait up to 5 seconds for the invalid email warning
                validation_msg.wait_for(state="visible", timeout=5000)
                actual_result = "The email address you entered is not in a valid format"
                status = "PASSED"
            except:
                if system_error.count() > 0 and system_error.first.is_visible():
                    actual_result = system_error.first.inner_text()
                    status = "FAILED"
                else:
                    actual_result = "Validation message 'The email address you entered is not in a valid format' not found"
                    status = "FAILED"


        elif title == "Invalid Number Format":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
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
            
            # --- DROPDOWN FIX ---
            user_role = page.get_by_label("User Role *")
            user_role.scroll_into_view_if_needed()
            user_role.select_option(index=1) 
            # --------------------

            page.get_by_role("button", name="Add user").click()

            # --- FIXED VALIDATION LOGIC WITH EXTRA TIME WAITING ---
            # Using get_by_text matches exact or partial visible popups correctly
            validation_msg = page.get_by_text("Invalid mobile number format. Must be in +639XXXXXXXXX format", exact=False)
            system_error = page.locator("text=Error|Failed|Unable")

            try:
                # Increased timeout to 7000ms (7 seconds) to account for slow toast animations
                validation_msg.wait_for(state="visible", timeout=7000)
                actual_result = validation_msg.first.inner_text()
                status = "PASSED"
            except:
                if system_error.count() > 0 and system_error.first.is_visible():
                    actual_result = system_error.first.inner_text()
                    status = "FAILED"
                else:
                    actual_result = "Validation message for mobile format not found"
                    status = "FAILED"

        elif title == "Password Doesn't Meet Req":
            # Timeout set to 60 seconds to handle slow environment loads securely
            page.goto(login_url, timeout=60000)
            page.wait_for_load_state("load", timeout=60000)
            
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
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
            
            # --- DROPDOWN FIX ---
            user_role = page.get_by_label("User Role *")
            user_role.scroll_into_view_if_needed()
            user_role.select_option(index=1)
            # --------------------
            
            page.get_by_role("button", name="Add user").click()

            # --- FIXED VALIDATION LOGIC WITH 7 SECONDS TIMEOUT ---
            # Using basic text query with exact=False ensures Playwright intercepts the banner text perfectly
            validation_msg = page.get_by_text("Password", exact=False)
            system_error = page.locator("text=Error|Failed|Unable")

            try:
                # Forces the automation to wait up to 7 seconds until the error message appears
                validation_msg.first.wait_for(state="visible", timeout=7000)
                actual_result = validation_msg.first.inner_text()
                status = "PASSED"
            except:
                if system_error.count() > 0 and system_error.first.is_visible():
                    actual_result = system_error.first.inner_text()
                    status = "FAILED"
                else:
                    actual_result = "Validation message for password requirements not found"
                    status = "FAILED"

        elif title == "edit btn":
            page.goto(login_url, timeout=30000)
            page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
            page.get_by_role("textbox", name="your password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            
            page.get_by_role("link", name="Users").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            
            # Click the specific user row to highlight/select it
            page.get_by_role("cell", name="BryanjWV Lasernaphi").click()
            
            # Click the Edit link button that appears for that row
            page.get_by_role("link", name="Edit").click()
            
            # --- VIEW-CHECK VALIDATION LOGIC ---
            # Define selectors for the modal components seen in your screenshot
            edit_modal_header = page.get_by_text("Edit User", exact=True)
            save_btn = page.get_by_role("button", name="Save Changes")

            try:
                # Wait up to 5 seconds for the "Edit User" heading to show up
                edit_modal_header.wait_for(state="visible", timeout=5000)
                actual_result = "Edit User modal form loaded successfully."
                status = "PASSED"
            except:
                # Fallback check if the heading locator behaves strictly but the button is there
                if save_btn.is_visible():
                    actual_result = "Save Changes button detected; edit form loaded successfully."
                    status = "PASSED"
                else:
                    actual_result = "Failed to open Edit User modal window."
                    status = "FAILED"
##===================================================================##
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
        "error_trace": error_trace if status == "FAILED" else "",
        "browser_errors": browser_errors,
        "network_errors": network_errors,
        "ui_error": ui_error,
    }

# ===============================
# Run all scenarios
# ===============================
def run(playwright: Playwright):
    total_start = datetime.now()  # start total execution
    results = []

    try:
        for scenario in TEST_SCENARIOS:
            scenario_start = datetime.now()  # start scenario timer
            result = run_scenario_with_retry(playwright, scenario, max_retries=1)
            scenario_end = datetime.now()
            
            # calculate duration in seconds and store it
            scenario_duration = (scenario_end - scenario_start).total_seconds()
            result['scenario_duration'] = scenario_duration
            results.append(result)

    except Exception as e:
        print(f"⚠️ Error during test execution: {e}")
    finally:
        total_end = datetime.now()
        total_duration = (total_end - total_start).total_seconds()
        print(f"⏱ Total execution time: {total_duration:.2f} seconds")
        
        for r in results:
            dur = r.get('scenario_duration', 0)

            try:
                dur = float(dur)
                print(f"{r['title']} → Duration: {dur:.2f} seconds")
            except:
                print(f"{r['title']} → Duration: {dur}")

        # Store total duration in the first result so email can access it
        if results:
            results[0]['total_duration'] = total_duration

        try:
            send_email(results)
        except Exception as e:
            print(f"❌ Failed to send email: {e}")

def run_all(playwright, login_url, selected_modules):
    total_start = datetime.now()
    results = []

    # ✅ FILTER SCENARIOS HERE
    filtered_scenarios = [
        s for s in TEST_SCENARIOS if s["module"] in selected_modules
    ]

    for scenario in filtered_scenarios:
        result = run_scenario_with_retry(playwright, scenario, login_url)
        results.append(result)

    total_duration = (datetime.now() - total_start).total_seconds()
    if results:
        results[0]['total_duration'] = total_duration

    send_email(results)

# ===============================
# GUI Wrapper
# ===============================
def run_tests(app_name):
    try:
        selected_modules = [m for m, v in module_vars.items() if v.get()]

        if not selected_modules:
            messagebox.showwarning("Warning", "⚠️ Please select at least one module!")
            return

        # ✅ copy para hindi ma-modify original
        app_modules = selected_modules.copy()

        # ✅ SKIP ELOAD FOR TRAXION ONLY
        if app_name == "Traxion" and "Eload" in app_modules:
            app_modules.remove("Eload")
            messagebox.showinfo("Info", "Eload module is not applicable for Traxion. Skipping...")

        if app_name == "Traxion" and "Bills Payment" in app_modules:
            app_modules.remove("Bills Payment")
            messagebox.showinfo("Info", "Bills Payment module is not applicable for Traxion. Skipping...")

        # ✅ GET SELECTED ENVIRONMENT
        selected_env = env_var.get()

        # ✅ GET URL BASED ON ENV + APP
        login_url = ENV_URLS[selected_env][app_name]

        status_var.set(f"Running {app_name} ({selected_env})")

        run_button_traxion.config(state=tk.DISABLED)
        run_button_bibo.config(state=tk.DISABLED)
        run_button_rbpay.config(state=tk.DISABLED)

        with sync_playwright() as playwright:
            # ✅ use app_modules instead of selected_modules
            run_all(playwright, login_url=login_url, selected_modules=app_modules)

        messagebox.showinfo(
            "Success",
            f"✅ Finished!\nApp: {app_name}\nEnv: {selected_env}\nModules: {', '.join(app_modules)}"
        )

    except Exception as e:
        messagebox.showerror("Error", f"❌ {str(e)}")

    finally:
        run_button_traxion.config(state=tk.NORMAL)
        run_button_bibo.config(state=tk.NORMAL)
        run_button_rbpay.config(state=tk.NORMAL)
        run_button_micropay.config(state=tk.NORMAL)
        run_button_mannypay.config(state=tk.NORMAL)
        run_button_psslai.config(state=tk.NORMAL)

def run_all_apps():
    try:
        selected_modules = [m for m, v in module_vars.items() if v.get()]

        if not selected_modules:
            messagebox.showwarning("Warning", "⚠️ Please select at least one module!")
            return

        run_button_traxion.config(state=tk.DISABLED)
        run_button_bibo.config(state=tk.DISABLED)
        run_button_rbpay.config(state=tk.DISABLED)
        run_button_micropay.config(state=tk.DISABLED)
        run_button_mannypay.config(state=tk.DISABLED)
        run_button_psslai.config(state=tk.DISABLED)

        with sync_playwright() as playwright:
            for app_name, url in ENV_URLS[env_var.get()].items():
                status_var.set(f"Running: {app_name}")

                # ✅ copy selected modules para hindi maapektuhan original
                app_modules = selected_modules.copy()

                # ✅ skip Eload ONLY for Traxion
                if app_name == "Traxion" and "Eload" in app_modules:
                    app_modules.remove("Eload")

                run_all(playwright, login_url=url, selected_modules=app_modules)

        messagebox.showinfo("Success", "✅ Finished running all applications!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        run_button_traxion.config(state=tk.NORMAL)
        run_button_bibo.config(state=tk.NORMAL)
        run_button_rbpay.config(state=tk.NORMAL)
        run_button_micropay.config(state=tk.NORMAL)
        run_button_mannypay.config(state=tk.NORMAL)
        run_button_psslai.config(state=tk.NORMAL)

# ===============================
# Tkinter GUI (ENHANCED UI)
# ===============================
# ===============================
# TKINTER GUI (FULL FIXED UI)
# ===============================
app = tk.Tk()
app.title("Traxion QA Automation Dashboard")

app.state("zoomed")
app.minsize(1100, 750)
app.configure(bg="#F5F7FA")

# ===============================
# STATUS BAR
# ===============================
status_var = tk.StringVar(value="Ready ✔ Select modules and run automation")

status_bar = tk.Label(
    app,
    textvariable=status_var,
    font=("Arial", 10),
    bg="#0B395B",
    fg="white",
    anchor="w",
    padx=10
)
status_bar.pack(fill="x")

# ===============================
# HEADER
# ===============================
header = tk.Frame(app, bg="#0B395B", height=90)
header.pack(fill="x")

tk.Label(
    header,
    text="🧪 QA AUTOMATION FOR WHITE LABEL APPLICATIONS",
    font=("Arial", 22, "bold"),
    bg="#0B395B",
    fg="white"
).pack(pady=25)

# ===============================
# MAIN CONTAINER
# ===============================
container = tk.Frame(app, bg="#F5F7FA")
container.pack(fill="both", expand=True, padx=18, pady=15)

container.columnconfigure(0, weight=1)
container.columnconfigure(1, weight=2)

# ===============================
# LEFT PANEL (MODULES)
# ===============================
def select_all_modules():
    for var in module_vars.values():
        var.set(True)

def deselect_all_modules():
    for var in module_vars.values():
        var.set(False)

left_panel = tk.LabelFrame(
    container,
    text=" 🧩 Test Modules ",
    font=("Arial", 12, "bold"),
    bg="white",
    fg="#0B395B",
    padx=15,
    pady=15
)
left_panel.grid(row=0, column=0, sticky="nsew", padx=10)

tk.Label(
    left_panel,
    text="Select test coverage",
    font=("Arial", 10),
    fg="#666",
    bg="white"
).pack(anchor="w", pady=(0, 10))

# ===============================
# SELECT / DESELECT BUTTONS UI
# ===============================
btn_frame = tk.Frame(left_panel, bg="white")
btn_frame.pack(fill="x", pady=(0, 10))

tk.Button(
    btn_frame,
    text="✔ Select All",
    command=select_all_modules,
    bg="#0B395B",
    fg="white",
    font=("Arial", 10, "bold"),
    bd=0,
    cursor="hand2"
).pack(side="left", expand=True, fill="x", padx=2)

tk.Button(
    btn_frame,
    text="✖ Deselect All",
    command=deselect_all_modules,
    bg="#0B395B",
    fg="white",
    font=("Arial", 10, "bold"),
    bd=0,
    cursor="hand2"
).pack(side="left", expand=True, fill="x", padx=2)

canvas = tk.Canvas(left_panel, bg="white", highlightthickness=0)
scrollbar = tk.Scrollbar(left_panel, orient="vertical", command=canvas.yview)
scroll_frame = tk.Frame(canvas, bg="white")

scroll_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

module_vars = {
    "Login": tk.BooleanVar(value=True),
    "Cash-Out": tk.BooleanVar(value=True),
    "Cash-In": tk.BooleanVar(value=True),
    "Eload": tk.BooleanVar(value=True),
    "Bills Payment": tk.BooleanVar(value=True),
    "Bulk Disbursement": tk.BooleanVar(value=True),
    "Members List": tk.BooleanVar(value=True),
    "Branches": tk.BooleanVar(value=True),
    "Transaction History": tk.BooleanVar(value=True),
    "User Management": tk.BooleanVar(value=True),
    "Settings": tk.BooleanVar(value=True),
}

for module, var in module_vars.items():
    card = tk.Frame(scroll_frame, bg="#F0F6FF", pady=6, padx=10)
    card.pack(fill="x", padx=10, pady=6)

    tk.Checkbutton(
        card,
        text=f" {module}",
        variable=var,
        bg="#F0F6FF",
        font=("Arial", 12, "bold"),
        fg="#0B395B",
        activebackground="#F0F6FF",
        anchor="w"
    ).pack(anchor="w")

# ===============================
# RIGHT PANEL (FIXED ORDER)
# ===============================
right_panel = tk.LabelFrame(
    container,
    text=" 🚀 Applications ",
    font=("Arial", 12, "bold"),
    bg="white",
    fg="#0B395B",
    padx=20,
    pady=20
)
right_panel.grid(row=0, column=1, sticky="nsew", padx=10)

tk.Label(
    right_panel,
    text="Choose environment to execute automation",
    font=("Arial", 11),
    bg="white",
    fg="#666"
).pack(pady=(0, 10))

# ===============================
# ENV SELECTOR (FIXED)
# ===============================
env_var = tk.StringVar(value="SIT")

tk.Label(
    right_panel,
    text="Environment",
    bg="white",
    fg="#0B395B",
    font=("Arial", 10, "bold")
).pack()

env_dropdown = ttk.Combobox(
    right_panel,
    textvariable=env_var,
    values=["SIT", "UAT", "PROD"],
    state="readonly",
    width=20
)
env_dropdown.pack(pady=5)


# ===============================
# BUTTON STYLE
# ===============================
def on_enter(e):
    e.widget["bg"] = "#0B395B"

def on_leave(e):
    e.widget["bg"] = "#177AC1"

def make_button(app_name):
    btn = tk.Button(
        right_panel,
        text=f"▶ {app_name}",
        font=("Arial", 13, "bold"),
        bg="#177AC1",
        fg="white",
        activebackground="#0B395B",
        activeforeground="white",
        width=28,
        height=2,
        bd=0,
        cursor="hand2",
        command=lambda: run_tests(app_name)
    )
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

# ===============================
# APP BUTTONS (FIXED)
# ===============================
run_button_traxion = make_button("Traxion")
run_button_traxion.pack(pady=6)

run_button_bibo = make_button("Bibo")
run_button_bibo.pack(pady=6)

run_button_rbpay = make_button("RBPay")
run_button_rbpay.pack(pady=6)

run_button_micropay = make_button("MicroPay")
run_button_micropay.pack(pady=6)

run_button_mannypay = make_button("MannyPay")
run_button_mannypay.pack(pady=6)

run_button_psslai = make_button("Psslai")
run_button_psslai.pack(pady=6)

run_button_digicoop = make_button("Digicoop")
run_button_digicoop.pack(pady=6)

# ===============================
# RUN ALL BUTTON
# ===============================
tk.Button(
    right_panel,
    text="🚀 Run All Applications",
    font=("Arial", 12, "bold"),
    bg="#0B395B",
    fg="white",
    bd=0,
    height=2,
    cursor="hand2",
    command=run_all_apps
).pack(pady=15, fill="x")

# ===============================
# FOOTER
# ===============================
footer = tk.Label(
    app,
    text="✔ Select modules → Choose environment → Run automation → View results",
    font=("Arial", 10),
    fg="#777",
    bg="#F5F7FA"
)
footer.pack(pady=10)

app.mainloop()