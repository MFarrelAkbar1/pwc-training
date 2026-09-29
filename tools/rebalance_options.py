"""Rebalance option lengths and answer positions in the English and Technical tests.

1. REWRITE gives new option texts (correct first) for questions where the correct
   option was noticeably longer than the distractors.
2. Every test is then rebalanced so each letter A-D is the answer equally often.
   English error-spotting questions keep their order: their letters match the
   (A)-(D) marks inside the sentence.
Seeded, so re-running gives the same result. Run: python tools/rebalance_options.py
"""
import json
import random
from pathlib import Path
from statistics import mean

DATA = Path(__file__).resolve().parent.parent / "site" / "data"
LETTERS = "ABCD"

# id -> [correct, wrong, wrong, wrong]
REWRITE = {
    # ---------------- Technical 1
    "T1-Q01": ["Access to programs and data, program changes, development and IT operations",
               "Revenue, purchasing, payroll and treasury cycles across all business units",
               "Input, processing and output checks built into a single application",
               "Preventive, detective and corrective controls over financial reporting"],
    "T1-Q02": ["Remove access promptly on HR leaver notice, backed by periodic access reviews",
               "Review the password policy each year and enforce much stronger complexity rules",
               "Encrypt the finance database and restrict who holds the encryption keys",
               "Require formal approval and testing before any change goes live"],
    "T1-Q03": ["Unreviewed or untested changes can reach production",
               "System performance may drop during busy processing periods",
               "Software licences may be exceeded as more users are added",
               "Nightly backups may fail if production changes too often"],
    "T1-Q04": ["The policy or standard the condition is measured against",
               "The facts the auditor actually observed during testing",
               "The underlying reason the issue was able to happen",
               "The actual or potential impact of the issue on the business"],
    "T1-Q06": ["Random sampling", "Judgmental sampling", "Haphazard sampling", "Block sampling"],
    "T1-Q07": ["A system three-way match of order, receipt and invoice before payment",
               "A quarterly review of all ERP user accounts by the IT security team",
               "A nightly backup of the ERP database copied to a second data centre",
               "A change advisory board that approves all ERP changes each week"],
    "T1-Q08": ["Only authorised, tested and approved changes reach production",
               "Changes reach production as quickly as the business requests them",
               "A complete list of software licences is kept up to date",
               "Users can adjust their own access when their role changes"],
    "T1-Q09": ["The maximum acceptable data loss, measured in time",
               "The maximum acceptable downtime after a disruption",
               "The distance required between primary and backup sites",
               "The number of backup copies that must be retained"],
    "T1-Q11": ["A certifiable standard for an information security management system",
               "A framework for the governance and management of enterprise IT",
               "An internal control framework for reliable financial reporting",
               "A professional standard for the audit of annual financial statements"],
    "T1-Q12": ["Pressure, opportunity and rationalisation", "Motive, means and method",
               "Planning, fieldwork and reporting", "Prevention, detection and incident response"],
    "T1-Q13": ["Actions can't be traced to one person", "The shared password may expire too often",
               "The ERP may run out of named user licences", "Scheduled backups may fail to run overnight"],
    "T1-Q14": ["A confirmation sent directly to the auditor by a third party",
               "A detailed verbal explanation given by the finance manager",
               "A spreadsheet prepared internally by the auditee's own team",
               "A scanned copy of an invoice emailed to the auditor by the auditee"],
    "T1-Q15": ["Find the cause, check the 3 changes and report the exceptions",
               "Accept the result, since 88% of the sample was approved",
               "Replace the 3 exceptions with new items from the population",
               "Stop the audit and report that all change controls failed"],
    "T1-Q18": ["The reviewer is checking access they granted themselves",
               "Monthly reviews are more frequent than is necessary",
               "The review should cover all company systems at the same time",
               "Payroll access doesn't need to be reviewed at all"],
    "T1-Q20": ["An independent monthly review of the bank reconciliations",
               "Asking the employee to sign the code of conduct each year",
               "Rotating the employee to a different desk each quarter",
               "Raising the employee's pay to reduce any financial pressure"],
    # ---------------- Technical 2
    "T2-Q01": ["Governance and management of enterprise IT",
               "Certifying an information security management system",
               "Designing controls over financial reporting",
               "Running day-to-day IT service desk operations"],
    "T2-Q03": ["Reviewing an exception report of posted manual journals",
               "A system rule requiring two approvals before payment release",
               "Password rules requiring length and complexity at login",
               "Input checks that reject invalid dates as data is keyed"],
    "T2-Q04": ["Data can be changed outside change and application controls",
               "The production database may run out of disk storage space quickly",
               "Developers may take longer to finish their projects",
               "Overnight backups may take longer than scheduled"],
    "T2-Q05": ["Set the objectives, scope and risk-based approach",
               "Write the final report and agree it with management",
               "Agree action plans and target dates for each finding",
               "Test every transaction in the period under review"],
    "T2-Q06": ["Sampling risk can be measured and results projected",
               "It always needs a smaller sample than other methods",
               "It removes the need for any auditor judgement",
               "It focuses the sample on the highest-value items"],
    "T2-Q08": ["The actual or potential impact on the organisation",
               "The standard or policy that should have been met",
               "The facts the auditor observed during testing",
               "The underlying reason the problem occurred"],
    "T2-Q09": ["The maximum acceptable time to restore a system",
               "The maximum acceptable amount of data that can be lost",
               "How often backups of the system are taken",
               "How long backup copies are retained for"],
    "T2-Q10": ["Test restores periodically to prove backups work",
               "Take backups twice a day instead of once",
               "Keep each backup for a longer retention period",
               "Move backups to a different storage vendor"],
    "T2-Q11": ["Users get only the access their job requires",
               "Only managers are allowed any system access",
               "All access is reviewed at least once a year",
               "Administrators get unrestricted access"],
    "T2-Q13": ["Escalate under the audit charter and record the scope limitation",
               "Skip the test quietly and leave it out of the report",
               "Obtain the logs from another system administrator without consent",
               "Conclude the control is effective since no issue was found"],
    "T2-Q14": ["The audit committee of the board", "The chief financial officer",
               "The chief information officer (CIO)", "The external audit partner"],
    "T2-Q15": ["Never takes leave and won't let others do their tasks",
               "Takes all of their annual leave entitlement every year",
               "Regularly asks for extra training and development",
               "Documents their work carefully and keeps records tidy"],
    "T2-Q16": ["A risk management or compliance function", "A sales team applying pricing controls",
               "The internal audit department", "The company's external auditors"],
    "T2-Q17": ["Missing or duplicated records go undetected", "The order system slows down at month end",
               "Users forget their passwords for the ledger", "The ledger needs more storage each year"],
    "T2-Q18": ["Confirm understanding of the process and key controls",
               "Test that a control operated correctly across the whole year",
               "Agree the final report wording with management",
               "Count physical inventory at the period end"],
    "T2-Q19": ["Whether it worked consistently throughout the period",
               "Whether it is designed to address the relevant risk",
               "Whether it is written down in a procedure document",
               "Whether management finds it useful and practical"],
    "T2-Q20": ["Trace shipping documents forward to invoices", "Trace invoices back to shipping documents",
               "Send confirmations to a sample of customers", "Recalculate the totals on a sample of invoices"],
    # ---------------- Technical 3
    "T3-Q01": ["Monitoring batch jobs and following up failures", "A three-way match check in the ERP purchasing module",
               "Credit limit checks on new customer orders", "Segregating approval of journal entries"],
    "T3-Q02": ["Allow them, but review and approve each soon after release",
               "Ban all emergency changes to production immediately",
               "Test every emergency change fully before any release to production",
               "Only allow emergency changes to be made at weekends"],
    "T3-Q03": ["Creating vendors and approving payments to them",
               "Reading system reports and printing those reports",
               "Receiving goods and storing them in the warehouse",
               "Attending training and signing the code of conduct"],
    "T3-Q04": ["Business users, to confirm it meets their needs",
               "The developers who wrote and unit-tested the code",
               "The external auditor, as part of the year-end audit",
               "The database administrator, just before go-live"],
    "T3-Q05": ["Migrated data may be incomplete or inaccurate", "Users may need more training on the new ERP",
               "The old system may never be switched off", "Licence costs may rise in the following year"],
    "T3-Q06": ["Focuses audit effort on the highest-risk areas", "Audits every area with equal effort each year",
               "Audits only the areas that management selects", "Covers IT systems but not business processes"],
    "T3-Q07": ["The relevance and reliability of the evidence", "The amount of evidence the auditor collects",
               "Whether the evidence is held electronically", "Whether management agrees with the evidence"],
    "T3-Q08": ["The control isn't operating: review results aren't acted on",
               "The control works, because every review was signed on time",
               "No conclusion is possible without testing a larger sample",
               "Only the reviewers who signed need further training"],
    "T3-Q09": ["The overall conclusion and the key findings", "Every test performed, described step by step",
               "The auditors' detailed working papers", "A full list of everyone who was interviewed"],
    "T3-Q10": ["A specific action, an owner and a target date", "The auditor's own opinion of the finding and nothing else",
               "A general promise to look into the issue", "The names of the audit team members"],
    "T3-Q12": ["The Statement of Applicability", "The business continuity plan",
               "The risk appetite statement", "The internal audit charter"],
    "T3-Q13": ["Call the supplier back on contact details already on file",
               "Ask the caller to confirm the change request by email instead",
               "Pay the supplier by cheque for the next invoice only",
               "Review all supplier payments together at year end"],
    "T3-Q14": ["Taking cash before it is recorded", "Recording sales that never happened",
               "Inflating personal expense claims", "Paying invoices from a fake supplier"],
    "T3-Q15": ["The risk left after controls are applied", "The risk before any controls are applied",
               "The risk of choosing the wrong sample", "The total risk the organisation will accept"],
    "T3-Q16": ["The risk an organisation is willing to take on", "The number of risks in the risk register",
               "The risk that remains once all the controls operate", "The likelihood that a given risk occurs"],
    "T3-Q17": ["Escalate confidentially per the fraud procedure and keep evidence",
               "Confront the manager straight away and ask for a full explanation",
               "Ignore it, because fraud is outside the audit's scope",
               "Warn the manager's team so they can watch out for it"],
    "T3-Q18": ["Testing the whole population, not just a sample", "No longer needing to plan the audit work",
               "Replacing the controls that management operates day to day", "Guaranteeing that no fraud has occurred"],
    "T3-Q19": ["So the fix addresses the problem, not just the symptom",
               "So the right person can be blamed for the issue",
               "So the audit report looks more thorough to all its readers",
               "So the audit fee can be justified to management"],
    "T3-Q20": ["Report it to management now to remove access and investigate",
               "Note it down and include it in next year's internal audit plan",
               "Disable the accounts yourself using admin rights",
               "Wait and include it in the final audit report"],
    # ---------------- English reading questions
    "E1-Q14": ["likely to ease as suppliers got used to it.", "caused by errors in the new approval system.",
               "the main reason approval times increased.", "due to managers rejecting more invoices."],
    "E1-Q19": ["hybrid working may not explain the drop in turnover.",
               "hybrid working actually caused turnover to increase.",
               "the finance director miscalculated the net saving.",
               "the firm should move back to all five floors."],
    "E2-Q13": ["Results and a drawback of a new fraud model", "Why purchases made abroad are especially risky",
               "How internal audit teams investigate card fraud", "The history and growth of Northgate Bank"],
    "E2-Q14": ["It declined many genuine purchases abroad.", "It ignored the size of each transaction.",
               "It was too expensive for the bank to run.", "It relied entirely on machine learning."],
    "E2-Q16": ["the model's lack of explainability.", "the cost of building the model.",
               "fraud losses rising after launch.", "changes in customer spending patterns."],
    "E2-Q19": ["It aims to avoid relying on one supplier.", "It will lower unit prices even further.",
               "It was introduced before the fire happened.", "It applies only to packaging materials."],
    "E3-Q15": ["frequent callers may already be unhappy with the network.",
               "hiring more support staff would certainly cut cancellations.",
               "the call data was probably collected incorrectly.",
               "customers who call once are the least satisfied."],
    "E3-Q18": ["checking physical inventory.", "reviewing electronic documents.",
               "planning the scope of the audit.", "reducing the cost of travel."],
    "E3-Q19": ["Remote document review, on-site observation", "Doing every part of the audit remotely",
               "Returning fully to on-site visits for all audit work", "Replacing audits with self-assessments"],
    "E3-Q20": ["the files were already electronic.", "auditors were more experienced.",
               "inventory levels were lower that year.", "managers travelled less during 2020."],
}


def fixed_order(q):
    """Error-spotting questions: option letters are tied to (A)-(D) marks in the sentence."""
    return q.get("skill") == "written expression"


def bias(questions):
    longest = sum(1 for q in questions
                  if len(q["options"][q["answer"]]) > max(len(v) for k, v in q["options"].items() if k != q["answer"]))
    ratio = mean(len(q["options"][q["answer"]]) /
                 mean(len(v) for k, v in q["options"].items() if k != q["answer"]) for q in questions)
    return longest, ratio


def main():
    rng = random.Random(4242)
    # English 4-6 and Technical 4-8 are built (already balanced) by tools/gen_english.py and tools/gen_technical.py;
    # including them here would reshuffle them and shift the seeded order used for Technical 1-3.
    for path in sorted(DATA.glob("english-[123].json")) + sorted(DATA.glob("technical-[123].json")):
        test = json.loads(path.read_text(encoding="utf-8"))
        qs = test["questions"]
        before = bias(qs)

        # 1. options as [correct, *wrong] (rewritten where listed)
        texts = {}
        for q in qs:
            if q["id"] in REWRITE:
                new = REWRITE[q["id"]]
                assert len(new) == 4 and len(set(new)) == 4, q["id"]
                texts[q["id"]] = new
            else:
                texts[q["id"]] = [q["options"][q["answer"]]] + [v for k, v in q["options"].items() if k != q["answer"]]

        # 2. choose answer letters so A-D each appear len/4 times; fixed questions keep theirs
        quota = {letter: len(qs) // 4 for letter in LETTERS}
        for q in qs:
            if fixed_order(q):
                quota[q["answer"]] -= 1
        pool = [letter for letter, n in quota.items() for _ in range(n)]
        rng.shuffle(pool)
        movable = [q for q in qs if not fixed_order(q)]
        assert len(pool) == len(movable), path.name

        for q, letter in zip(movable, pool):
            correct, *wrong = texts[q["id"]]
            rng.shuffle(wrong)
            slots = wrong[:]
            slots.insert(LETTERS.index(letter), correct)
            q["options"] = dict(zip(LETTERS, slots))
            q["answer"] = letter
        for q in qs:
            if fixed_order(q):
                assert q["id"] not in REWRITE

        after = bias(qs)
        counts = {letter: sum(q["answer"] == letter for q in qs) for letter in LETTERS}
        print(f"{path.name}: correct longest {before[0]:>2} -> {after[0]:>2} of {len(qs)}; "
              f"avg length ratio {before[1]:.2f} -> {after[1]:.2f}; answers {counts}")
        path.write_text(json.dumps(test, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
