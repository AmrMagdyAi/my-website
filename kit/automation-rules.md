# Wholesaling CRM Field Kit: Automation Rules

Ten plain-English rules that keep the fields in this kit filled in and honest.
Each rule has a Salesforce hint and an "any CRM" hint, because the logic is the
same whether you use Salesforce, REsimpli, Podio, HubSpot or a spreadsheet.

Field names match lead-fields.csv, deal-fields.csv and buyer-fields.csv.
Times and day counts below are starting points. Change them to fit your team.

From the Wholesaling CRM Field Kit by Amr Magdy: https://amrmagdy.com/crm-field-kit.html
Free to use, copy and change.

---

## 1. No lead leaves New without a source

**Rule:** When Status changes from New to anything else and Lead Source is empty → block save. If Lead Source is a paid channel and Campaign is empty → block save.

- **Salesforce:** Validation rule on Lead: `AND(ISCHANGED(Status__c), PRIORVALUE(Status__c) = "New", ISBLANK(TEXT(Lead_Source__c)))`.
- **Any CRM:** Make Lead Source a required field on every stage after New. If your CRM can't require fields by stage, run a daily list of leads past New with no source and fix them.

## 2. Every logged touch counts, and the first one is stamped

**Rule:** When a call, text or email to the seller is logged → add 1 to Touch Count. If First Contact At is empty → stamp it with the time of that touch.

- **Salesforce:** Record-triggered Flow on Task (after save) that updates the related lead. Minutes to First Attempt is then a formula: `(First_Contact_At__c - CreatedDate) * 1440`.
- **Any CRM:** Use the activity count your CRM already keeps if it has one. Otherwise, a workflow or Zapier/Make step that increments a number field when an activity is logged.

## 3. A missed seller call becomes a callback task in 5 minutes

**Rule:** When an inbound call to a marketing number is missed → set Missed Call Callback Due to now + 5 minutes and create a callback task, due at that time, for the lead owner (or the next available rep if the lead is new). When the callback is logged → clear Missed Call Callback Due.

- **Salesforce:** Record-triggered Flow on the call record your phone integration creates (Task or a custom call object), filtered on missed/unanswered inbound calls.
- **Any CRM:** Most dialers can send a webhook or trigger a workflow on a missed call. Point it at "create task, due in 5 minutes, assigned to owner". Review a missed-calls-without-callback list every day.

## 4. No open lead without a next date

**Rule:** When a lead is saved with Status not Dead and not Under Contract and Next Task Date is empty → block save.

- **Salesforce:** Validation rule on Lead: `AND(NOT(ISPICKVAL(Status__c, "Dead")), NOT(ISPICKVAL(Status__c, "Under Contract")), ISBLANK(Next_Task_Date__c))`.
- **Any CRM:** Required field while the lead is open, or a saved view of "open leads with no next task" that someone clears every morning.

## 5. Dead needs a reason

**Rule:** When Status changes to Dead and Dead Reason is empty → block save.

- **Salesforce:** Validation rule on Lead: `AND(ISPICKVAL(Status__c, "Dead"), ISBLANK(TEXT(Dead_Reason__c)))`.
- **Any CRM:** Make Dead Reason required on the Dead stage. If that's not possible, report Dead leads with no reason weekly and send them back to the rep.

## 6. Dead Reason sets the revisit date

**Rule:** When Dead Reason is set → fill Revisit On:
- Not motivated → today + 90 days
- Price too high → today + 60 days
- Listed with agent → today + 120 days (around when many listings expire)
- Other → today + 90 days
- Wrong number or Sold → leave empty (no revisit)

On the Revisit On date → set Status to Nurture and create a follow-up task for the owner.

- **Salesforce:** Record-triggered Flow on Lead (before save) for the date, plus a scheduled path on Revisit On for the task and status change.
- **Any CRM:** A date field filled by workflow, or a saved view of "Dead leads where Revisit On is today or earlier" worked once a week.

## 7. Offers above MAO need a second pair of eyes

**Rule:** When Offer Amount > MAO (Offer Above MAO is TRUE) → Deal Status can't move to Offer Sent until Manager Approved is checked.

- **Salesforce:** Approval process on the deal (Opportunity or custom object) with entry criteria `Offer_Above_MAO__c = TRUE`, plus a validation rule that blocks Offer Sent while `AND(Offer_Above_MAO__c, NOT(Manager_Approved__c))`.
- **Any CRM:** Required checkbox when the offer is above MAO, or a rule that notifies the manager and moves the deal to a "Needs approval" stage.

## 8. Signing a contract stamps the numbers that matter later

**Rule:** When a lead's Status changes to Under Contract or a deal's Deal Status changes to Under Contract → stamp Contract Signed Date, copy Touch Count into Touch # at Contract, copy Lead Source and Campaign from the lead to the deal, require Booked Fee, and lock all three against edits.

- **Salesforce:** Record-triggered Flow on Opportunity (or your deal object). Lock source fields with a validation rule using `ISCHANGED()` and a permission bypass for admins.
- **Any CRM:** A stage-change workflow that copies the fields. If your CRM can't lock fields, restrict who can edit them and check source changes in the audit log.

## 9. A fall-out zeroes the fee and records why

**Rule:** When Deal Status changes to Fell Out → Fall-out Reason is required and Kept Fee is set to 0. When a deal closes with Kept Fee lower than Booked Fee → Fall-out Reason is required (choose Renegotiated if that's what happened).

- **Salesforce:** Validation rule for the required reason; before-save Flow to set `Kept_Fee__c = 0` on Fell Out.
- **Any CRM:** Required field on the Fell Out stage, and a rule or habit that Kept Fee is never left at the booked number.

## 10. Every Monday, list the hot leads nobody touched

**Rule:** Every Monday morning → list leads where Status = Hot and there has been no logged activity in 14 or more days, grouped by owner, and send it to each owner and the acquisitions manager.

- **Salesforce:** Report on Leads filtered `Status = Hot` and `Last Activity <= 14 days ago` (or a custom last-touch date), subscribed for Monday delivery.
- **Any CRM:** A saved filter or smart view with the same conditions. If there's no scheduled delivery, put "open the stale Hot leads view" on the Monday meeting agenda.

---

Want help setting these up? https://amrmagdy.com/crm-revenue-audit.html
