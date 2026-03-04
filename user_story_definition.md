# User Story Definition

A well-formed user story consists of **three elements**. These map directly to fields in the ServiceNow `rm_story` table.

---

## 1. Title — `short_description`

A single sentence that captures **who** wants **what** and **why**, in plain language.

**Format:**
> As a `[type of user]`, I want `[goal or action]` so that `[benefit or reason]`.

**Rules:**
- Maximum 80 characters
- Written from the perspective of the end user, not the system
- Specific enough to be actionable, concise enough to scan at a glance

**Good example:**
> As an employee, I want to submit IT and HR requests through a single form so that I no longer need to use multiple systems.

**Avoid:**
> The system should have a form. *(No user perspective, no benefit)*

---

## 2. Description — `description`

A short narrative (2–4 sentences) that provides **context** and **rationale** for the story.

This section answers:
- What problem does this solve?
- Who is affected and how often?
- Are there any constraints or important context to be aware of?

**Example:**
> Employees currently use two separate systems to submit IT requests and HR requests, which causes confusion and increases handling time. A unified service catalog with categorized request types will provide a single entry point for all requests. The form should support dynamic fields based on the selected category, mandatory fields, file attachments, and a free-text notes field.

---

## 3. Acceptance Criteria — `acceptance_criteria`

A list of **3–5 specific, testable conditions** that must all be true for the story to be considered done.

**Format:** Each criterion should be independently verifiable — a tester should be able to say "pass" or "fail" without ambiguity.

**Recommended style:** Use "Given / When / Then" or simple bullet statements.

**Example:**
- The catalog displays request categories (e.g. IT, HR, Facilities) on the landing page.
- Selecting a category shows only the fields relevant to that request type.
- Mandatory fields are clearly marked and prevent form submission if left empty.
- Employees can attach one or more files to any request.
- Submitted requests appear in the employee's "My Requests" overview within 60 seconds.

**Avoid vague criteria like:**
- *"The form works correctly"* — not testable
- *"It looks good"* — subjective

---

## ServiceNow field mapping

| Story element | ServiceNow field | Type |
|---|---|---|
| Title | `short_description` | String (max 255 chars) |
| Description | `description` | Long text |
| Acceptance criteria | `acceptance_criteria` | Long text (newline-separated) |
