# Wholesaling CRM Field Kit: Monday 5 Report Spec

The five numbers an investor owner should see every Monday, and the exact
fields each one reads from. Field names match lead-fields.csv and
deal-fields.csv in this kit. The reasoning behind each number is on
https://amrmagdy.com/monday-5-real-estate-kpis.html

From the Wholesaling CRM Field Kit by Amr Magdy: https://amrmagdy.com/crm-field-kit.html
Free to use, copy and change.

## One thing you need besides the kit fields

**Campaign spend.** Each campaign (a mailer drop, a PPC month, a cold-call list)
needs a record with its spend for the period. In Salesforce that's the standard
Campaign object and its Actual Cost field. In other CRMs it can be a simple
campaign list or a spreadsheet tab with Campaign name, Period and Spend. Every
lead and deal points to a campaign through the Campaign field.

Run every number for last week and for the last 13 weeks, so one odd week doesn't drive the decision.

---

## 1. Cost per appointment, by campaign

**Question:** Which channel is actually worth the money?

**Formula:** Campaign spend ÷ appointments set from that campaign's leads.

**Reads from:**
- Lead: Campaign, Lead Source, Appointment Set Date
- Campaign: Spend (Actual Cost)

**Report:** Leads with Appointment Set Date in the period, counted and grouped by Campaign, next to that campaign's spend for the same period.

## 2. Contracts per campaign

**Question:** Where do signed deals really come from?

**Formula:** Count of signed contracts, traced back to the original lead's campaign.

**Reads from:**
- Deal: Campaign (copied from the lead and locked), Lead Source, Contract Signed Date

**Report:** Deals with Contract Signed Date in the period, grouped by Campaign and Lead Source. Repeat sellers keep their first source.

## 3. Contract to first seller call

**Question:** Are we keeping deals warm until closing?

**Formula:** Hours between Contract Signed Date and the first logged call to the seller after it.

**Reads from:**
- Deal: Contract Signed Date, First Seller Call After Contract, Hours Contract to First Seller Call (formula), deal owner

**Report:** Average Hours Contract to First Seller Call by owner, plus a list of deals under contract where First Seller Call After Contract is still empty. Pick the hour threshold that fits your team.

## 4. Booked vs. kept profit

**Question:** What did we book, and how close was the forecast?

**Formula:** Sum of Booked Fee compared with sum of Kept Fee for the same deals.

**Reads from:**
- Deal: Booked Fee (locked at signing), Kept Fee, Closed Date, Deal Status, Fall-out Reason

**Report:** Two parts. (a) Booked Fee on contracts signed this week. (b) For deals that closed or fell out in the period: Booked Fee vs. Kept Fee, with the gap broken down by Fall-out Reason.

## 5. Campaign ROI, including the houses you keep

**Question:** Is our best channel being undercounted?

**Formula:** (Sum of Kept Fee + sum of Kept House Equity − campaign spend) ÷ campaign spend, by campaign. Kept House Equity is after-repair value minus all-in cost, so a house you keep counts what it added, not its full price.

**Reads from:**
- Deal: Campaign, Kept Fee, Kept House Equity, Closed Date
- Campaign: Spend (Actual Cost)

**Report:** By campaign, over the last 13 weeks or longer (deals take weeks to close, so a one-week ROI is noise). Uses Kept Fee, never Booked Fee, so cancelled and renegotiated contracts don't inflate the result.

---

Want this built as one dashboard? https://amrmagdy.com/crm-revenue-audit.html
