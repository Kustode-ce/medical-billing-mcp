# Usage Examples

Real conversations showing the Medical Billing MCP in action.

---

## Example 1: Understanding a Denial Code

**Scenario:** Billing staff receives ERA with denial code CO-50.

### Conversation

**User:** I got a denial with code CO-50 on my claim. What does this mean?

**Claude:** Let me look that up for you.

*[Calls lookup_denial(code="CO-50")]*

CO-50 is a **Contractual Obligation** denial meaning the payer determined the service was **not medically necessary**.

**Important:** Since this is a CO (Contractual Obligation) group code, you cannot bill the patient for this amount.

**Resolution Steps:**

1. **Review your diagnosis codes** - Are you using the most specific ICD-10 code available? For example, use E11.65 (diabetes with hyperglycemia) instead of E11.9 (diabetes unspecified) if documented.

2. **Check coverage criteria** - Look up the LCD (Local Coverage Determination) for this procedure to see what diagnoses are covered.

3. **Add supporting diagnoses** - Include secondary diagnoses that support why the service was needed.

4. **Prepare an appeal** with:
   - Letter of medical necessity from the physician
   - Relevant clinical notes
   - Test results that support the need for the service

Would you like me to look up the specific documentation requirements for the procedure code that was denied?

---

## Example 2: Modifier Guidance

**Scenario:** Provider performed an E/M visit and a minor procedure on the same day.

### Conversation

**User:** I did a 99213 office visit and then a skin tag removal on the same patient same day. Do I need a modifier?

**Claude:** Yes, let me explain the correct modifier to use.

*[Calls lookup_modifier(modifier="25")]*

You should use **modifier 25** on the E/M code (99213-25).

**Modifier 25** indicates a "significant, separately identifiable E/M service" performed on the same day as a procedure.

**When to use it:**
- The E/M visit addressed issues beyond just the procedure
- You documented a separate chief complaint, history, and/or exam
- The E/M work was above and beyond the typical pre/post work for the procedure

**Documentation required:**
- Separate chief complaint (not just "here for skin tag removal")
- History and/or exam elements related to the separate issue
- Separate medical decision making

**⚠️ Warning:** Modifier 25 has a **HIGH audit risk**. It's one of the most frequently audited modifiers. Make sure your documentation clearly supports a separate E/M service.

**Your claim should look like:**
- Line 1: 99213-25 (Office visit with modifier)
- Line 2: 11200 (Skin tag removal)

---

## Example 3: Timely Filing

**Scenario:** Staff finds old claims that were never submitted.

### Conversation

**User:** I found claims from 6 months ago that never got submitted. Is it too late for Medicare? What about Blue Cross?

**Claude:** Let me check the timely filing limits.

*[Calls lookup_payer(payer="medicare")]*
*[Calls lookup_payer(payer="bcbs")]*

**Medicare:** You're fine! Medicare's timely filing limit is **365 days** from the date of service. Claims from 6 months ago can still be submitted.

**Blue Cross:** This varies by plan, but most BCBS plans have **90-180 day** limits. At 6 months (180 days), you're at risk:
- Check the specific plan - some allow 180 days
- If you're past the limit, you'll need to appeal with proof of why the claim was delayed

**Recommended action:**
1. Submit the Medicare claims immediately
2. For BCBS, check the specific plan's filing limit
3. If past the BCBS limit, gather documentation explaining the delay:
   - System issues
   - Pending medical records
   - Patient eligibility verification delays

Want me to look up any specific BCBS state plan?

---

## Example 4: Bundling Check

**Scenario:** Coder is unsure if two codes can be billed together.

### Conversation

**User:** Can I bill 45378 and 45380 on the same claim?

**Claude:** Let me check the bundling rules for those codes.

*[Calls lookup_bundling(codes=["45378", "45380"])]*

**No, these codes are bundled.**

- **45378** = Diagnostic colonoscopy
- **45380** = Colonoscopy with biopsy

When a biopsy is performed during a colonoscopy, the diagnostic colonoscopy (45378) is **included** in 45380. You should only bill **45380**.

**Why?** The work of performing the diagnostic scope is inherent to performing the biopsy. Billing both would be double-billing for the same work.

**What to bill:** Just 45380 (colonoscopy with biopsy)

**Note:** If biopsies were taken from multiple distinct sites requiring separate passes of the scope, you may be able to add additional units or use modifier 59, but this is rare and requires clear documentation.

---

## Example 5: Code Lookup with Documentation Requirements

**Scenario:** New coder needs to understand E/M documentation.

### Conversation

**User:** What documentation do I need for a 99214?

**Claude:** Let me look up the requirements for 99214.

*[Calls lookup_cpt(code="99214")]*

**99214** is an office visit for an established patient with **moderate complexity** medical decision making.

**Documentation Requirements (2 of 3):**

| Element | Requirement for Moderate |
|---------|-------------------------|
| **Problems** | 1+ chronic illness with severe exacerbation/progression, OR 2+ chronic stable illnesses |
| **Data** | Moderate - order and review tests, obtain external history, or discuss with external provider |
| **Risk** | Moderate - prescription drug management, minor surgery with risk factors |

**OR Time-Based:**
- **30-39 minutes** total time on date of encounter
- Document the time and what you did

**Must Document:**
- Chief complaint
- History of present illness
- Assessment (what's wrong)
- Plan (what you're doing about it)
- Either MDM elements OR time spent

**Common denial reasons for 99214:**
- Documentation supports 99213 (low complexity) instead
- Missing elements to support moderate MDM
- Time not documented if billing time-based

---

## Example 6: ICD-10 Code Search

**Scenario:** Finding the right diagnosis code.

### Conversation

**User:** What's the ICD-10 code for type 2 diabetes with kidney disease?

**Claude:** Let me search for that.

*[Calls lookup_icd10(search="diabetes kidney")]*

For **Type 2 diabetes with kidney disease**, use:

**E11.65x** - Type 2 diabetes mellitus with diabetic kidney disease

The 5th/6th digits specify the stage:
- E11.65 - Diabetic kidney disease (general)

You should also code the specific chronic kidney disease stage:
- N18.1 - CKD Stage 1
- N18.2 - CKD Stage 2
- N18.3 - CKD Stage 3
- N18.4 - CKD Stage 4
- N18.5 - CKD Stage 5
- N18.6 - End stage renal disease

**Best practice:** Use the most specific code documented. If the physician documents "diabetic nephropathy, CKD stage 3", code:
- E11.65 (diabetes with kidney disease)
- N18.3 (CKD stage 3)

**Tip:** More specific codes = better HCC capture = appropriate risk adjustment.

---

## Sample Output Format

All tool responses follow this structure:

```json
{
  "code": "99214",
  "description": "Office visit, established patient, moderate complexity",
  "category": "E/M",
  "time_range": "30-39 minutes",
  "documentation": {
    "requires": ["chief_complaint", "history", "assessment", "plan"],
    "mdm_level": "moderate"
  }
}
```

For errors:

```json
{
  "error": "Code X99999 not found"
}
```
