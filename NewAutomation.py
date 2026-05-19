import sys
import threading
import traceback
import random
import shutil
import os
import re
import smtplib
from pathlib import Path
from datetime import datetime
from email.message import EmailMessage
import tkinter as tk
from tkinter import messagebox, ttk

# Third-party UI & automation dependencies
import customtkinter as cctk
import matplotlib.pyplot as plt
from playwright.sync_api import sync_playwright, Playwright, TimeoutError

# Set visual styling theme
cctk.set_appearance_mode("Light")
cctk.set_default_color_theme("blue")

# =====================================================================
# Gmail Settings
# =====================================================================
GMAIL_USER = "mj@traxiontech.net"
GMAIL_APP_PASSWORD = "aohrspbjzpcdugdt"
RECIPIENT_EMAIL = "respinosa@traxiontech.net"

# =====================================================================
# Test Configuration & Unabridged Target Scenarios Matrix Registry
# =====================================================================
USERNAME = "txnqatestautomation@mailinator.com"
PASSWORD = "Traxion123!"

TEST_SCENARIOS = [
    # LOGIN MODULE
    #=POSITIVE=#
    {"module": "Login", "category": "Positive", "title": "TEST_LOGIN_01", "description": "Verify login success."},
    {"module": "Login", "category": "Positive", "title": "TEST_LOGIN_02", "description": "Verify System Validation for Invalid login."},
    {"module": "Login", "category": "Positive", "title": "TEST_LOGIN_03", "description": "Verify logout."},
    #=NEGATIVE=#
    {"module": "Login", "category": "Negative", "title": "Login without pass", "description": "Verify if the system showed validation message"},
    {"module": "Login", "category": "Negative", "title": "Non Existing Account", "description": "Verify if the user could proceed to the dashboard"},
    {"module": "Login", "category": "Negative", "title": "Password Length", "description": "Verify if the passwordfield have a password length validation."},
    {"module": "Login", "category": "Negative", "title": "Invalid Password", "description": "Verify if the user could proceed to the dashboard even if the password is incorrect."},

    ##=======================================================##

    # WITHDRAWAL MODULE
    #=POSITIVE=#
    {"module": "Cash-Out", "category": "Positive", "title": "Direct Fund Transfer", "description": "Verify Successful Direct transfer."},
    {"module": "Cash-Out", "category": "Positive", "title": "Withdraw Funds Via Instapay", "description": "Verify System Validation for Direct Fund Transfer Insufficient Balance"},
    {"module": "Cash-Out", "category": "Positive", "title": "TEST_BANK_TRANSFER_01", "description": "Verify Successful Bank transfer."},
   
    #=NEGATIVE=#
    {"module": "Cash-Out", "category": "Negative", "title": "Withdraw Funds Invalid Password", "description": "verify that banktransfer fails with invalid credentials."},
    {"module": "Cash-Out", "category": "Negative", "title": "Direct Fundtransfer Invalid Password", "description": "verify that fundtransfer fails with invalid credentials."},
   
    ##=======================================================##

    # CASH-IN MODULE
    #=POSITIVE=#
    {"module": "Cash-In", "category": "Positive", "title": "TEST_MANUAL_DEPOSIT_01", "description": "Verify Successful Manual deposit."},
    {"module": "Cash-In", "category": "Positive", "title": "TEST_CASH_IN_FROM_DRAGONPAY_01", "description": "Verify Successful DragonPay deposit."},
   
    #=NEGATIVE=#
    {"module": "Cash-In", "category": "Negative", "title": "Leave Blank Required Fields in Manual Deposit", "description": "Verify that the system shows validation messages when required fields are left blank in manual deposit."},
    {"module": "Cash-In", "category": "Negative", "title": "Leave Blank Deposit Slip", "description": "Verify that the system shows validation messages when required fields are left blank in manual deposit."},

    ##=======================================================##
    # TRANSACTION HISTORY MODULE
    {"module": "Transaction History", "category": "General", "title": "TEST_TRANSACTION_HISTORY_01", "description": "Verify If The System Allows The User To Search Transactions"},
    ##=======================================================##

    ##=======================================================##
    # ELOAD HISTORY MODULE  
    ##==POSITIVE==##
    {"module": "Eload", "category": "Positive", "title": "TEST_ELOAD_01", "description": "Verify Successful Eload Transactions"},
    {"module": "Eload", "category": "Positive", "title": "Non Telco", "description": "Verify that a merchant can do buyload transaction with non-telco product"},
    ##==NEGATIVE==##
    {"module": "Eload", "category": "Negative", "title": "Negative: Invalid Recipient Number", "description": "Verify that the system rejects invalid recipient numbers"},
    {"module": "Eload", "category": "Negative", "title": "Without Entering Number", "description": "Verify that the system cannot proceed with the transaction when recipient number is not entered"},
    {"module": "Eload", "category": "Negative", "title": "Without Entering Password", "description": "Verify that the system shows validation message when password is not entered"},
    ##=======================================================##

    ##=======================================================##
    # PAYBILLS MODULE
    ##==POSITIVE==##
    {"module": "Bills Payment", "category": "Positive", "title": "Bills Payment Successful", "description": "Verify that a merchant can successfully make a bill payment transaction."},
    {"module": "Bills Payment", "category": "Positive", "title": "Optional Fields Empty", "description": "Verify that payment is successful when leaving optional fields like 'Account No.' and 'Remarks' empty."},
    ##==NEGATIVE==##
    {"module": "Bills Payment", "category": "Negative", "title": "Without Entering Password in Bills", "description": "Verify that field system forces credential evaluation on submissions"},
    {"module": "Bills Payment", "category": "Negative", "title": "Mandatory Fields Missing", "description": "Verify error feedback on empty mandatory user details input elements"},
    {"module": "Bills Payment", "category": "Negative", "title": "Below Minimum Amount", "description": "Verify transaction restriction constraints on payments under boundary conditions"},
    ##=======================================================##

    # BULKDISBURSEMENT MODULE
    {"module": "Bulk Disbursement", "category": "General", "title": "TEST_BULKDISBURSEMENT_01", "description": "Verify Successful Bulk Disbursement Transactions"},
    ##=======================================================##

    # USER MANAGEMENT MODULE
    #=POSITIVE=#
    {"module": "User Management", "category": "Positive", "title": "TEST_USERMANAGEMENT_01", "description": "Verify that a new user can be successfully created with valid mandatory fields and the system displays a success confirmation message."},
    #=NEGATIVE=#
    {"module": "User Management", "category": "Negative", "title": "Add Existing User", "description": "Verify validation on adding existing user"},
    {"module": "User Management", "category": "Negative", "title": "Required Fields", "description": "Verify if the system showed a validation message"},
    {"module": "User Management", "category": "Negative", "title": "Existing Email", "description": "Verify if the user can add user with existing email"},
    {"module": "User Management", "category": "Negative", "title": "Mismatching Pass", "description": "Verify if the user could create mismatching pass"},
    {"module": "User Management", "category": "Negative", "title": "Mismatching MPIN", "description": "Verify if the user could create mismatching mpin"},
    {"module": "User Management", "category": "Negative", "title": "Invalid Email Format", "description": "Verify if the user could create account with invalid email format"},
    {"module": "User Management", "category": "Negative", "title": "Invalid Number Format", "description": "Verify if the user could create account with invalid number format"},
    {"module": "User Management", "category": "Negative", "title": "Password Doesn't Meet Req", "description": "Verify if the user can create a password that does not meet the requirements"},
    {"module": "User Management", "category": "Negative", "title": "edit btn", "description": "Verify if the user could proceed to the next page"},
    ##=======================================================##

    ##=======================================================##
    # USER MANAGEMENT MODULE
    #=POSITIVE=#
    {"module": "Branches", "category": "Positive", "title": "TEST_BRANCHES_01", "description": "Verify that a new branch can be successfully created with valid mandatory fields and the system displays a success confirmation message."},
    #=NEGATIVE=#

]   

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
        "Digicoop": "https://digicoop-uat.traxionpay.com/signin"
    },
    "PROD": {
        "Traxion": "https://merchant.traxionpay.com/signin",
        "Bibo": "https://bibo.traxionpay.com/signin",
        "RBPay": "https://rbpay.traxionpay.com/signin",
        "MannyPay": "https://mannypay.traxionpay.com/signin",
        "MicroPay": "https://micropay.traxionpay.com/signin",
        "Psslai": "https://psslai.traxionpay.com/signin",
        "Digicoop": "https://digicoop.traxionpay.com/signin"
    }
}

BASE_DIR = Path("automation_artifacts")
RUN_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
RUN_DIR = BASE_DIR / RUN_TIMESTAMP
SCREENSHOT_DIR = RUN_DIR / "screenshots"
ERROR_DIR = RUN_DIR / "errors"
REPORT_DIR = RUN_DIR / "report"

for directory in [SCREENSHOT_DIR, ERROR_DIR, REPORT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# =====================================================================
# Reporting Utilities & Helpers (FIXED SMTP LOGIC)
# =====================================================================
def get_ui_error(page):
    selectors = [".alert-danger", ".error", ".error-message", ".toast-error", "[role='alert']", ".MuiAlert-message"]
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
    explode = (0.05, 0)

    plt.figure(figsize=(5,5))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%', startangle=90, explode=explode, textprops={'fontsize':14, 'color':'#0B395B'})
    plt.title('Test Pass Rate', fontsize=16, color='#0B395B')
    plt.tight_layout()
    plt.savefig(chart_path, transparent=True)
    plt.close()

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
        <table width="100%" cellpadding="10" cellspacing="0" style="border-collapse:collapse; margin:20px 0; text-align:center;">
          <tr>
            <td style="background: linear-gradient(135deg, #177AC1, #0B395B); color: white; border-radius: 12px; padding: 20px; width: 33%;">
              <strong style="display:block; font-size:16px;">Total Tests</strong><span style="font-size:28px; font-weight:bold;">{total}</span>
            </td>
            <td style="background: linear-gradient(135deg, #4CAF50, #2E7D32); color: white; border-radius: 12px; padding: 20px; width: 33%;">
              <strong style="display:block; font-size:16px;">Passed</strong><span style="font-size:28px; font-weight:bold;">{passed}</span>
            </td>
            <td style="background: linear-gradient(135deg, #F44336, #C62828); color: white; border-radius: 12px; padding: 20px; width: 33%;">
              <strong style="display:block; font-size:16px;">Failed</strong><span style="font-size:28px; font-weight:bold;">{failed}</span>
            </td>
          </tr>
        </table>
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
        <td align="center"><span style="padding:6px 12px; border-radius:20px; background:{badge_bg}; color:{badge_color}; font-weight:bold; font-size:12px;">{r['status']}</span></td>
        <td align="center">{r.get('scenario_duration', 'N/A')}s</td>
        <td align="center"><img src="cid:{cid}" width="160" style="border:1px solid #CCC; border-radius:4px;"></td>
        </tr>
        """
        if r["status"] == "FAILED" and r.get("error_trace"):
            html += f"""
            <tr style="background:#FFF5F5; border-bottom:1px solid #DDD;"><td colspan="5" style="padding:10px;">
            <strong style="color:#C62828;">⚠️ Error Details:</strong>
            <pre style="background:#FDECEA; color:#C62828; font-size:12px; padding:10px; border-radius:6px; max-height:150px; overflow:auto;">{r['error_trace']}</pre>
            </td></tr>
            """

    html += f"""
        </table>
        <div style="margin-top:40px; background:#FFFFFF; border-radius:12px; padding:20px; text-align:center;">
            <h3 style="margin-bottom:20px; color:#0B395B; font-size:20px; font-weight:bold;">📊 Test Pass Rate</h3>
            <img src="cid:{chart_path.name}" style="width:300px; border:1px solid #CCC; border-radius:12px;">
            <p style="margin-top:15px; font-size:14px; color:#0B395B; font-weight:bold;">⏱ Total Execution Time: {format_duration(test_results[0].get('total_duration', 0))}</p>
        </div>
    </body></html>
    """
    msg.add_alternative(html, subtype="html")

    for r in test_results:
        try:
            if os.path.exists(r["screenshot"]):
                with open(r["screenshot"], "rb") as f:
                    msg.get_payload()[0].add_related(f.read(), "image", "png", cid=os.path.basename(r["screenshot"]))
        except Exception as e:
            print(f"⚠️ Could not attach screenshot {r['screenshot']}: {e}")

    try:
        with open(chart_path, "rb") as f:
            msg.get_payload()[0].add_related(f.read(), "image", "png", cid=chart_path.name)
    except Exception as e:
        print(f"⚠️ Could not attach chart {chart_path}: {e}")

    # ---------------------------------------------------------
    # FIXED: PURE SMTP_SSL INITIALIZATION (REPLACED BUGGED OPEN)
    # ---------------------------------------------------------
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        print("📧 Email report sent successfully")
    except Exception as e:
        print(f"❌ Failed to send email via SMTP layer: {e}")

# =====================================================================
# UI Layout Dynamic Accordion Component
# =====================================================================
class AccordionModuleCard(cctk.CTkFrame):
    """Collapsible UI accordion grouping categories (Positive/Negative) cleanly."""
    def __init__(self, master, module_name, scenarios, on_selection_change_cb, **kwargs):
        super().__init__(master, fg_color="#F8FAFC", border_color="#E2E8F0", border_width=1, corner_radius=10, **kwargs)
        self.module_name = module_name
        self.scenarios = scenarios
        self.on_selection_change_cb = on_selection_change_cb
        self.is_expanded = False
        
        self.scenario_vars = {}
        
        # Primary Collapsible Header Bar
        self.header_frame = cctk.CTkFrame(self, fg_color="#F0F6FF", height=42, corner_radius=10)
        self.header_frame.pack(fill="x", ipady=2)
        
        self.toggle_btn = cctk.CTkButton(
            self.header_frame, text="▶", width=25, fg_color="transparent", 
            text_color="#0B395B", font=("Arial", 12, "bold"), hover=False, command=self.toggle
        )
        self.toggle_btn.pack(side="left", padx=6)
        
        self.main_checkbox = cctk.CTkCheckBox(
            self.header_frame, text=self.module_name, font=("Arial", 13, "bold"),
            text_color="#0B395B", fg_color="#0B395B", checkbox_width=18, checkbox_height=18,
            command=self.on_main_checkbox_click
        )
        self.main_checkbox.pack(side="left", padx=2)
        
        self.counter_label = cctk.CTkLabel(
            self.header_frame, text="(0/0 selected)", font=("Arial", 11, "italic"), text_color="#64748B"
        )
        self.counter_label.pack(side="right", padx=12)
        
        # Inner Dropdown Container Frame View Panel
        self.body_frame = cctk.CTkFrame(self, fg_color="transparent")
        
        # Segment into Positive vs Negative category slots explicitly
        pos_scenarios = [s for s in scenarios if s.get("category") == "Positive"]
        neg_scenarios = [s for s in scenarios if s.get("category") == "Negative"]
        gen_scenarios = [s for s in scenarios if s.get("category") not in ["Positive", "Negative"]]
        
        if pos_scenarios:
            lbl = cctk.CTkLabel(self.body_frame, text="🟢 Positive Scenarios", font=("Arial", 11, "bold"), text_color="#16A34A")
            lbl.pack(anchor="w", padx=28, pady=(6, 2))
            self.build_rows(pos_scenarios)
            
        if neg_scenarios:
            lbl = cctk.CTkLabel(self.body_frame, text="🔴 Negative Scenarios", font=("Arial", 11, "bold"), text_color="#DC2626")
            lbl.pack(anchor="w", padx=28, pady=(6, 2))
            self.build_rows(neg_scenarios)
            
        if gen_scenarios:
            lbl = cctk.CTkLabel(self.body_frame, text="🔵 General Verification Steps", font=("Arial", 11, "bold"), text_color="#177AC1")
            lbl.pack(anchor="w", padx=28, pady=(6, 2))
            self.build_rows(gen_scenarios)
            
        self.update_selection_counters()
        
    def build_rows(self, subset_scenarios):
        for src in subset_scenarios:
            row = cctk.CTkFrame(self.body_frame, fg_color="transparent")
            row.pack(fill="x", padx=36, pady=2, anchor="w")
            
            chk_var = tk.BooleanVar(value=False)
            self.scenario_vars[src["title"]] = chk_var
            
            chk = cctk.CTkCheckBox(
                row, text=f"{src['title']} - {src['description'][:50]}...",
                variable=chk_var, font=("Arial", 12), text_color="#334155",
                fg_color="#177AC1", checkbox_width=16, checkbox_height=16,
                command=self.on_scenario_checkbox_click
            )
            chk.pack(side="left", anchor="w")

    def toggle(self):
        if self.is_expanded:
            self.body_frame.pack_forget()
            self.toggle_btn.configure(text="▶")
            self.is_expanded = False
        else:
            self.body_frame.pack(fill="x", pady=(0, 6))
            self.toggle_btn.configure(text="▼")
            self.is_expanded = True

    def on_main_checkbox_click(self):
        target_state = self.main_checkbox.get()
        for var in self.scenario_vars.values():
            var.set(target_state)
        self.update_selection_counters()
        self.on_selection_change_cb()

    def on_scenario_checkbox_click(self):
        self.update_selection_counters()
        self.on_selection_change_cb()

    def update_selection_counters(self):
        total = len(self.scenario_vars)
        selected = sum(1 for var in self.scenario_vars.values() if var.get())
        self.counter_label.configure(text=f"({selected}/{total} selected)")
        if selected == total:
            self.main_checkbox.select()
        elif selected == 0:
            self.main_checkbox.deselect()
        else:
            self.main_checkbox.configure(state="normal")

    def set_all_states(self, checked=True):
        if checked:
            self.main_checkbox.select()
        else:
            self.main_checkbox.deselect()
        for var in self.scenario_vars.values():
            var.set(checked)
        self.update_selection_counters()


# =====================================================================
# Main Revamped QA Dashboard Architecture
# =====================================================================
class ModernAutomationDashboard(cctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Traxion Automated White-Label Validation System")
        self.geometry("1200x750")
        self.state("zoomed")
        self.configure(fg_color="#F1F5F9")
        
        self.accordion_cards = []
        self.assemble_ui_components()
        self.bind_and_populate_modules()

    def assemble_ui_components(self):
        # Header Strip Bar area
        header = cctk.CTkFrame(self, fg_color="#0B395B", height=75, corner_radius=0)
        header.pack(fill="x")
        
        title_label = cctk.CTkLabel(
            header, text="⚙️ QA AUTOMATION PLATFORM FOR WHITE LABEL APPLICATION ECOSYSTEMS",
            font=("Arial", 18, "bold"), text_color="white"
        )
        title_label.pack(side="left", padx=24, pady=20)
        
        self.env_var = cctk.StringVar(value="SIT")
        env_lbl = cctk.CTkLabel(header, text="TARGET RUN ENV:", font=("Arial", 11, "bold"), text_color="#93C5FD")
        env_lbl.pack(side="right", padx=(0, 6))
        
        self.env_dropdown = cctk.CTkOptionMenu(
            header, variable=self.env_var, values=["SIT", "UAT", "PROD"],
            fg_color="#177AC1", button_color="#0B395B", button_hover_color="#1E3A8A",
            width=100, font=("Arial", 12, "bold")
        )
        self.env_dropdown.pack(side="right", padx=24)

        # Container Split Panels Layout Grid
        main_grid = cctk.CTkFrame(self, fg_color="transparent")
        main_grid.pack(fill="both", expand=True, padx=20, pady=20)
        main_grid.columnconfigure(0, weight=4, minsize=520) 
        main_grid.columnconfigure(1, weight=3, minsize=400)
        main_grid.rowconfigure(0, weight=1)

        # --- LEFT PANEL FRAME (TREE CHECKLIST SELECTORS) ---
        left_column = cctk.CTkFrame(main_grid, fg_color="white", corner_radius=12, border_color="#E2E8F0", border_width=1)
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        
        left_title = cctk.CTkLabel(left_column, text="🧩 Automation Test Suite Coverage Modules Tree", font=("Arial", 14, "bold"), text_color="#0B395B")
        left_title.pack(anchor="w", padx=18, pady=(16, 2))
        
        search_frame = cctk.CTkFrame(left_column, fg_color="transparent")
        search_frame.pack(fill="x", padx=16, pady=8)
        
        self.search_var = cctk.StringVar()
        self.search_var.trace_add("write", self.filter_modules_by_search_query)
        self.search_bar = cctk.CTkEntry(
            search_frame, placeholder_text="🔍 Search inside titles, descriptions or module scopes...",
            textvariable=self.search_var, height=32, font=("Arial", 12)
        )
        self.search_bar.pack(fill="x")
        
        macro_frame = cctk.CTkFrame(left_column, fg_color="transparent")
        macro_frame.pack(fill="x", padx=16, pady=(0, 8))
        
        select_all_btn = cctk.CTkButton(
            macro_frame, text="✓ Select All", fg_color="#E2E8F0", text_color="#334155",
            hover_color="#CBD5E1", height=28, font=("Arial", 11, "bold"), command=self.macro_select_all
        )
        select_all_btn.pack(side="left", expand=True, fill="x", padx=(0, 4))
        
        deselect_all_btn = cctk.CTkButton(
            macro_frame, text="✖ Clear All", fg_color="#E2E8F0", text_color="#334155",
            hover_color="#CBD5E1", height=28, font=("Arial", 11, "bold"), command=self.macro_deselect_all
        )
        deselect_all_btn.pack(side="left", expand=True, fill="x", padx=(4, 0))

        self.module_scroller = cctk.CTkScrollableFrame(left_column, fg_color="transparent", label_text="")
        self.module_scroller.pack(fill="both", expand=True, padx=12, pady=(0, 16))

        # --- RIGHT PANEL FRAME ---
        right_column = cctk.CTkFrame(main_grid, fg_color="white", corner_radius=12, border_color="#E2E8F0", border_width=1)
        right_column.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        
        app_title = cctk.CTkLabel(right_column, text="🚀 Target Ecosystem White Label Applications", font=("Arial", 14, "bold"), text_color="#0B395B")
        app_title.pack(anchor="w", padx=18, pady=16)
        
        app_grid_frame = cctk.CTkFrame(right_column, fg_color="transparent")
        app_grid_frame.pack(fill="both", expand=True, padx=18, pady=(0, 12))
        app_grid_frame.columnconfigure(0, weight=1)
        app_grid_frame.columnconfigure(1, weight=1)
        
        apps_list = ["Traxion", "Bibo", "RBPay", "MicroPay", "MannyPay", "Psslai", "Digicoop"]
        self.app_buttons = {}
        
        for index, app_name in enumerate(apps_list):
            row_idx = index // 2
            col_idx = index % 2
            
            btn = cctk.CTkButton(
                app_grid_frame, text=f"▶ Run {app_name}", font=("Arial", 12, "bold"),
                fg_color="#177AC1", hover_color="#0B395B", height=42,
                command=lambda name=app_name: self.dispatch_execution_thread(lambda: self.execute_automation_suite(name))
            )
            btn.grid(row=row_idx, column=col_idx, sticky="ew", padx=6, pady=6)
            self.app_buttons[app_name] = btn
            
        self.run_all_apps_btn = cctk.CTkButton(
            right_column, text="🔥 BATCH EXECUTE SYSTEM WIDE (ALL TENANT SUITES)", font=("Arial", 13, "bold"),
            fg_color="#0B395B", hover_color="#1E3A8A", height=46, corner_radius=8,
            command=lambda: self.dispatch_execution_thread(self.execute_batch_system_wide)
        )
        self.run_all_apps_btn.pack(fill="x", padx=24, pady=(10, 24))

        # Bottom operational tracking status strip
        footer = cctk.CTkFrame(self, height=30, fg_color="#E2E8F0", corner_radius=0)
        footer.pack(fill="x", side="bottom")
        
        self.footer_status = cctk.CTkLabel(
            footer, text="Engine Standing By. Check target script definitions profiles to kick off automated checks pipelines.",
            font=("Arial", 11), text_color="#475569"
        )
        self.footer_status.pack(side="left", padx=16, pady=4)

    # =====================================================================
    # Component Matrix Populators
    # =====================================================================
    def bind_and_populate_modules(self):
        grouped_data = {}
        for scenario in TEST_SCENARIOS:
            grouped_data.setdefault(scenario["module"], []).append(scenario)
            
        for module_name, scenarios in grouped_data.items():
            card = AccordionModuleCard(
                self.module_scroller, module_name=module_name, scenarios=scenarios,
                on_selection_change_cb=self.evaluate_system_selection_metrics
            )
            card.pack(fill="x", pady=5, padx=2)
            self.accordion_cards.append(card)
            
    def evaluate_system_selection_metrics(self):
        total_selected = 0
        for card in self.accordion_cards:
            total_selected += sum(1 for var in card.scenario_vars.values() if var.get())
        self.footer_status.configure(
            text=f"Active Configuration Workspace: Curated total target scope matching [{total_selected}] test cases scripts ready for run cycles profiles passes."
        )

    def macro_select_all(self):
        for card in self.accordion_cards:
            card.set_all_states(checked=True)
        self.evaluate_system_selection_metrics()

    def macro_deselect_all(self):
        for card in self.accordion_cards:
            card.set_all_states(checked=False)
        self.evaluate_system_selection_metrics()

    def filter_modules_by_search_query(self, *args):
        query = self.search_var.get().lower().strip()
        for card in self.accordion_cards:
            if not query:
                card.pack(fill="x", pady=5, padx=2)
                continue
            module_match = query in card.module_name.lower()
            scenario_match = any(query in title.lower() for title in card.scenario_vars.keys())
            if module_match or scenario_match:
                card.pack(fill="x", pady=5, padx=2)
                if scenario_match and not card.is_expanded:
                    card.toggle()
            else:
                card.pack_forget()

    def dispatch_execution_thread(self, processing_lambda_target):
        execution_worker_thread = threading.Thread(target=processing_lambda_target, daemon=True)
        execution_worker_thread.start()

    def switch_ui_execution_state(self, is_running=True):
        state = "disabled" if is_running else "normal"
        for btn in self.app_buttons.values():
            btn.configure(state=state)
        self.run_all_apps_btn.configure(state=state)

    def retrieve_curated_execution_scenarios(self):
        selected_scenarios = []
        for card in self.accordion_cards:
            for scenario_title, boolean_var in card.scenario_vars.items():
                if boolean_var.get():
                    match_object = next((s for s in TEST_SCENARIOS if s["title"] == scenario_title), None)
                    if match_object:
                        selected_scenarios.append(match_object)
        return selected_scenarios

    # =====================================================================
    # Playwright Framework Automation Pipeline Infrastructure Logic Core
    # =====================================================================
    def execute_automation_suite(self, app_name):
        selected_scope = self.retrieve_curated_execution_scenarios()
        if not selected_scope:
            messagebox.showwarning("Target Check Range Null", "⚠️ Zero specific script rows selected inside modular collapsible options layouts array stacks.")
            return

        self.switch_ui_execution_state(is_running=True)
        target_env = self.env_var.get()
        
        try:
            login_url = ENV_URLS[target_env][app_name]
        except KeyError:
            self.switch_ui_execution_state(is_running=False)
            return

        total_start = datetime.now()
        results = []

        with sync_playwright() as playwright_instance:
            for index, scenario in enumerate(selected_scope):
                if app_name == "Traxion" and scenario["module"] in ["Eload", "Bills Payment"]:
                    continue

                scenario_start = datetime.now()
                print(f"🔁 Running '{scenario['title']}' | Context Target Index Suite Node: {index+1}")
                
                try:
                    browser = playwright_instance.chromium.launch(headless=False, slow_mo=300)
                    context = browser.new_context()
                    page = context.new_page()
                    
                    result_data = self.run_legacy_scenario_steps(page, scenario["title"], login_url)
                    scenario_end = datetime.now()
                    
                    result_data["scenario_duration"] = round((scenario_end - scenario_start).total_seconds(), 2)
                    results.append(result_data)
                    
                except Exception as ex:
                    scenario_end = datetime.now()
                    results.append({
                        "title": scenario["title"], "description": scenario["description"], "status": "FAILED",
                        "screenshot": str(ERROR_DIR / f"{scenario['title']}_fail.png"), "error_trace": traceback.format_exc(),
                        "scenario_duration": round((scenario_end - scenario_start).total_seconds(), 2)
                    })
                finally:
                    try:
                        context.close()
                        browser.close()
                    except:
                        pass

        total_duration = (datetime.now() - total_start).total_seconds()
        if results:
            results[0]['total_duration'] = total_duration
            try:
                send_email(results)
            except Exception as email_dispatch_err:
                print(f"❌ Reporting module dispatch failed: {email_dispatch_err}")

        self.switch_ui_execution_state(is_running=False)
        messagebox.showinfo("Execution Phase Cleared", f"Finished suite runs routines for {app_name} on [{target_env}] system zone profile domain maps.")

    def run_legacy_scenario_steps(self, page, title, login_url):
        """Preserves and maps all unique automated functional test logic playbook steps exactly as written."""
        error_trace = ""
        browser_errors = []
        network_errors = []
        ui_error = ""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = SCREENSHOT_DIR / f"{title.replace(' ', '_')}_{timestamp}.png"
        status = "FAILED"
        description_str = next((s["description"] for s in TEST_SCENARIOS if s["title"] == title), "")

        try:
            ###======================== LOGIN SCENARIOS ========================##
            ##POSITIVE##
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
            elif title == "Direct Fund Transfer":
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
                validation_msg = page.locator("text=Fund Transfer transaction processed successfully.")
                system_error = page.locator("text=Error|Failed|Unable")
                page.wait_for_timeout(2000)

                if validation_msg.first.is_visible():
                    actual_result = "Fund Transfer transaction processed successfully."
                    status = "PASSED"
                elif system_error.first.is_visible():
                    actual_result = system_error.first.inner_text()
                    status = "FAILED"
                else:
                    actual_result = "No validation message displayed"
                    status = "FAILED"

            elif title == "Withdraw Funds Via Instapay":
                page.goto(login_url, timeout=30000)
                page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
                page.get_by_role("textbox", name="your password").fill(PASSWORD)
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Withdrawals").click()
                page.get_by_role("link", name="Withdraw Funds").click()
                page.locator("#withdraw_recipient_bank").select_option("197")
                page.get_by_placeholder("0.00").click()
                page.get_by_placeholder("0.00").fill("500")
                page.get_by_role("radio", name="Password").check()
                page.get_by_role("textbox", name="form-control required field").click()
                page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
                page.get_by_role("button", name="Withdraw Funds").click()
                download = download_info.value
                validation_msg = page.locator("text=Fund Transfer transaction processed/initiated successfully.")
                system_error = page.locator("text=Error|Failed|Unable")
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

            ###==================================================================##
            ##CASH-IN SCENARIOS##
            #POSITIVE#
            elif title == "TEST_MANUAL_DEPOSIT_01":
                page.goto(login_url, timeout=30000)
                page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
                page.get_by_role("textbox", name="your password").fill(PASSWORD)
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Deposits").click()
                page.get_by_role("link", name="Make A Deposit").click()
                page.locator("#manual_amount").fill("100")
                page.get_by_label("Select BANCO DE ORO UNIBANK,").select_option("BDO_UNIBANK")
                file_path = Path(__file__).parent / "file" / "upload.png"
                page.locator("input[type='file']").set_input_files(str(file_path))
                page.wait_for_load_state("networkidle", timeout=90000)
                page.get_by_role("button", name="Submit Manual Deposit Request").click()
                page.wait_for_load_state("networkidle", timeout=90000)
                page.get_by_text("Manual deposit request with").click()
                status = "PASSED"

            elif title == "TEST_CASH_IN_FROM_DRAGONPAY_01":
                page.goto(login_url, timeout=30000)
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
                page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
                page.get_by_role("textbox", name="your password").fill(PASSWORD)
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Deposits").click()
                page.get_by_role("link", name="Make A Deposit").click()
                page.get_by_role("button", name="Submit Manual Deposit Request").click()
                validation_msg = page.locator("text=This Field is Required")
                system_error = page.locator("text=Error|Failed|Unable")
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

            ###===================================================================##
            elif title == "TEST_TRANSACTION_HISTORY_01":
                page.goto(login_url, timeout=30000)
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

            ###==================================================================##
            ##==eload module==##
            ##==POSITIVE==##
            elif title == "TEST_ELOAD_01":
                page.goto(login_url, timeout=30000)
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

            ###===================================================================##
            ##== BILLS PAYMENT MODULE ==##
            ##==POSITIVE==##
            elif title == "Bills Payment Successful":
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
                success_text = page.locator("text=Success|Successful|Reference|Completed|Thank you")

                try:
                    if system_error.is_visible(timeout=5000):
                        actual_result = system_error.first.inner_text()
                        status = "FAILED"
                    elif success_text.is_visible(timeout=5000):
                        actual_result = success_text.first.inner_text()
                        status = "PASSED"
                    elif page.url != current_url:
                        actual_result = f"Passed: System redirected to {page.url} without errors."
                        status = "PASSED"
                    else:
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

                if validation_msg.count() > 0:
                    actual_result = "Minimum amount is PHP 25.00"
                    status = "PASSED"
                elif system_error.count() > 0:
                    actual_result = system_error.first.inner_text()
                    status = "FAILED"
                else:
                    actual_result = "No validation message displayed"
                    status = "FAILED"

            ###===================================================================##
            elif title == "TEST_BULKDISBURSEMENT_01":
                page.goto(login_url, timeout=30000)
                page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
                page.get_by_role("textbox", name="your password").fill(PASSWORD)
                page.get_by_role("button", name="Sign in").click()
                page.get_by_role("link", name="Disbursements").click()
                page.get_by_role("link", name="Create Bulk Disbursement").click()
                original_file = "9UGXNORKHJ-DISBURSEMENT-2026042901.xlsx"
                suffix = str(random.randint(100, 999))
                base_name = original_file[:-7]
                new_filename = f"{base_name}{suffix}.xlsx"
                current_dir = os.path.dirname(__file__)
                source_path = os.path.join(current_dir, original_file)
                new_path = os.path.join(current_dir, new_filename)
                shutil.copy(source_path, new_path)
                page.locator("input[type='file']").set_input_files(new_path)
                page.get_by_role("radio", name="Password").check()
                page.get_by_role("textbox", name="form-control required field").fill("Traxion123!")
                page.locator(".row > .mb-3").first.click()
                page.wait_for_load_state("networkidle", timeout=30000)
                page.get_by_role("button", name="Make A Bulk Disbursement").click()
                page.wait_for_load_state("networkidle", timeout=30000)
                status = "PASSED"
                try:
                    os.remove(new_path)
                except:
                    pass

            ###===================================================================##
            ##===USER MODULE===##
            ##==POSITIVE==##
            elif title == "TEST_USERMANAGEMENT_01":
                import time
                ts = int(time.time())
                rand = random.randint(100, 999)
                unique_id = f"{ts}{rand}"
                first_name = f"Mark{unique_id}"
                email = f"mj+{unique_id}@traxiontech.net"
                mobile = f"9{str(ts)[-6:]}{rand}"[:10]

                page.goto(login_url, timeout=30000)
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
                page.get_by_role("textbox", name="your@email.com").fill(USERNAME)
                page.get_by_role("textbox", name="your password").fill(PASSWORD)
                page.get_by_role("button", name="Sign in").click()
                page.wait_for_load_state("networkidle")
                page.get_by_role("link", name="Users").click()
                page.get_by_role("link", name="Add New User").click()
                page.wait_for_load_state("networkidle")
                page.get_by_role("textbox", name="First Name *").fill("Lebron")
                page.get_by_role("textbox", name="Last Name *").fill("James")
                page.get_by_role("textbox", name="Email Address *").fill("respinosa@traxiontech.net")
                page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill("9878787878")
                page.get_by_role("textbox", name="Password *").fill("Traxion123!")
                page.get_by_role("textbox", name="Minimum 8 characters required").fill("traxion12345!")
                page.get_by_role("textbox", name="MPIN *", exact=True).fill("231895")
                page.get_by_role("textbox", name="Confirm MPIN *").fill("231895")
                user_role = page.get_by_label("User Role *")
                user_role.scroll_into_view_if_needed()
                user_role.select_option(index=1) 
                page.get_by_role("button", name="Add user").click()
                mismatch_err = page.get_by_text("Password and Confirmation do not match")
                system_err = page.locator("text=Error|Failed|Unable")

                try:
                    mismatch_err.wait_for(state="visible", timeout=5000)
                    actual_result = "Password and Confirmation do not match"
                    status = "PASSED"
                except:
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
                user_role_dropdown = page.get_by_label("User Role *")
                user_role_dropdown.scroll_into_view_if_needed()
                user_role_dropdown.select_option(index=1)
                page.get_by_role("button", name="Add user").click()
                page.wait_for_timeout(2000)
                validation_msg = page.locator("text=ensure both fields match")
                system_error = page.locator("text=Error|Failed|Unable")
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
                page.get_by_role("textbox", name="First Name *").fill("Boss")
                page.get_by_role("textbox", name="Last Name *").fill("Atan")
                page.get_by_role("textbox", name="Email Address *").fill("BoossAtan.com.net")
                page.get_by_role("textbox", name="10 digits starting with 9 (e.").fill("9888787848")
                page.get_by_role("textbox", name="Password *").fill("Traxion123!")
                page.get_by_role("textbox", name="Minimum 8 characters required").fill("Traxion123!")
                page.get_by_role("textbox", name="MPIN *", exact=True).fill("231895")
                page.get_by_role("textbox", name="Confirm MPIN *").fill("231895")
                user_role = page.get_by_label("User Role *")
                user_role.scroll_into_view_if_needed()
                user_role.select_option(index=1) 
                page.get_by_role("button", name="Add user").click()
                validation_msg = page.locator("text=The email address you entered is not in a valid format")
                system_error = page.locator("text=Error|Failed|Unable")

                try:
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
                user_role = page.get_by_label("User Role *")
                user_role.scroll_into_view_if_needed()
                user_role.select_option(index=1) 
                page.get_by_role("button", name="Add user").click()
                validation_msg = page.get_by_text("Invalid mobile number format. Must be in +639XXXXXXXXX format", exact=False)
                system_error = page.locator("text=Error|Failed|Unable")

                try:
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
                user_role = page.get_by_label("User Role *")
                user_role.scroll_into_view_if_needed()
                user_role.select_option(index=1)
                page.get_by_role("button", name="Add user").click()
                validation_msg = page.get_by_text("Password", exact=False)
                system_error = page.locator("text=Error|Failed|Unable")

                try:
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
                page.get_by_role("cell", name="BryanjWV Lasernaphi").click()
                page.get_by_role("link", name="Edit").click()
                edit_modal_header = page.get_by_text("Edit User", exact=True)
                save_btn = page.get_by_role("button", name="Save Changes")

                try:
                    edit_modal_header.wait_for(state="visible", timeout=5000)
                    actual_result = "Edit User modal form loaded successfully."
                    status = "PASSED"
                except:
                    if save_btn.is_visible():
                        actual_result = "Save Changes button detected; edit form loaded successfully."
                        status = "PASSED"
                    else:
                        actual_result = "Failed to open Edit User modal window."
                        status = "FAILED"

            page.screenshot(path=str(screenshot_path))

        except Exception:
            error_trace = traceback.format_exc()
            ui_error = get_ui_error(page)
            status = "FAILED"
            try:
                page.screenshot(path=str(screenshot_path))
            except:
                pass

        return {
            "title": title, "description": description_str, "status": status,
            "screenshot": str(screenshot_path), "error_trace": error_trace if status == "FAILED" else ""
        }

    def execute_batch_system_wide(self):
        apps_list = ["Traxion", "Bibo", "RBPay", "MicroPay", "MannyPay", "Psslai", "Digicoop"]
        for tenant in apps_list:
            self.execute_automation_suite(tenant)


# =====================================================================
# Program Entry Run Trigger
# =====================================================================
if __name__ == "__main__":
    if sys.platform.startswith("win"):
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
            
    dashboard_app_instance = ModernAutomationDashboard()
    dashboard_app_instance.mainloop()