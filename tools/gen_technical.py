"""Write the Technical (Risk Assurance) tests T4-T8 to site/data/technical-4..8.json.

  T4 IT general controls                   logical access, change management, IT operations
  T5 Cybersecurity & frameworks            ISO/IEC 27001:2022, NIST CSF 2.0, attacks and controls, incident response
  T6 Governance, risk & internal control   COSO 2013, COBIT 2019, IIA Three Lines, risk, control types, ICFR, evidence
  T7 Data, privacy, cloud & third parties  UU PDP (Law 27/2022), data governance/analytics, cloud, SOC reports, BCP/DR
  T8 Mixed mock exam                       all of the above

All content is original, written for this site. T1-T3 were hand-written JSON (balanced afterwards by
tools/rebalance_options.py); these tests keep the same schema (type definition/scenario, level easy/medium/hard,
4 options, 20 minutes) plus a topic, and live here so a question can be fixed and the JSON rebuilt.
Facts tied to a standard, law or number were checked against the sources listed in REVIEW.md.

Options are listed correct first; the correct option is then moved to a seeded letter so each test uses A-D
exactly five times. The script refuses to write a test whose difficulty mix, scenario share or option lengths
would give the answer away. Run: python tools/gen_technical.py
"""
import json
import random
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "site" / "data"
LETTERS = "ABCD"
LEVELS = {"easy": 6, "medium": 10, "hard": 4}  # per test: 30% / 50% / 20%
TIME_LIMIT_SEC = 1200  # 20 minutes, like T1-T3
S, D = "scenario", "definition"

# (topic, type, level, question, [correct, wrong, wrong, wrong], explanation)

# ---------------------------------------------------------------- T4 IT general controls
T4 = [
    ("logical access", D, "easy",
     "What does role-based access control (RBAC) mean?",
     ["Access is granted through roles that match job functions",
      "Users get the same standard access so work isn't held up",
      "Users pick their own permissions within an overall limit",
      "Access is granted according to each person's seniority"],
     "RBAC bundles permissions into roles designed around job functions, and users get roles, not ad-hoc rights. "
     "Access by seniority is tempting because senior staff often have more access, but rank is not a job need."),
    ("privileged access", D, "easy",
     "Why do auditors pay special attention to privileged accounts such as database or domain administrators?",
     ["They can bypass controls and change data, settings and access",
      "They are used by more staff than any other kind of user account",
      "They cost more in licence fees than normal user accounts",
      "They are created automatically and can't be removed later"],
     "Privileged accounts can change configurations, security settings, data and other users' rights, so misuse can "
     "defeat other controls. They are usually held by few people, not most staff, which is why they must be restricted."),
    ("segregation of duties", S, "medium",
     "The IT security administrator who creates user accounts in the ERP also holds a finance role in the same ERP "
     "that allows posting journal entries. What is the main risk?",
     ["They could give themselves extra access and post unauthorised entries",
      "The ERP may slow down because one person holds two quite different roles",
      "Their journal entries may be posted to the wrong accounting period",
      "They may forget their password more often with two separate roles"],
     "Administering access is incompatible with using the system for transactions: the person could grant rights "
     "and use them without anyone else being involved. Posting to the wrong period is a normal processing error, not "
     "the segregation-of-duties risk this combination creates."),
    ("periodic access review", S, "hard",
     "A manager signs off the quarterly access review of the general ledger system using a user list emailed by IT. "
     "To rely on this control, what else should the auditor check?",
     ["That the user list was complete and accurate when it was extracted",
      "That the manager has a professional qualification in IT security",
      "That the list was sent as a password-protected spreadsheet file",
      "That the review was signed within one working day after the quarter ended"],
     "A review is only as good as its input: if the report the reviewer relies on is incomplete (information produced "
     "by the entity), some users are never reviewed. Signing within one day isn't required; the review just has to be "
     "timely enough to be effective."),
    ("access modification", S, "medium",
     "An employee moved from the procurement team to the sales team six months ago and still has purchase-approval "
     "rights in the ERP. Which access control failed?",
     ["Changing access when a user moves to a new role",
      "Removing access when an employee leaves the company",
      "Approving program changes before they reach production",
      "Enforcing a minimum password length for all ERP users"],
     "This is a mover: access should be adjusted, and old rights removed, when a role changes. The leaver process is "
     "tempting, but the employee hasn't left, so leaver controls wouldn't have caught this."),
    ("privileged access", S, "medium",
     "Database administrators (DBAs) need unrestricted access to the production database to do their jobs. Which "
     "control best reduces the risk of this access being misused?",
     ["Log DBA activity and have someone independent review the logs",
      "Remove all DBA access and let the software vendor do the work",
      "Ask the DBAs to sign an acceptable use policy once every year",
      "Change the DBA passwords every 30 days and keep them complex"],
     "When access can't be restricted further, an independent review of what privileged users actually did is the "
     "compensating control. Changing passwords protects against outsiders using the account, not against the DBAs "
     "themselves misusing it."),
    ("change management", D, "easy",
     "Why should program changes be tested in an environment separate from production?",
     ["So a faulty change can't affect live data or users",
      "So developers don't need to document what they change",
      "So users can use new features before they are approved",
      "So the change can go live without business sign-off"],
     "A separate test environment lets errors show up without damaging live data or disrupting users. It doesn't "
     "remove the need for documentation or approval; those are separate change-management steps."),
    ("change management", S, "hard",
     "An auditor selects 25 changes from the change ticketing system to test for approval. Which extra step best "
     "addresses the risk that some changes reached production without any ticket at all?",
     ["Compare a system-generated list of production changes to the tickets",
      "Select a larger sample of changes from the same ticketing system",
      "Interview the developers about how they usually log and record their changes",
      "Check that every ticket in the sample has an attached test script"],
     "Changes made outside the process never appear in the ticketing system, so the population must come from the "
     "system itself (e.g. change logs or object timestamps) and be matched to tickets. A bigger sample from the "
     "ticketing system is tempting, but it can only find problems with changes that were logged."),
    ("change management", S, "medium",
     "At a small company, one developer both builds changes and is the only person able to move them into "
     "production. Segregating these duties isn't possible. Which compensating control is most appropriate?",
     ["Independent review of production change logs against approved tickets",
      "Ask the developer to test every change twice before releasing it",
      "Have the developer email the CIO a short summary note after every release",
      "Limit the developer's production access to normal office hours"],
     "Someone independent checks, after the fact, that everything that reached production was approved, which "
     "catches unauthorised changes. An email from the developer is tempting, but it is self-reported, so it would "
     "leave out exactly the changes that matter."),
    ("emergency changes", S, "medium",
     "An auditor finds that 40% of all changes to the ERP last year were logged as emergency changes. What does "
     "this most likely indicate?",
     ["The emergency route may be used to bypass normal change controls",
      "The change management process is working quickly and efficiently",
      "The ERP has too few users to justify a standard change process",
      "Testing of normal changes is more thorough than it needs to be"],
     "Emergency changes should be rare because they skip some approval and testing before release. A high share "
     "suggests the lighter route is being used for convenience. Speed is not a sign of a working control when the "
     "checks are being skipped."),
    ("change management", D, "medium",
     "Which is the best evidence that a change was tested and accepted before it was released?",
     ["Test results signed off by the business user before the release date",
      "A written statement by the developer that the change was fully tested",
      "A production log showing the date and time the change was deployed",
      "Approval of the change request by the IT manager after the release"],
     "Dated user acceptance before release shows both that testing happened and that it came first. The developer's "
     "own statement is tempting, but it isn't independent and doesn't show what was tested."),
    ("job scheduling", S, "medium",
     "Any member of the IT support team can add, change or delete jobs in the batch scheduler that runs the monthly "
     "interest calculation. What is the main risk?",
     ["Jobs could be changed without authorisation, affecting financial data",
      "The scheduler could run out of disk space during month-end processing",
      "Jobs could run faster than the finance team is able to review them",
      "Support staff would need more training to use the batch scheduler"],
     "The scheduler decides what runs, when and with which parameters, so unrestricted edit rights let anyone alter "
     "financial processing. Disk space is an operational capacity issue, not an authorisation risk."),
    ("backup", D, "easy",
     "Why are backup copies kept at a separate location, such as another site or cloud region?",
     ["So a disaster at the main site doesn't destroy the backups too",
      "So that backup jobs finish faster over the company's internal network",
      "So that restoring data from backup no longer needs approval",
      "So that the company needs to take backups less frequently"],
     "Backups exist to survive the loss of the primary site; if they sit in the same building, a fire or flood takes "
     "both. Offsite copies usually make backups slower, not faster."),
    ("incident management", D, "medium",
     "In IT service management (e.g. ITIL), what is the difference between an incident and a problem?",
     ["An incident is a disruption; a problem is the cause behind incidents",
      "A problem is a minor incident that is logged in a separate queue",
      "Incidents affect users, while problems affect servers and networks",
      "An incident is caused by users; a problem is caused by IT staff"],
     "An incident is an unplanned interruption or loss of service quality; a problem is the cause, or potential "
     "cause, of one or more incidents. Treating a problem as a small incident mixes up restoring service with "
     "fixing the root cause."),
    ("incident management", S, "medium",
     "The IT incident log shows high-priority incidents are recorded, but many are closed with no note of how they "
     "were resolved, and several keep coming back. What should the auditor recommend?",
     ["Require resolution notes and root-cause review for recurring incidents",
      "Reduce the number of priority levels so fewer incidents are high",
      "Stop logging low-priority incidents so support staff can focus on the important ones",
      "Let users close their own incidents once the service works again"],
     "Without resolution records, nobody can check that the fix was proper, and recurring incidents point to an "
     "unaddressed cause that problem management should investigate. Fewer priority levels only relabels incidents."),
    ("backup", S, "hard",
     "Nightly backups of the finance server are scheduled. Failure alerts go to a shared mailbox nobody monitors, and "
     "12 backups failed during the year without being rerun. What should the auditor conclude?",
     ["The control isn't operating effectively, as failures aren't followed up",
      "The control is effective because the backups are scheduled every night",
      "The control is effective because about 97% of the backups succeeded",
      "There is no issue because no data was actually lost during the year"],
     "The control is not just scheduling a backup; it includes detecting and fixing failures. Nobody does that, so "
     "the control failed each time. A high success rate is tempting, but the failures were random and unnoticed, so "
     "any day's data could have been unrecoverable."),
    ("ITGC reliance", D, "medium",
     "Why does it matter to an auditor relying on automated application controls if the ITGCs over that system "
     "are ineffective?",
     ["The auditor can't assume the automated controls ran consistently",
      "Automated controls turn into manual controls once the ITGCs have failed",
      "The company's financial statements must then be restated",
      "The auditor has to stop further testing of that system"],
     "Effective ITGCs (especially change and access) give comfort that a configured control stayed the same all "
     "year. Without them, it could have been changed or bypassed, so more testing is needed. A restatement doesn't "
     "follow: ITGC failures raise risk, they are not misstatements."),
    ("logical access", D, "easy",
     "An ERP locks a user account after five failed login attempts. What does this setting mainly protect against?",
     ["Attackers guessing passwords",
      "Staff sharing their passwords",
      "Leavers keeping their access",
      "Changes made without approval"],
     "Lockout limits how many guesses an attacker gets. Password sharing is tempting, but a colleague who is given "
     "the right password logs in on the first try, so lockout doesn't stop it."),
    ("segregation of duties", S, "hard",
     "An SoD analysis shows 40 users with conflicting access in the ERP. Management says the conflicts are needed "
     "because the finance team is small. What is the most appropriate response?",
     ["Check whether mitigating controls exist and work for these users",
      "Report all 40 users to the audit committee as confirmed fraud cases",
      "Accept management's explanation and take no further audit action",
      "Recommend removing all ERP access for the 40 users straight away"],
     "Conflicts can be acceptable if a mitigating control (e.g. an independent review of their transactions) covers "
     "the risk, so the auditor tests for that before rating the issue. Removing all access is tempting but ignores "
     "the business need; conflicting access alone isn't fraud either."),
    ("access provisioning", S, "easy",
     "When testing new user accounts, an auditor finds that for 4 of 25 new users the approval is dated after the "
     "account was created. What is this?",
     ["A control exception: access was granted before it was approved",
      "Not an issue, because each of the users was approved in the end",
      "A matter for the users' managers rather than an exception",
      "A design weakness in the password settings of the application"],
     "The provisioning control is approval before access. Approval after the fact means the users had unauthorised "
     "access for a time. \"Approved in the end\" is tempting, but a late approval can't stop what happened in between."),
]

# ---------------------------------------------------------------- T5 Cybersecurity & frameworks
T5 = [
    ("ISO/IEC 27001", D, "hard",
     "Which part of ISO/IEC 27001:2022 contains the mandatory management-system requirements, such as leadership, "
     "risk assessment, internal audit and management review?",
     ["Clauses 4 to 10", "Annex A", "Clauses 1 to 3", "ISO/IEC 27002"],
     "Clauses 4–10 (context, leadership, planning, support, operation, performance evaluation, improvement) are the "
     "requirements for the ISMS. Annex A is tempting, but it is the reference list of controls that the risk "
     "treatment process uses; clauses 1–3 are scope, references and terms, and ISO/IEC 27002 is guidance."),
    ("ISO/IEC 27001", D, "easy",
     "ISO/IEC 27001:2022 groups its Annex A controls into four themes. Which list is correct?",
     ["Organizational, people, physical, technological",
      "Identify, protect, detect, respond",
      "Preventive, detective, corrective, compensating",
      "Policy, access, operations, compliance"],
     "The 2022 edition has 93 controls in four themes: organizational (37), people (8), physical (14) and "
     "technological (34). \"Identify, protect, detect, respond\" are NIST CSF functions, and preventive / detective / "
     "corrective are control types, not themes."),
    ("ISO/IEC 27001", D, "medium",
     "Under ISO/IEC 27001:2022 Annex A, which theme contains the control on screening (background checks) of job "
     "candidates?",
     ["People", "Organizational", "Physical", "Technological"],
     "Screening is control 6.1, the first of the eight people controls, which cover the employment life cycle. "
     "Organizational is tempting because HR policies feel organisation-wide, but the 2022 edition puts screening "
     "under people."),
    ("ISO/IEC 27001", D, "medium",
     "An ISMS risk assessment finds a risk above the organisation's acceptance criteria. Which is NOT an acceptable "
     "way to handle it?",
     ["Ignore it and record no decision",
      "Add controls to reduce the risk",
      "Share the risk, e.g. by insurance",
      "Stop the activity causing the risk"],
     "Reducing, sharing, avoiding and (formally) retaining a risk are all valid treatments, but each must be a "
     "documented decision that the risk owner approves. Retaining a risk is allowed; silently ignoring it isn't."),
    ("ISO/IEC 27001", S, "hard",
     "A company certified to ISO/IEC 27001 hasn't held a management review of its ISMS for two years, although the "
     "security team meets every week. What should the auditor conclude?",
     ["A nonconformity: top management must review the ISMS at planned intervals",
      "No issue, since the weekly security team meetings replace the formal review",
      "No issue, since management review is optional guidance in the standard",
      "An opportunity for improvement, not a nonconformity"],
     "Clause 9.3 requires top management to review the ISMS at planned intervals, with set inputs and outputs. "
     "Team meetings are tempting as a substitute, but they aren't top management reviewing the whole ISMS, and a "
     "required activity that is missing is a nonconformity, not just an improvement point."),
    ("NIST CSF 2.0", D, "easy",
     "Which function was added to the NIST Cybersecurity Framework in version 2.0 (2024)?",
     ["Govern", "Monitor", "Comply", "Prepare"],
     "CSF 2.0 has six functions: Govern, Identify, Protect, Detect, Respond and Recover. Govern is new and sits at the "
     "centre. \"Monitor\" and \"Prepare\" are common security words but are not CSF functions."),
    ("NIST CSF 2.0", S, "medium",
     "A company sets up alerts in its SIEM for unusual logins outside working hours. Which NIST CSF 2.0 function "
     "does this mainly support?",
     ["Detect", "Protect", "Respond", "Govern"],
     "Detect covers finding and analysing possible attacks and anomalies, including continuous monitoring. Protect "
     "is tempting, but an alert doesn't stop the login; it reveals it."),
    ("NIST CSF 2.0", S, "medium",
     "The board approves a cybersecurity risk strategy, sets roles and responsibilities, and defines security "
     "expectations for suppliers. Which NIST CSF 2.0 function covers these activities?",
     ["Govern", "Identify", "Protect", "Recover"],
     "Govern covers strategy, roles, policy, oversight and cybersecurity supply chain risk management. Identify is "
     "tempting (in version 1.1 some of this sat there), but in 2.0 it covers understanding assets and risks, not "
     "setting strategy."),
    ("phishing", S, "easy",
     "Several staff receive an email that appears to come from the CEO, urgently asking them to buy gift cards and "
     "send the codes. What kind of attack is this?",
     ["Phishing (social engineering)", "Denial of service",
      "SQL injection", "Brute-force password guessing attack"],
     "It tricks people, not systems, by impersonating a trusted sender and creating urgency. Nothing is flooded "
     "(denial of service) or guessed (brute force)."),
    ("MFA", D, "easy",
     "Which of these is true multi-factor authentication?",
     ["A password plus a code from an app on the user's phone",
      "A password plus the answer to a secret security question",
      "Two different passwords entered one after the other",
      "A username plus a long and complex password"],
     "MFA needs factors of different types: something you know, have or are. The phone app is something you have. "
     "A security question is tempting, but it is a second thing you know, so it's the same factor twice."),
    ("ransomware", S, "medium",
     "After a ransomware attack, a company finds that its backups, kept on a network drive in the same domain, were "
     "also encrypted. Which control would best have protected the backups?",
     ["Offline or immutable backup copies kept apart from the main network",
      "Running backups more often to the same network drive as before",
      "Stronger antivirus software installed on all employee laptops",
      "A longer and more complex password for the backup service account"],
     "Ransomware encrypts everything it can reach, so at least one copy must be unreachable or unchangeable. More "
     "frequent backups to the same drive are tempting, but they would have been encrypted as well."),
    ("encryption", D, "easy",
     "What is the main purpose of full-disk encryption on a company laptop?",
     ["Keeping data unreadable if the laptop is lost or stolen",
      "Protecting the laptop from being infected by malware",
      "Stopping users from copying company files to USB drives",
      "Protecting data while it is sent over the internet"],
     "Disk encryption protects data at rest: without the key, a thief can't read the drive. Data sent over the "
     "internet is data in transit, which TLS protects, not disk encryption."),
    ("encryption", D, "hard",
     "Why should an application store user passwords as salted hashes rather than in encrypted form?",
     ["A hash is one-way, so stored passwords can't simply be decrypted",
      "Hashing makes the password database smaller and faster to search",
      "ISO/IEC 27001 requires hashing and forbids encrypting passwords",
      "Salted hashes let administrators recover passwords users forget"],
     "Encrypted passwords can be decrypted by anyone who gets the key; a hash can only be checked, not reversed, and "
     "the salt stops precomputed-table attacks. Recovering forgotten passwords is exactly what a hash prevents; "
     "users reset them instead."),
    ("patching", S, "medium",
     "A vendor releases a critical patch for a vulnerability that is being actively exploited. Company policy "
     "applies all patches in a quarterly cycle. What should the auditor recommend?",
     ["Patch by risk, fixing critical exploited flaws within days",
      "Keep the quarterly cycle so that all patches are treated alike",
      "Apply every patch to production the same day, skipping tests",
      "Wait for the next major version upgrade rather than patching"],
     "A risk-based policy speeds up critical, actively exploited fixes while routine patches follow the normal "
     "cycle, still with suitable testing. Patching everything with no testing is tempting as the fast answer, but it "
     "trades one risk for another."),
    ("OWASP", D, "medium",
     "Which is the most effective control against SQL injection in a web application?",
     ["Parameterised queries (prepared statements)",
      "Encrypting the database files stored on disk",
      "Hiding detailed error messages from all users",
      "Requiring HTTPS for every page of the website"],
     "Parameterised queries keep user input as data, so it can never be run as SQL. Hiding error messages is "
     "tempting and helps a little, but the injection still works; it just gives the attacker less feedback."),
    ("OWASP", S, "medium",
     "Logged in as customer 1001, a tester changes the URL from /invoice?id=1001 to /invoice?id=1002 and sees "
     "another customer's invoice. What kind of weakness is this?",
     ["Broken access control", "Cross-site scripting (XSS)",
      "Weak encryption in transit", "Denial of service"],
     "The server doesn't check that the logged-in user may see the requested record (an insecure direct object "
     "reference), which OWASP groups under broken access control. XSS would inject a script into a page; nothing is "
     "injected here."),
    ("incident response", S, "medium",
     "The security team confirms that malware on one server is spreading to other machines on the network. What "
     "should they do first?",
     ["Contain it, e.g. isolate the server from the network",
      "Wipe the server and rebuild it from scratch right away",
      "Write the lessons-learned report for management",
      "Email every customer to tell them about the attack"],
     "While the malware is spreading, stopping it comes first; containment limits the damage and keeps evidence. "
     "Rebuilding is tempting but comes after containment and analysis, and wiping first destroys evidence."),
    ("incident response", S, "hard",
     "During a suspected breach, an IT administrator wants to shut down and reimage a compromised server at once to "
     "\"clean it up\". What is the main concern?",
     ["Evidence such as memory and logs could be lost before analysis",
      "Reimaging a server usually takes longer than restoring a backup",
      "The operating system licence may become invalid after reimaging",
      "All users of the server would need to reset their passwords"],
     "Shutting down erases memory, and reimaging overwrites the disk, so the team may never learn how the attacker "
     "got in or what was taken. Password resets may be needed anyway, but they are a separate step, not a reason "
     "to wait."),
    ("incident response", D, "easy",
     "What is the main purpose of a post-incident (lessons-learned) review?",
     ["Improve controls so similar incidents are less likely",
      "Decide which employee should be disciplined for the incident",
      "Close the incident ticket as quickly as possible",
      "Work out the insurance claim for the incident"],
     "The review looks at what happened and how the response went, then feeds improvements back into controls and "
     "plans. It is deliberately not about blame, so people report honestly."),
    ("vulnerability management", D, "medium",
     "What is the main difference between a vulnerability scan and a penetration test?",
     ["A pen test tries to exploit weaknesses; a scan only finds them",
      "A scan is done by hand, while a pen test is fully automated",
      "A pen test covers the physical security of the building",
      "They are the same test, sold under different names"],
     "A scan is a mostly automated check for known weaknesses; a penetration test goes further and tries to exploit "
     "them, showing the real impact. \"Scan by hand, pen test automated\" has it backwards: scans are the automated part."),
]

# ---------------------------------------------------------------- T6 Governance, risk & internal control
T6 = [
    ("COSO", D, "easy",
     "Which COSO internal control component covers identifying and analysing risks to objectives, including the "
     "risk of fraud?",
     ["Risk assessment", "Control activities", "Monitoring activities", "Control environment"],
     "Risk assessment (principles 6–9) covers setting objectives, identifying and analysing risks, assessing fraud "
     "risk and significant changes. Control activities are the responses to those risks, not their analysis."),
    ("COSO", S, "medium",
     "Internal audit carries out periodic separate evaluations of whether controls are present and working, and "
     "reports deficiencies to management and the board. Which COSO component is this?",
     ["Monitoring activities", "Control activities",
      "Information and communication", "Risk assessment"],
     "Monitoring activities are ongoing and separate evaluations of the whole system of internal control, plus "
     "reporting deficiencies. Control activities are tempting, but those are the controls themselves, not the "
     "checking of them."),
    ("COSO", S, "medium",
     "A new policy requires approval of all discounts above 10%, but it was only saved to a shared folder and most "
     "sales staff don't know about it. Which COSO component is weakest?",
     ["Information and communication", "Control environment",
      "Risk assessment", "Monitoring activities"],
     "The control exists but was never communicated to the people who have to follow it, which is an information and "
     "communication failure. Control environment is tempting because it covers culture, but here the gap is that the "
     "message never reached staff."),
    ("COSO", D, "hard",
     "COSO's Internal Control – Integrated Framework (2013) supports its five components with how many principles?",
     ["17", "5", "12", "20"],
     "COSO 2013 has 17 principles spread over the 5 components, and each must be present and functioning for "
     "effective internal control. Five is the number of components, not principles."),
    ("COBIT", D, "medium",
     "In COBIT 2019, how is governance distinguished from management?",
     ["Governance evaluates, directs and monitors; management plans, builds and runs",
      "Governance is carried out by IT staff, while management is done by the business",
      "Governance covers legal compliance, while management covers operations and delivery",
      "There is no difference; the two words refer to the same set of IT activities"],
     "COBIT separates governance (evaluate, direct, monitor, usually by the board) from management (plan, build, "
     "run, monitor, by executives). IT staff vs business is tempting, but both sides involve business leaders."),
    ("COBIT", D, "hard",
     "Which COBIT 2019 domain contains the governance objectives?",
     ["Evaluate, Direct and Monitor (EDM)", "Monitor, Evaluate and Assess (MEA)",
      "Align, Plan and Organise (APO)", "Deliver, Service and Support (DSS)"],
     "EDM holds the five governance objectives; APO, BAI, DSS and MEA hold the 35 management objectives. MEA is "
     "tempting because it also \"monitors\", but it is a management domain for performance and conformance."),
    ("Three Lines Model", S, "medium",
     "The head of internal audit is asked to also design and run the company's new risk management process. Under "
     "the IIA Three Lines Model, what is the main concern?",
     ["Internal audit would later be auditing work it designed and runs",
      "Risk management must be run by the first line, not the second",
      "The board isn't allowed to oversee how risk management is done",
      "Internal audit isn't permitted to advise management on risk topics"],
     "The third line must stay independent of management responsibilities; running the process would mean auditing "
     "its own work. It may still give advice, so saying it can't advise is too strict."),
    ("Three Lines Model", S, "easy",
     "A sales manager checks and approves discounts above a set limit for the sales team. In the Three Lines Model, "
     "whose role is this?",
     ["A first-line role", "A second-line role", "A third-line role", "The governing body's"],
     "The first line provides products and services and manages the risks that come with them, including day-to-day "
     "controls. Second-line roles (risk, compliance) support and challenge the first line; they don't approve its "
     "discounts."),
    ("risk assessment", S, "medium",
     "Payment fraud risk is rated likelihood 4 and impact 5 (scales of 1–5) before controls. After dual approval is "
     "introduced, likelihood falls to 2 and impact stays the same. Using likelihood × impact, what is the residual "
     "risk score?",
     ["10", "20", "8", "4"],
     "Residual risk is the risk after controls: 2 × 5 = 10. The inherent score was 4 × 5 = 20, which is tempting if "
     "you forget that the control changed the likelihood."),
    ("risk response", S, "easy",
     "A company buys cyber insurance to cover losses from a possible data breach. Which risk response is this?",
     ["Share (transfer)", "Accept (retain)", "Avoid (exit)", "Reduce (mitigate)"],
     "Insurance moves part of the financial impact to the insurer. It doesn't lower the chance of a breach, so it is "
     "not \"reduce\"."),
    ("risk response", S, "medium",
     "After controls, a risk's residual rating is still above the risk appetite approved by the board. What is the "
     "most appropriate next step?",
     ["Add further controls or escalate it for a formal decision",
      "Re-rate the inherent risk lower so the residual fits appetite",
      "Accept the risk, since some controls are already in place",
      "Remove it from the risk register until the event happens"],
     "A risk outside appetite needs more treatment, or a decision by someone with authority to accept it. Accepting "
     "it just because controls exist is tempting, but that isn't within anyone's authority when the board set the "
     "appetite lower."),
    ("control types", S, "medium",
     "The ERP blocks any payment to a vendor that is not in the approved vendor master file. What type of control "
     "is this?",
     ["Automated preventive", "Automated detective", "Manual preventive", "Manual detective"],
     "The system (automated) stops the payment before it happens (preventive). Detective is tempting if you think of "
     "an exception report, but here nothing is reported after the fact; the payment never happens."),
    ("key controls", D, "medium",
     "In testing internal control over financial reporting, what makes a control a \"key control\"?",
     ["It is relied on to prevent or detect a material misstatement",
      "It is carried out by the most senior person in the process",
      "It is the control that costs the most money to operate",
      "It runs automatically in the system, with no human input needed"],
     "Key controls are the ones that address the significant risks of material misstatement, so they are what the "
     "auditor tests. Seniority is tempting, but a clerk's control can be key and a director's can be redundant."),
    ("ICFR / SOX", D, "hard",
     "In ICFR (e.g. under SOX), what is a material weakness?",
     ["A deficiency making it reasonably possible that a material misstatement is not prevented or detected in time",
      "Any control deficiency, however small, that the external auditor identifies during the year's annual audit",
      "A deficiency that has already led to a restatement of the company's prior-year financial statements",
      "A deficiency found in any control that is performed by the members of senior management staff"],
     "A material weakness is a deficiency, or combination of deficiencies, with a reasonable possibility that a "
     "material misstatement won't be prevented or detected on time. A restatement is a strong indicator, which makes "
     "it tempting, but a weakness doesn't require that a misstatement has already happened."),
    ("ICFR / SOX", D, "easy",
     "Who is primarily responsible for designing and maintaining internal control over financial reporting?",
     ["Management", "The external auditor", "Internal audit", "The securities regulator"],
     "Management owns ICFR and (under SOX 404(a)) assesses it. The external auditor is tempting because it gives an "
     "opinion on ICFR for larger listed companies, but auditing controls doesn't make it responsible for them."),
    ("sampling", D, "medium",
     "Why do auditors usually test more items for a control performed many times a day than for one performed once "
     "a quarter?",
     ["More occurrences give more chances to fail, so more evidence is needed",
      "Daily controls are usually manual, so they are less reliable",
      "Quarterly controls are done by senior staff, so they need less testing",
      "Sample sizes are set mainly by how much time the audit budget allows"],
     "Sample size grows with control frequency because a small sample covers a smaller share of many occurrences. "
     "Daily controls can be automated or manual, so frequency says nothing about how reliable they are."),
    ("testing automated controls", S, "hard",
     "An automated three-way match in the ERP is configured correctly, and ITGCs over the ERP were effective all "
     "year. What testing of the automated control's operation is usually enough?",
     ["One instance of each relevant scenario (a test of one)",
      "25 items, the same as for a manual control done daily",
      "Every transaction processed in the year, one by one",
      "No direct testing, since the ITGCs were effective"],
     "An automated control does the same thing every time, so with effective ITGCs one example per scenario "
     "(match, mismatch) is enough. 25 items is tempting but comes from manual-control sampling. Effective ITGCs "
     "don't remove the need to test the control itself once."),
    ("audit evidence", S, "medium",
     "The finance manager tells the auditor that the CFO reviews all journals over IDR 1 billion. What should the "
     "auditor do next?",
     ["Corroborate it, e.g. inspect a sample of signed journals",
      "Accept the statement, as the finance manager is a senior person",
      "Report that the control does not exist in the company",
      "Ask the CFO to confirm the same statement by email"],
     "Inquiry alone isn't enough evidence that a control operates; it must be backed by inspection, observation or "
     "reperformance. An email from the CFO is tempting, but it is still just inquiry, only from another person."),
    ("audit evidence", D, "easy",
     "Which audit procedure means the auditor independently redoes a control or calculation?",
     ["Reperformance", "Inspection", "Observation", "Inquiry"],
     "Reperformance is independently carrying out the control again and comparing the results. Inspection only "
     "examines documents or records that the control produced."),
    ("governance", D, "easy",
     "In a listed company, which body oversees financial reporting, the external auditor and internal audit?",
     ["The audit committee", "The finance department",
      "The IT steering committee", "The general meeting of shareholders"],
     "The audit committee (a committee of the board, or in Indonesia of the board of commissioners) oversees "
     "reporting, the external auditor and internal audit. Shareholders appoint the board but don't oversee day to day."),
]

# ---------------------------------------------------------------- T7 Data, privacy, cloud & third parties
T7 = [
    ("UU PDP", D, "easy",
     "Under Indonesia's Personal Data Protection Law (UU PDP, Law No. 27 of 2022), which of these is specific "
     "(sensitive) personal data?",
     ["Health data", "Full name", "Nationality", "Marital status"],
     "Article 4 lists specific data as health, biometric, genetic, criminal records, children's data and personal "
     "financial data. Name, nationality and marital status are listed as general personal data."),
    ("UU PDP", D, "medium",
     "Under UU PDP, how quickly must a controller give written notice to the data subjects and the authority after "
     "a personal data protection failure?",
     ["Within 3 × 24 hours", "Within 7 calendar days", "Within 14 working days", "Within 30 days"],
     "Article 46 requires written notice within 3 × 24 hours (72 hours) to the data subjects and the institution, "
     "saying what data was exposed, when and how, and how it is being handled."),
    ("UU PDP", S, "medium",
     "A bank hires a payroll provider to process its employees' salary data on the bank's instructions. Under UU "
     "PDP, what are the two parties?",
     ["The bank is the controller; the provider is a processor",
      "The provider is the controller; the bank is a processor",
      "Both are joint controllers with equal responsibility",
      "The provider is the controller because it holds the data"],
     "The controller decides the purposes and control of processing; a processor acts on its behalf and on its "
     "instructions (Article 51). Holding the data doesn't make the provider a controller."),
    ("UU PDP", S, "hard",
     "A fintech plans to use an automated credit-scoring model that approves or rejects loans with no human review. "
     "What does UU PDP require before it starts this processing?",
     ["A data protection impact assessment",
      "Customers' acceptance of the terms of use",
      "Publishing the model's source code",
      "Certification of the model by an auditor"],
     "Article 34 requires an impact assessment for high-risk processing, which explicitly includes automated "
     "decisions with legal or significant effects on the data subject. Consent to terms is tempting, but consent "
     "is a basis for processing, not a replacement for the assessment."),
    ("UU PDP", S, "medium",
     "A data processor wants to hand part of the processing to another company (a sub-processor). What does UU PDP "
     "require first?",
     ["Written approval from the controller",
      "A notice to the data subjects",
      "An update to its privacy policy",
      "Approval from the processor's board"],
     "Article 51(5) requires the processor to get the controller's written approval before involving another "
     "processor. The controller stays responsible for the processing, which is why its consent is needed."),
    ("UU PDP", D, "easy",
     "Which of these is a right of the data subject under UU PDP?",
     ["Withdrawing consent they gave for processing",
      "Seeing other people's data held by the controller",
      "Setting the controller's internal retention policy",
      "Choosing which employee processes their own data"],
     "Data subjects may withdraw consent (Article 9), and also have rights to information, access, correction, "
     "erasure and portability. They can access their own data, not other people's."),
    ("UU PDP", D, "medium",
     "What is the maximum administrative fine under UU PDP?",
     ["2% of annual revenue", "4% of global turnover", "A flat IDR 5 billion", "10% of annual profit"],
     "Article 57(3) caps the administrative fine at 2% of annual income or revenue for the violation. 4% of global "
     "turnover is tempting because it is the EU GDPR maximum."),
    ("data governance", D, "easy",
     "In data governance, who is normally accountable for deciding the quality rules and access for a data set such "
     "as the customer master file?",
     ["The data owner in the business", "The IT database administrator",
      "The external auditor of the company", "Any user who works with the data"],
     "The business data owner is accountable for the data's quality, use and access. The database administrator is "
     "tempting, but that is the custodian role: running and protecting the data as the owner decides."),
    ("data analytics", S, "medium",
     "Analytics over a full year of payments finds 120 cases with the same vendor, invoice number and amount paid "
     "more than once. What should the auditor do next?",
     ["Investigate them to confirm which are real duplicate payments",
      "Report all 120 to management as confirmed losses to the company",
      "Ignore them, as analytics results often include false positives",
      "Delete the duplicate entries from the ERP to correct the ledger"],
     "Analytics results are exceptions to follow up, not conclusions: some may be credit-note reversals or split "
     "payments. Reporting all 120 as losses is tempting but not yet supported. Auditors never change the client's records."),
    ("data analytics", S, "hard",
     "An auditor receives a journal entry file extracted by the client for a full-year analytics test. What should "
     "the auditor do before running the tests?",
     ["Reconcile the file's totals to the trial balance to check it is complete",
      "Ask the client to confirm by email that the file contains every entry",
      "Remove all entries below a set amount so the analysis runs more quickly",
      "Convert the file to PDF format so no one can change it during testing"],
     "Analytics on an incomplete or altered extract gives false comfort, so the auditor first reconciles it to the "
     "ledger and checks record counts. An email confirmation is tempting, but it is only the client's word."),
    ("cloud", S, "easy",
     "A company uses a SaaS email service. Under the shared responsibility model, who manages which staff have "
     "accounts and what access they have?",
     ["The customer company", "The SaaS provider",
      "The internet provider", "The company's auditor"],
     "Whatever the service model, the customer is responsible for its identities, accounts and data. The SaaS "
     "provider runs the application and infrastructure, but it can't know who joined or left the company."),
    ("cloud", S, "medium",
     "A company runs its own virtual servers on an IaaS platform. An unpatched operating system on those servers is "
     "exploited. Under the shared responsibility model, who should have patched the operating system?",
     ["The customer", "The cloud provider",
      "Both equally, by default", "The hardware vendor"],
     "In IaaS the provider secures the physical hosts, network and virtualisation layer; the guest operating system "
     "and everything above it are the customer's. In PaaS the provider would patch the OS, which is why the provider "
     "is tempting."),
    ("UU PDP", S, "hard",
     "An Indonesian company plans to move customer personal data to a cloud region outside Indonesia. What does UU "
     "PDP expect it to ensure?",
     ["Equal or higher protection, binding safeguards, or consent",
      "That the cloud provider has a registered office in Indonesia",
      "A transfer ban: personal data must stay in Indonesia",
      "A separate written approval from each customer's own bank"],
     "Article 56 allows cross-border transfer if the recipient country's protection is equal or higher; otherwise "
     "adequate and binding safeguards are needed, and failing both, the data subject's consent. A total ban is "
     "tempting but wrong: the law regulates transfers, it doesn't forbid them."),
    ("SOC reports", S, "medium",
     "A company outsources payroll processing. Its external auditor wants assurance that the provider's controls "
     "relevant to financial reporting worked throughout the year. Which report fits best?",
     ["SOC 1 Type 2", "SOC 1 Type 1", "SOC 2 Type 1", "SOC 3"],
     "SOC 1 covers controls relevant to user entities' financial reporting, and Type 2 tests operating "
     "effectiveness over a period. SOC 1 Type 1 is tempting, but it only covers design at a point in time."),
    ("SOC reports", D, "easy",
     "What is the main difference between a SOC 2 Type 1 report and a SOC 2 Type 2 report?",
     ["Type 2 also tests if controls operated over a period",
      "Type 2 covers privacy, while Type 1 covers security",
      "Type 1 is for general use; Type 2 has restricted use",
      "Type 1 is done by internal audit; Type 2 by a CPA"],
     "Type 1 reports on the design of controls at a point in time; Type 2 adds tests of operating effectiveness "
     "over a period (often 6–12 months). The trust services criteria covered don't depend on the type."),
    ("SOC reports", S, "hard",
     "A clean SOC 1 Type 2 report on a cloud payroll provider lists complementary user entity controls (CUECs), "
     "such as customers reviewing user access to the payroll portal. What should the customer's auditor do about the CUECs?",
     ["Test that the customer performs the listed CUECs",
      "Rely on the report fully, with no further audit work",
      "Ask the provider to perform the CUECs instead",
      "Set the report aside because it lists CUECs"],
     "The provider's controls only achieve their objectives if the customer performs its complementary controls, so "
     "the auditor must test them at the customer. A clean opinion is tempting, but it assumes the CUECs are in place."),
    ("third-party risk", D, "medium",
     "Which is the most appropriate way to manage third-party risk across hundreds of vendors?",
     ["Tier vendors by risk and do deeper due diligence on high-risk ones",
      "Do the same full on-site audit of every vendor, however small, each year",
      "Assess the vendors with the largest contracts and skip the rest",
      "Rely on the signed contracts instead of doing assessments"],
     "Risk tiering puts effort where the risk is: data access, criticality, regulatory impact. Contract value is "
     "tempting, but a small vendor with access to customer data can be high risk."),
    ("third-party risk", S, "medium",
     "A vendor's SOC 2 report covers only its Singapore data centre, but your company's data is processed at its "
     "Jakarta facility. What should you do?",
     ["Get other assurance for Jakarta, as it's outside the report",
      "Rely on the report, since it is issued for the same vendor",
      "End the contract at once because the report is not useful",
      "Ask the vendor to add Jakarta to the report's cover letter"],
     "A SOC report gives assurance only for the systems and locations in its scope. Relying on it because it's the "
     "same vendor is tempting, but the Jakarta controls were never tested."),
    ("BCP / DR", S, "medium",
     "A system has a recovery point objective (RPO) of 1 hour, but its database is backed up only once a night. "
     "What is the gap?",
     ["Up to a day of data could be lost, well beyond the 1-hour target",
      "Recovery of the system could take longer than the 1-hour target allows",
      "There is no gap, since a backup is taken each day of the week",
      "Backups are taken more often than the target actually needs"],
     "RPO is about how much data can be lost; with nightly backups, a failure late in the day loses almost a day of "
     "work. Recovery time is the RTO, a different measure, which makes \"recovery could take longer\" tempting."),
    ("BCP / DR", D, "easy",
     "What is the purpose of a business impact analysis (BIA) in business continuity planning?",
     ["Find the critical processes and how fast each must recover",
      "Test whether the backups of key systems can be restored",
      "Decide which vendor to buy disaster recovery software from",
      "List every IT asset the company owns for insurance cover"],
     "The BIA identifies critical processes, the impact of disruption over time, and so the recovery objectives "
     "(e.g. RTO and RPO). Testing backups is a later step that checks the plan works."),
]

# ---------------------------------------------------------------- T8 Mixed mock exam
T8 = [
    ("ITGC scope", S, "easy",
     "An auditor is deciding which systems are in scope for ITGC testing in a financial statement audit. Which is "
     "most likely in scope?",
     ["The ERP that records sales and posts to the ledger",
      "The company's public marketing website on the internet",
      "The staff canteen's meal ordering app on phones",
      "The meeting room booking system at head office"],
     "ITGCs are tested for systems that support financial reporting, where a failure could affect the figures. A "
     "public website matters for cybersecurity, but it doesn't process the company's accounting."),
    ("change management", S, "medium",
     "A company uses a SaaS ERP whose vendor releases updates every month. What change-management control is still "
     "expected at the company?",
     ["Review the release notes and test the impact on key processes",
      "Approve each line of the vendor's source code before release",
      "Leave it to the vendor, which is responsible for ERP changes",
      "Block vendor updates permanently to keep the ERP stable and unchanged"],
     "The vendor controls its code, but the customer must understand how updates affect its configuration, reports "
     "and controls. \"The vendor is responsible\" is tempting, but it ignores the customer's side of the shared model."),
    ("MFA", S, "easy",
     "Attackers logged in to a company's VPN using an employee's stolen password. Which control would most directly "
     "have stopped this?",
     ["Multi-factor authentication on the VPN",
      "A longer password expiry period",
      "Annual security awareness training for staff",
      "Encrypting laptop hard drives"],
     "With MFA, a stolen password alone isn't enough to log in. Awareness training might have reduced the chance of "
     "the password being stolen, but it wouldn't stop the login once it was."),
    ("ISO/IEC 27001", S, "hard",
     "A software company that builds its own applications excludes the Annex A control on secure development from "
     "its Statement of Applicability, giving no reason. What should the ISO/IEC 27001 auditor conclude?",
     ["A nonconformity: the exclusion is unjustified and doesn't fit the risks",
      "Acceptable, as any Annex A control may be excluded without explanation",
      "Acceptable, as Annex A is guidance that certified firms may set aside",
      "Acceptable while no incident has been caused by the exclusion"],
     "The Statement of Applicability must justify every exclusion, and an exclusion must follow from the risk "
     "assessment. A developer excluding secure development with no reason fails both. Annex A isn't optional "
     "guidance: its controls must be compared with the ones chosen."),
    ("NIST CSF 2.0", S, "medium",
     "After an outage, the team restores systems from backups, confirms they work and updates stakeholders on "
     "progress. Which NIST CSF 2.0 function is this?",
     ["Recover", "Respond", "Protect", "Identify"],
     "Recover covers restoring assets and operations and communicating about recovery. Respond is tempting, but it "
     "covers managing and containing the incident itself, not restoring normal operations."),
    ("phishing", S, "medium",
     "In a phishing simulation, 30% of staff clicked the test link. What is the most appropriate response?",
     ["Targeted awareness training plus stronger email filtering",
      "Formal disciplinary action for every employee who clicked",
      "Block incoming external email for the whole company",
      "Stop the simulations, since the results were so poor"],
     "People and technical controls work together: training for those who clicked, filtering to cut how many phishing "
     "emails arrive. Disciplining everyone is tempting as a firm response but discourages reporting."),
    ("COSO", S, "easy",
     "A company requires two signatures on every payment above a set limit. Which COSO component does this belong to?",
     ["Control activities", "Control environment", "Risk assessment", "Monitoring activities"],
     "Dual authorisation is a control activity: an action set by policy to reduce a risk. Monitoring would be a "
     "later check that the dual-signature rule is actually followed."),
    ("Three Lines Model", D, "easy",
     "In the IIA Three Lines Model, who is accountable to stakeholders for oversight of the organisation?",
     ["The governing body", "Internal audit", "Management", "The external auditor"],
     "The governing body (e.g. the board) is accountable to stakeholders for oversight. Internal audit is tempting "
     "because it reports to the board, but it provides assurance and advice; it doesn't own oversight."),
    ("ICFR / SOX", S, "hard",
     "A key review control failed testing, but a separate control that detects the same misstatements was tested "
     "and found effective. How does this affect the evaluation?",
     ["The compensating control may reduce how severe the deficiency is",
      "The failed control is no longer treated as a deficiency",
      "Both controls now have to be reported as material weaknesses",
      "The compensating control has to be ignored in the evaluation"],
     "Compensating controls are considered when judging the severity of a deficiency, but the deficiency itself "
     "remains and is still reported at the right level. Saying it disappears is the tempting mistake."),
    ("audit evidence", D, "medium",
     "What is the main limitation of observation as audit evidence?",
     ["It shows only that the control ran while being watched",
      "It can't be written up in the audit working papers",
      "It isn't accepted as evidence for IT controls",
      "It is less reliable than just asking the staff member about it"],
     "Observation is good evidence at that moment, but people may act differently when watched, and it says nothing "
     "about the rest of the period. It is more reliable than inquiry, not less."),
    ("UU PDP", S, "medium",
     "A retailer collected customers' phone numbers to arrange deliveries and now wants to use them for marketing "
     "messages. Under UU PDP, what is needed?",
     ["A valid basis for the new purpose, e.g. explicit consent",
      "No new step, since the retailer already holds the numbers",
      "Just a limit of one marketing message a month",
      "Deleting the numbers, as phone numbers can't be stored"],
     "UU PDP requires processing to be limited to specific purposes and to have a lawful basis (Articles 16 and 20). "
     "A new purpose needs its own basis, typically consent for marketing. Already holding the data is not a basis."),
    ("UU PDP", S, "medium",
     "A customer asks a company to erase their personal data. No law requires the company to keep it and there is no "
     "legal dispute. What should the company do?",
     ["Erase the data and inform the customer that it was erased",
      "Keep the data indefinitely for future analytics projects",
      "Erase the customer's name but keep the other fields",
      "Refuse the request, because consent was given earlier"],
     "Data subjects may ask for erasure, and the controller must erase or destroy the data and tell the subject it "
     "has done so (Articles 8, 43–45). Earlier consent doesn't block this, since consent can be withdrawn."),
    ("cloud", S, "medium",
     "Before moving its accounting system to a cloud provider, which document best gives the company independent "
     "assurance over the provider's controls?",
     ["A recent SOC 1 or SOC 2 Type 2 report on the service",
      "The provider's marketing brochure about its security",
      "A reference call with one of the provider's customers",
      "The provider's own self-assessment questionnaire"],
     "A Type 2 SOC report is an independent auditor's opinion on controls tested over a period. A self-assessment is "
     "tempting because it is detailed, but it is written by the provider itself."),
    ("SOC reports", D, "hard",
     "Which SOC report is meant for general use and can be published, e.g. on the provider's website?",
     ["SOC 3", "SOC 2 Type 2", "SOC 1 Type 2", "SOC 1 Type 1"],
     "SOC 3 is a short general-use report on the trust services criteria. SOC 2 Type 2 covers the same criteria in "
     "detail, which is why it is tempting, but its use is restricted to people who understand the system."),
    ("BCP / DR", S, "hard",
     "A disaster recovery test restored the ERP at the backup site in 10 hours. The ERP's recovery time objective "
     "(RTO) is 4 hours. The IT manager records the test as \"passed\" because the system came back. What should "
     "the auditor conclude?",
     ["The test missed its RTO; the gap needs a remediation plan",
      "The test passed, because the system was fully recovered",
      "The test failed its recovery point objective, not the RTO",
      "The RTO should simply be changed to 10 hours to match"],
     "The RTO is the target the test measures, so 10 hours against 4 means the plan doesn't meet business needs. "
     "Raising the RTO is tempting, but the RTO comes from the business impact analysis; it can't be changed to fit "
     "a test result."),
    ("third-party risk", S, "medium",
     "Your key cloud vendor uses a subcontractor to run its data centres. What should your vendor due diligence "
     "cover?",
     ["How the vendor oversees its own subcontractors",
      "No review, as you have no contract with the subcontractor",
      "The subcontractor's prices for its services",
      "The subcontractor's marketing and brand policies"],
     "Risk flows through the supply chain, so due diligence covers how the vendor manages its fourth parties. Having "
     "no direct contract is tempting as a reason to stop, but the data is still exposed there."),
    ("data analytics", D, "medium",
     "In journal entry testing, which entries would an auditor usually treat as higher risk?",
     ["Manual entries posted at unusual times or by unusual users",
      "Entries created automatically by the billing interface",
      "Entries that are matched to approved purchase orders",
      "Recurring monthly depreciation entries set up by the finance team"],
     "Fraud through management override often shows up as manual entries at odd times, by unexpected users, with "
     "round amounts or odd accounts. Automated interface entries are routine and covered by other controls."),
    ("privileged access", S, "easy",
     "Most employees have local administrator rights on their company laptops. What is the main risk?",
     ["Users can install software, including malware, and turn off security",
      "The laptops will need to be backed up more often than other laptops",
      "Users are more likely to forget the password for their own laptop",
      "The network will become slower for other users across the company"],
     "Admin rights let users (and any malware running as them) install programs and disable protection. Backups and "
     "network speed aren't affected by who is an administrator."),
    ("encryption", D, "easy",
     "Which control protects data sent between a user's browser and a web application?",
     ["TLS (HTTPS)", "Full-disk encryption", "Database backups", "Account lockout"],
     "TLS encrypts data in transit between browser and server. Full-disk encryption is tempting as \"encryption\", "
     "but it protects data at rest on a device."),
    ("data governance", S, "medium",
     "The customer master file has many duplicate customers, created by different branches for the same person. "
     "Which control best prevents new duplicates?",
     ["A system duplicate check when a new customer is created",
      "A once-a-year clean-up by IT without any business input",
      "Letting each branch keep its own separate customer list",
      "Encrypting the customer master file on the database"],
     "A check at the point of entry stops duplicates before they exist (preventive). A yearly clean-up is tempting "
     "but detective and after the fact, and without the business it can merge the wrong records."),
]

TESTS = {
    4: ("IT General Controls", T4, 0.4),
    5: ("Cybersecurity & Frameworks", T5, 0.4),
    6: ("Governance, Risk & Internal Control", T6, 0.4),
    7: ("Data, Privacy, Cloud & Third Parties", T7, 0.4),
    8: ("Mixed Mock Exam", T8, 0.5),
}


def placed(rng, n):
    """Letters for the correct options: each of A-D n/4 times, in a seeded order."""
    pool = [letter for letter in LETTERS for _ in range(n // 4)]
    rng.shuffle(pool)
    return pool


# Questions whose options are fixed names (the COSO components), so the correct one can't be shortened. The
# longest name, "Information and communication", is also a wrong option in T6 #2, so length gives nothing away.
NAMED_OPTIONS = {"Information and communication"}


def length_report(items):
    """How often the correct option is the (strictly) longest / shortest, and the worst lead over every distractor."""
    longest = shortest = 0
    worst = 0
    for *_, (correct, *wrong), _ in items:
        lead = len(correct) - max(map(len, wrong))
        if correct not in NAMED_OPTIONS:
            worst = max(worst, lead)
        longest += lead > 0
        shortest += len(correct) < min(map(len, wrong))
    return longest, shortest, worst


def check(number, items, min_scenario):
    assert len(items) == 20, (number, len(items))
    levels = {lvl: sum(i[2] == lvl for i in items) for lvl in LEVELS}
    assert levels == LEVELS, (number, levels)
    scenarios = sum(i[1] == S for i in items)
    assert scenarios >= min_scenario * len(items), (number, scenarios)
    for topic, kind, level, text, options, why in items:
        assert kind in (S, D) and topic and why.strip(), text
        assert len(options) == 4 and len(set(options)) == 4, text
    longest, shortest, worst = length_report(items)
    # The correct option may be the longest no more often than chance (1 in 4), and never by more than 4 characters
    # (except where the options are fixed names, see NAMED_OPTIONS).
    assert longest <= len(items) // 4 and worst <= 4, (number, longest, worst)
    return scenarios, longest, shortest


def build(number, name, items, rng):
    questions = []
    for n, ((topic, kind, level, text, (correct, *wrong), why), letter) in \
            enumerate(zip(items, placed(rng, len(items))), 1):
        slots = list(wrong)
        rng.shuffle(slots)
        slots.insert(LETTERS.index(letter), correct)
        questions.append({"id": f"T{number}-Q{n:02d}", "type": kind, "level": level, "topic": topic,
                          "text": text, "options": dict(zip(LETTERS, slots)), "answer": letter,
                          "explanation": why, "source": "generated", "flag": None})
    return {"id": f"T{number}", "section": "technical", "test": number,
            "title": f"Technical (Risk Assurance) – Test {number}: {name}",
            "timeLimitSec": TIME_LIMIT_SEC, "source": "generated", "questions": questions}


def main():
    rng = random.Random(2027)
    texts = set()
    for n in (1, 2, 3):  # no repeats of the hand-written tests
        old = json.loads((DATA / f"technical-{n}.json").read_text(encoding="utf-8"))
        texts |= {q["text"] for q in old["questions"]}
    for number, (name, items, min_scenario) in TESTS.items():
        scenarios, longest, shortest = check(number, items, min_scenario)
        for item in items:
            assert item[3] not in texts, f"T{number}: repeated question: {item[3]}"
            texts.add(item[3])
        test = build(number, name, items, rng)
        counts = {letter: sum(q["answer"] == letter for q in test["questions"]) for letter in LETTERS}
        path = DATA / f"technical-{number}.json"
        path.write_text(json.dumps(test, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{path.name}: {len(items)} questions, {scenarios} scenario, answers {counts}, "
              f"correct longest {longest}x / shortest {shortest}x")


if __name__ == "__main__":
    main()
