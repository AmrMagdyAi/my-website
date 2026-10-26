#!/usr/bin/env python3
"""Build Amr_Magdy_CV.pdf in the amrmagdy.com look (assets/site.css, the brand print kit).
Requires: pip install fpdf2. Fonts are in scripts/fonts (DM Sans, DM Serif Display; SIL OFL)."""
import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# Light-theme colors from assets/site.css
INK = (34, 32, 29)        # --ink
INK2 = (77, 72, 66)       # --ink2
INK3 = (107, 100, 93)     # --ink3
LINE = (228, 221, 210)    # --line
PAPER = (255, 253, 249)   # --paper
TEAL = (15, 118, 110)     # --teal: the fix, "after"
TEAL_INK = (11, 92, 86)   # --teal-ink
ROSE = (155, 93, 93)      # --rose: the leak, "before"

F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + os.sep
SITE = "https://amrmagdy.com/?utm_source=pdf&utm_medium=cv"
MAIL = "mailto:info@AmrMagdy.com"
LINKEDIN = "https://www.linkedin.com/in/amrmagdyai"
PW, PH = 215.9, 279.4     # US Letter
L = 15
W = PW - 2 * L

class CV(FPDF):
    def header(self):
        self.set_fill_color(*PAPER)
        self.rect(0, 0, PW, PH, "F")
        if self.page_no() > 1:
            self.set_xy(L, 9)
            self.parts_line([("Amr Magdy — Salesforce CRM Consultant · amrmagdy.com", SITE)], 8, INK3, align="R", h=6)
            self.set_y(19)

    def footer(self):
        self.set_y(-14)
        self.parts_line([("info@AmrMagdy.com", MAIL), ("  ·  ", None), ("amrmagdy.com", SITE), ("  ·  ", None),
                         ("linkedin.com/in/amrmagdyai", LINKEDIN), (f"  ·  Page {self.page_no()}", None)],
                        7.5, INK3, align="C", h=6)
        # every page ends on the 7px rose | teal edge
        edge = 7 * 25.4 / 96
        self.set_fill_color(*ROSE); self.rect(0, PH - edge, PW / 2, edge, "F")
        self.set_fill_color(*TEAL); self.rect(PW / 2, PH - edge, PW / 2, edge, "F")

    def parts_line(self, parts, size, color, align="L", h=5, x=L):
        """One line of (text, link) parts, so each address in it is clickable."""
        self.set_font("sans", "", size); self.set_text_color(*color)
        total = sum(self.get_string_width(t) for t, _ in parts)
        self.set_x({"L": x, "C": L + (W - total) / 2, "R": L + W - total}[align])
        for t, url in parts:
            self.cell(self.get_string_width(t), h, t, link=url or "")
        self.ln(h)

pdf = CV("P", "mm", "Letter")
pdf.add_font("sans", "", F + "DMSans-Regular.ttf")
pdf.add_font("sans", "B", F + "DMSans-SemiBold.ttf")
pdf.add_font("serif", "", F + "DMSerifDisplay-Regular.ttf")
pdf.add_font("serif", "I", F + "DMSerifDisplay-Italic.ttf")
pdf.set_margins(L, 14, L)
pdf.set_auto_page_break(True, margin=19)
pdf.set_title("Amr Magdy - CV"); pdf.set_author("Amr Magdy"); pdf.set_lang("en")
pdf.add_page()

# ---- Name, role line and contact
pdf.set_xy(L, 13)
pdf.set_font("serif", "", 26); pdf.set_text_color(*INK)
pdf.cell(W, 11, "Amr Magdy Abd El-Fattah", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("serif", "I", 13); pdf.set_text_color(*TEAL_INK)
pdf.cell(W, 7, "Salesforce CRM Consultant", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("sans", "", 9); pdf.set_text_color(*INK2)
pdf.cell(W, 5.5, "Apex & LWC Development  ·  Certified Admin & App Builder  ·  Remote", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.parts_line([("info@AmrMagdy.com", MAIL), ("  ·  +20 103 327 5250  ·  ", None), ("amrmagdy.com", SITE),
                ("  ·  ", None), ("linkedin.com/in/amrmagdyai", LINKEDIN)], 8.2, INK3, h=5.5)
pdf.ln(2.5)
pdf.set_draw_color(*LINE); pdf.set_line_width(0.3)
pdf.line(L, pdf.get_y(), L + W, pdf.get_y())

# ---- (stat bar removed: its numbers were all from the Central City role)

def section(title):
    pdf.ln(3.5)
    if pdf.get_y() > PH - 45: pdf.add_page()
    pdf.set_x(L)
    pdf.set_font("serif", "", 14); pdf.set_text_color(*INK)
    pdf.cell(W, 7, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_draw_color(*LINE); pdf.set_line_width(0.3)
    pdf.line(L, pdf.get_y() + 0.5, L + W, pdf.get_y() + 0.5)
    pdf.ln(3)

def para(txt, size=8.8, color=INK):
    pdf.set_font("sans", "", size); pdf.set_text_color(*color)
    pdf.set_x(L); pdf.multi_cell(W, 4.6, txt, align="L")
    pdf.ln(1)

def role(title, dates, org, intro=None):
    if pdf.get_y() > PH - 42: pdf.add_page()
    pdf.set_x(L)
    pdf.set_font("sans", "B", 10); pdf.set_text_color(*INK)
    pdf.cell(W - 45, 5.5, title)
    pdf.set_font("sans", "B", 8.4); pdf.set_text_color(*TEAL_INK)
    pdf.cell(45, 5.5, dates, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(L)
    pdf.set_font("sans", "", 8.4); pdf.set_text_color(*INK3)
    pdf.cell(W, 4.6, org, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(0.8)
    if intro:
        para(intro, 8.6, INK2)

def bullet(txt, badge=None):
    # teal bullet, text hanging from it, the badge (a real result) in teal at the end
    pdf.set_left_margin(L + 5.5)
    pdf.set_x(L + 2)
    pdf.set_font("sans", "", 8.6); pdf.set_text_color(*TEAL)
    pdf.cell(3.5, 4.5, "•")
    pdf.set_text_color(*INK)
    pdf.write(4.5, txt)
    if badge:
        pdf.set_font("sans", "B", 8.6); pdf.set_text_color(*TEAL_INK)
        pdf.write(4.5, "  " + badge)
    pdf.ln(4.5)
    pdf.set_left_margin(L)
    pdf.ln(0.7)

# ---- Summary
section("Professional Summary")
para("Strategic Salesforce CRM Consultant with hands-on Apex and LWC development experience, specializing in "
     "real estate. I build the systems real estate companies actually run on — centralized Configuration Objects "
     "that run the automation rules, custom Apex integrations syncing RingCentral call logs, Kanban LWC components "
     "deployed company-wide, full-funnel campaign ROI dashboards, and multi-system integrations. "
     "My 8-year background as an Adobe Certified Instructor (8,000+ students, 4.9/5 rating) means the solutions I "
     "build get genuinely adopted — not just delivered.")

# ---- Expertise
section("Core Expertise")
cols = [
    ("Salesforce Platform", ["Flow Builder & Process Automation", "Apex (Schedulable, Queueable, Batch, Triggers)",
     "Lightning Web Components (LWC)", "Configuration Object Architecture", "Reports, Dashboards & Scorecards",
     "Data Loader & Mass Updates"]),
    ("Integrations & Tools", ["RingCentral Apex API Sync", "DocuSign, QuickBooks",
     "SmrtPhone, Zapier, Google Drive", "Tableau Connected to Salesforce", "Python for Data Cleaning & Migration",
     "Salesforce ↔ Slack Direct Integration"]),
    ("Real Estate Specialty", ["Lead Routing & Speed-to-Lead Automation", "Campaign Attribution via Call Tracking",
     "Transaction Coordination Workflows", "Marketing ROI Tracking by Campaign", "Property Acquisition Pipeline Architecture",
     "Duplicate Lead Detection & Management"]),
]
cw = W / 3
x0 = L; ytop = pdf.get_y()
maxy = ytop
for i, (h, items) in enumerate(cols):
    x = x0 + i * cw
    pdf.set_xy(x, ytop)
    pdf.set_font("sans", "B", 8.6); pdf.set_text_color(*TEAL_INK)
    pdf.cell(cw - 4, 5, h)
    yy = ytop + 6
    for it in items:
        pdf.set_xy(x, yy)
        pdf.set_font("sans", "", 8.2); pdf.set_text_color(*TEAL)
        pdf.cell(3, 4.1, "•")
        pdf.set_text_color(*INK)
        pdf.multi_cell(cw - 7, 4.1, it, align="L")
        yy = pdf.get_y() + 0.6
    maxy = max(maxy, yy)
pdf.set_y(maxy + 1)

# ---- Experience
section("Professional Experience")

role("Salesforce CRM Consultant", "Jun 2024 – Present",
     "Two-market home-buying company  ·  Remote · Ohio, USA",
     "Real estate acquisition company — full-cycle CRM design, Apex development, LWC customization, and multi-system integration.")
for b, badge in [
    ("Built a centralized Configuration Object that runs the automation rules (Slack, email, SMS, tasks) — non-technical users add and disable automations without developer involvement.", None),
    ("Developed MergeFieldReplacer Apex class replacing merge field tokens in automation templates with live Salesforce data, supporting cross-object lookups, date arithmetic, and system variables.", None),
    ("Built RCDailyCallLogSync — Schedulable Apex with chained Queueable processing that auto-syncs RingCentral call logs into Salesforce Tasks daily, matching calls to Leads by phone number.", None),
    ("Migrated the Zapier automations to native Salesforce Flows after repeated API limit violations — eliminating external dependency, cutting costs, and improving trigger speed from minutes to milliseconds.", None),
    ("Integrated RingCentral, DocuSign, QuickBooks, SmrtPhone, Google Drive, and Tableau with Salesforce — all synced automatically.", None),
    ("Built custom LWC Queue Task Manager with sort/filter, color-coded dates, custom mobile notifications, and utility bar deployment — adopted company-wide.", None),
    ("Designed complete Transaction Coordination system: custom Kanban LWC board, automated task triggers, DocuSign status tracking, TC scorecard, and post-close review automation.", None),
    ("Built Marketing ROI dashboard tracking cost-per-lead, cost-per-appointment, and lead-to-contract rates by campaign — driving weekly leadership decisions.", None),
    ("Used Python to clean leads with invalid phone fields, bulk-updated lead-campaign mappings, and managed the onboarding of the prospect buyer database.", None),
    ("Built intelligent duplicate lead detection: preserved historical homeowner records, copied campaign strategy, and sent real-time Slack alerts on every duplicate.", None),
]: bullet(b, badge)
pdf.ln(1.5)

role("Salesforce CRM Consultant (Post-Implementation)", "Apr 2025 – Jun 2025",
     "Pezon Properties  ·  Remote · PA, USA",
     "Handover consulting after the main implementation — 50+ delivered requests ensuring the incoming developer had a fully documented, stable platform.")
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
def check(x, y):
    pdf.set_draw_color(*TEAL); pdf.set_line_width(0.45)
    pdf.polyline([(x + 0.2, y + 2.6), (x + 1.1, y + 3.5), (x + 2.8, y + 1.5)])

def cert(x, w, label):
    if label.startswith("✔ "):
        check(x, pdf.get_y())
        label = label[2:]
    elif label.startswith("★★ "):
        pdf.set_fill_color(*TEAL)
        for dx in (0.8, 3.2):
            pdf.star(x + dx, pdf.get_y() + 2.45, 0.6, 1.35, 5, rotate_degrees=-90, style="F")
        label = label[3:]
    pdf.set_xy(x + 5, pdf.get_y())
    pdf.set_font("sans", "", 8.6); pdf.set_text_color(*INK)
    pdf.cell(w - 5, 5.2, label)

for i in range(0, len(certs), 2):
    y = pdf.get_y()
    cert(L, W / 2, certs[i])
    if i + 1 < len(certs):
        pdf.set_y(y)
        cert(L + W / 2, W / 2, certs[i + 1])
    pdf.set_y(y + 5.4)
cert(L, W, "★★ Trailhead Double Star Ranger — 20 Superbadges · 210+ Badges · 130k+ Points")
pdf.set_y(pdf.get_y() + 5.4)
pdf.parts_line([("Verify certifications: ", None), ("salesforce.com/trailblazer/amrmagdyai", "https://www.salesforce.com/trailblazer/amrmagdyai")], 8.6, INK2, h=5.2, x=L + 5)

# ---- Education
section("Education")
para("Bachelor of Business Administration  ·  Faculty of Commerce, Cairo University  ·  2020  ·  Cairo")
para("Arabic — Native    ·    English — Fluent")

pdf.output("Amr_Magdy_CV.pdf")
print("Done:", pdf.page_no(), "pages")
