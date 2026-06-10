#!/usr/bin/env python3
"""Build Amr_Magdy_CV.pdf with brand styling. Requires: pip install fpdf2"""
from fpdf import FPDF

NAVY = (11, 31, 58)
GOLD = (184, 134, 47)
GOLD2 = (212, 162, 62)
INK = (30, 41, 59)
GREY = (100, 116, 139)
LIGHT = (247, 244, 238)
GREEN = (31, 138, 76)

F = "/usr/share/fonts/truetype/dejavu/"

class CV(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("dv", "", 8); self.set_text_color(*GREY)
            self.cell(0, 6, "Amr Magdy — Salesforce CRM Consultant · amrmagdy.com", align="R")
            self.ln(10)

    def footer(self):
        self.set_y(-12)
        self.set_font("dv", "", 7.5); self.set_text_color(*GREY)
        self.cell(0, 6, f"info@AmrMagdy.com  ·  amrmagdy.com  ·  linkedin.com/in/amrmagdyai  ·  Page {self.page_no()}", align="C")

pdf = CV("P", "mm", "A4")
pdf.add_font("dv", "", F + "DejaVuSans.ttf")
pdf.add_font("dv", "B", F + "DejaVuSans-Bold.ttf")
pdf.add_font("dv", "I", F + "DejaVuSans.ttf")  # no oblique variant available; fall back to regular
pdf.set_auto_page_break(True, margin=16)
pdf.add_page()

# ---- Header band
pdf.set_fill_color(*NAVY)
pdf.rect(0, 0, 210, 34, "F")
pdf.set_xy(14, 7)
pdf.set_font("dv", "B", 19); pdf.set_text_color(255, 255, 255)
pdf.cell(0, 9, "Amr Magdy Abd El-Fattah", ln=1)
pdf.set_x(14)
pdf.set_font("dv", "", 9.5); pdf.set_text_color(*GOLD2)
pdf.cell(0, 6, "Salesforce CRM Consultant  ·  Apex & LWC Development  ·  4× Certified  ·  Remote", ln=1)
pdf.set_x(14)
pdf.set_font("dv", "", 8); pdf.set_text_color(220, 228, 240)
pdf.cell(0, 6, "info@AmrMagdy.com  ·  +20 103 327 5250  ·  amrmagdy.com  ·  linkedin.com/in/amrmagdyai", ln=1)

# ---- Stat bar
stats = [("+30%", "Pipeline Visibility"), ("20+ hrs", "Saved / Week"), ("+25%", "User Adoption"),
         ("300+", "Cases Resolved"), ("6+", "Systems Integrated")]
y = 38; w = 182 / len(stats); x = 14
for n, l in stats:
    pdf.set_fill_color(*LIGHT)
    pdf.rect(x, y, w - 2, 13, "F")
    pdf.set_xy(x, y + 1.5); pdf.set_font("dv", "B", 10.5); pdf.set_text_color(*GOLD)
    pdf.cell(w - 2, 5.5, n, align="C")
    pdf.set_xy(x, y + 7); pdf.set_font("dv", "", 6.5); pdf.set_text_color(*GREY)
    pdf.cell(w - 2, 4, l, align="C")
    x += w
pdf.set_y(y + 17)

def section(title):
    pdf.ln(2.5)
    pdf.set_font("dv", "B", 11.5); pdf.set_text_color(*NAVY)
    pdf.cell(0, 7, title, ln=1)
    pdf.set_draw_color(*GOLD2); pdf.set_line_width(0.5)
    pdf.line(14, pdf.get_y(), 196, pdf.get_y())
    pdf.ln(2.5)

def para(txt, size=8.6):
    pdf.set_font("dv", "", size); pdf.set_text_color(*INK)
    pdf.set_x(14); pdf.multi_cell(182, 4.6, txt)
    pdf.ln(1)

def role(title, dates, org, intro=None):
    if pdf.get_y() > 255: pdf.add_page()
    pdf.set_x(14)
    pdf.set_font("dv", "B", 9.8); pdf.set_text_color(*NAVY)
    pdf.cell(135, 5.5, title)
    pdf.set_font("dv", "B", 8); pdf.set_text_color(*GOLD)
    pdf.cell(47, 5.5, dates, align="R", ln=1)
    pdf.set_x(14)
    pdf.set_font("dv", "I", 8.2); pdf.set_text_color(*GREY)
    pdf.cell(0, 4.6, org, ln=1)
    pdf.ln(0.8)
    if intro:
        para(intro, 8.3)

def bullet(txt, badge=None):
    pdf.set_x(14)
    pdf.set_font("dv", "", 8.4); pdf.set_text_color(*INK)
    if badge:
        txt = txt + "   "
    pdf.set_x(17)
    start_y = pdf.get_y()
    pdf.multi_cell(176, 4.5, "•  " + txt + (f"  [{badge}]" if badge else ""))
    pdf.ln(0.4)

# ---- Summary
section("Professional Summary")
para("Strategic Salesforce CRM Consultant with hands-on Apex and LWC development experience, specializing in "
     "real estate. I build the systems real estate companies actually run on — centralized Configuration Objects "
     "managing 50+ automation rules, custom Apex integrations syncing RingCentral call logs, Kanban LWC components "
     "deployed company-wide, full-funnel campaign ROI dashboards, and multi-system integrations across 6+ platforms. "
     "My 7-year background as an Adobe Certified Instructor (8,000+ students, 4.9/5 rating) means the solutions I "
     "build get genuinely adopted — not just delivered.")

# ---- Expertise
section("Core Expertise")
cols = [
    ("Salesforce Platform", ["Flow Builder & Process Automation", "Apex (Schedulable, Queueable, Batch, Triggers)",
     "Lightning Web Components (LWC)", "Configuration Object Architecture", "Reports, Dashboards & Scorecards",
     "Data Loader & Mass Updates"]),
    ("Integrations & Tools", ["RingCentral Apex API Sync (100% automated)", "DocuSign, QuickBooks (4 accounts)",
     "SmrtPhone, Zapier, Google Drive", "Tableau Connected to Salesforce", "Python for Data Cleaning & Migration",
     "Salesforce ↔ Slack Direct Integration"]),
    ("Real Estate Specialty", ["Lead Routing & Speed-to-Lead Automation", "Campaign Attribution via Call Tracking",
     "Transaction Coordination Workflows", "Marketing ROI Tracking by Campaign", "Property Acquisition Pipeline Architecture",
     "Duplicate Lead Detection & Management"]),
]
cw = 182 / 3
x0 = 14; ytop = pdf.get_y()
maxy = ytop
for i, (h, items) in enumerate(cols):
    x = x0 + i * cw
    pdf.set_xy(x, ytop)
    pdf.set_font("dv", "B", 8.4); pdf.set_text_color(*GOLD)
    pdf.cell(cw - 4, 5, h, ln=0)
    yy = ytop + 5.5
    for it in items:
        pdf.set_xy(x, yy)
        pdf.set_font("dv", "", 7.4); pdf.set_text_color(*INK)
        pdf.multi_cell(cw - 5, 3.9, "• " + it)
        yy = pdf.get_y() + 0.6
    maxy = max(maxy, yy)
pdf.set_y(maxy + 1)

# ---- Experience
section("Professional Experience")

role("Salesforce CRM Platform Manager", "Jun 2024 – Present",
     "Central City Solutions  ·  Remote · Columbus, OH, USA",
     "Real estate acquisition company — full-cycle CRM design, Apex development, LWC customization, and multi-system integration.")
for b, badge in [
    ("Built a centralized Configuration Object managing 50+ automation rules (Slack, email, SMS, tasks) — non-technical users add and disable automations without developer involvement.", None),
    ("Developed MergeFieldReplacer Apex class replacing merge field tokens in automation templates with live Salesforce data, supporting cross-object lookups, date arithmetic, and system variables.", None),
    ("Built RCDailyCallLogSync — Schedulable Apex with chained Queueable processing that auto-syncs RingCentral call logs into Salesforce Tasks daily, matching calls to Leads by phone number.", "−2 hrs/user/wk"),
    ("Migrated 30+ Zapier automations to native Salesforce Flows after repeated API limit violations — eliminating external dependency, cutting costs, and improving trigger speed from minutes to milliseconds.", "30+ flows"),
    ("Integrated 6+ external systems: RingCentral, DocuSign, QuickBooks (4 accounts), SmrtPhone, Google Drive, and Tableau — all synced to Salesforce automatically.", None),
    ("Built custom LWC Queue Task Manager with sort/filter, color-coded dates, custom mobile notifications, and utility bar deployment — adopted company-wide.", None),
    ("Designed complete Transaction Coordination system: custom Kanban LWC board, 15+ automated task triggers, DocuSign status tracking, TC scorecard, and post-close review automation.", None),
    ("Built Marketing ROI dashboard tracking cost-per-lead, cost-per-appointment, and lead-to-contract rates by campaign — driving weekly leadership decisions.", "+30%"),
    ("Used Python to clean 247 leads with invalid phone fields; bulk-updated 115 lead-campaign mappings; managed onboarding of 45,000 prospect buyer records.", None),
    ("Built intelligent duplicate lead detection: preserved historical homeowner records, copied campaign strategy, and sent real-time Slack alerts on every duplicate.", "+25%"),
]: bullet(b, badge)
pdf.ln(1.5)

role("Salesforce CRM Consultant (On-Demand)", "Apr 2025 – Present",
     "Pezon Properties  ·  Remote · PA, USA",
     "Real estate acquisition company — 50+ delivered requests across analytics, automation, and process design.")
for b, badge in [
    ("Built a full-funnel campaign performance dashboard with 25 metrics — gross/net leads and response rates, opportunity, appointment, signed agreement, and closed deal rates, cost-per metric at every funnel stage, net profit per unit, and return multiple — filterable by week, month, and quarter.", None),
    ("Automated lead source and campaign attribution from call-tracking phone numbers across direct mail, Google Business Profile, PPC, and web — plus web-to-direct-mail campaign matching by street address.", None),
    ("Rebuilt the Transaction Coordination application: conditional stages for cash vs. financed purchases and SFH/MFH/5+ unit logic, a 40+ field property onboarding checklist stage, and required quality-control gates blocking stage progression.", None),
    ("Automated the lead lifecycle: status transitions on outbound activity, 30-day inactivity handling, 24-hour stale-lead email escalations, follow-up task automation with overdue notifications, and required-field gates before lead conversion.", "+20%"),
    ("Built speed-to-lead, missed-call-to-callback, live answer rate, and text response time reporting — excluding spam calls and inbound texts for honest numbers.", None),
    ("Integrated DocuSign for agreements of sale, automated quarterly campaign creation with naming conventions, and built a Google Sheets + Zapier lead import pipeline.", "+15%"),
    ("Enforced data governance: conversion-only opportunity creation, locked lead-status edits, duplicate handling across prospect/homeowner records, Do Not Mail/Call/Text compliance, and per-user permission matrices.", None),
]: bullet(b, badge)
pdf.ln(1.5)

role("Salesforce CRM Platform Manager (Part-Time)", "Oct 2024 – Mar 2025",
     "Pezon Properties  ·  Remote · PA, USA")
for b, badge in [
    ("Developed a full financial analytics system tracking property expenses, acquisition costs, renovation budgets, and net profit per deal — giving leadership accurate P&L visibility at the individual deal level.", None),
    ("Built cost-per-lead and cost-per-opportunity calculations broken down by campaign and lead source — revealing the true ROI of every marketing channel.", None),
    ("Created performance dashboards showing which campaigns (direct mail, dialers, PPC, TV, referrals) generated the most profitable leads vs. just the highest lead volume — directly informing marketing budget decisions.", None),
    ("Built revenue and expense reports separating acquisition cost, holding costs, and net profit — enabling leadership to see real profitability, not just closed deal counts.", None),
    ("Reduced operational inefficiencies through CRM implementation and process automation.", "−25%"),
]: bullet(b, badge)
pdf.ln(1.5)

role("Salesforce Administrator & Developer", "Feb 2024 – Nov 2024",
     "Sylndr  ·  Hybrid · Cairo, Egypt",
     "Egypt's leading used-car marketplace — maintained and developed features on an enterprise Salesforce platform covering the full vehicle lifecycle.")
for b, badge in [
    ("Maintained and extended features across multiple domains of the vehicle lifecycle platform: lead management, duplicate vehicle detection, inspection visits, quality control, spare parts inventory, work orders, refurbishing, pricing, pre-sale stages, and B2C & dealer sales workflows.", None),
    ("Developed features and fixes using Apex, Lightning Web Components, and Flows — working within an existing complex codebase across multiple custom objects.", None),
    ("Managed user provisioning, roles, and permission sets ensuring secure CRM access.", None),
    ("Improved data quality through validation rules and automation across pipeline stages.", "−15% errors"),
]: bullet(b, badge)
pdf.ln(1.5)

role("Jr. Salesforce Marketing Cloud Consultant", "Oct 2023 – Dec 2023",
     "Conx Digital  ·  Remote · UAE")
for b, badge in [
    ("Marketing Cloud implementation, configuration, and data migration for UAE-based client.", None),
    ("Built automated customer journeys increasing marketing engagement.", "+10%"),
]: bullet(b, badge)
pdf.ln(1.5)

role("Adobe Certified Instructor & Expert", "2015 – 2023",
     "Twjeih · Critical Innovation · YAT · Engosoft · Russian Culture Center  ·  Global · Egypt, UAE, Saudi Arabia")
for b, badge in [
    ("Trained 8,000+ students globally in Photoshop, Illustrator, and InDesign — 4.9/5 course rating.", "4.9/5"),
    ("One of five Adobe-authorized training partners in the Middle East — certified Instructor and Expert.", None),
    ("This training background directly drives above-average Salesforce user adoption outcomes at every client.", None),
]: bullet(b, badge)

# ---- Certifications
section("Certifications")
certs = [
    "✔ Salesforce Certified Administrator — Mar 2023", "✔ Salesforce Certified Platform App Builder — Apr 2023",
    "✔ Salesforce Certified Associate — Nov 2023", "✔ Salesforce Certified AI Associate — Nov 2023",
    "✔ Adobe Certified Instructor (Ps, Ai, InDesign) — 2019", "✔ Adobe Certified Expert (Ps, Ai, InDesign) — 2019",
]
for i in range(0, len(certs), 2):
    pdf.set_x(14)
    pdf.set_font("dv", "", 8.2); pdf.set_text_color(*INK)
    pdf.cell(91, 5.2, certs[i])
    if i + 1 < len(certs):
        pdf.cell(91, 5.2, certs[i + 1])
    pdf.ln(5.2)
pdf.set_x(14)
pdf.cell(0, 5.2, "★★ Trailhead Double Star Ranger — 20 Superbadges · 210+ Badges · 130k+ Points  ·  Verify: salesforce.com/trailblazer/amrmagdyai")
pdf.ln(5.2)

# ---- Education
section("Education")
para("Bachelor of Business Administration  ·  Faculty of Commerce, Cairo University  ·  2020  ·  Cairo")
para("Arabic — Native    ·    English — Fluent")

pdf.output("Amr_Magdy_CV.pdf")
print("Done:", pdf.page_no(), "pages")
