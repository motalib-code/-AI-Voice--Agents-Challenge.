# Pull Request Summary - Day 5: Simple FAQ SDR + Lead Capture

## PR Details

**Branch:** `day5`
**Base Branch:** `main`
**Repository:** (Your Repository URL)

## Quick Links

**Create Pull Request:**
👉 (Go to your GitHub repository and switch to branch `day5` to create PR)

## Changes Summary

### Files Modified/Added: 3 Total

#### ✨ New Files (2)
1. **backend/src/day5_agent.py**
   - SDR Agent implementation (Razorpay persona)
   - Lead qualification logic
   - FAQ answering capability
   - Lead data capture and saving

2. **backend/shared-data/day5_sdr_content.json**
   - Company info, Products, Pricing, FAQs for Razorpay

#### 📝 Modified Files (1)
1. **backend/README.md**
   - Added running instructions for Day 5 agent
   - Updated Challenge Progress

## Commit Message

```
Day 5: SDR & Lead Capture (Razorpay) implementation

Implemented Sales Development Representative (SDR) agent:
- Persona: Riya from Razorpay
- Features: Lead qualification, FAQ answering, Lead capture
- Content: Razorpay specific data (Pricing, Products)
- Output: Saves qualified leads to JSON files
```

## PR Description Template

Copy this for your PR description:

---

## Overview
Implemented a Sales Development Representative (SDR) agent for Day 5. The agent acts as "Riya" from Razorpay, qualifying leads and answering questions.

## Features ✅
- ✅ **Persona**: Professional SDR (Voice: Terra).
- ✅ **Lead Qualification**: Captures Name, Company, Role, Use Case, Team Size, Timeline, Email.
- ✅ **FAQ Answering**: Answers questions using `day5_sdr_content.json`.
- ✅ **Lead Capture**: Saves lead details to `backend/leads/`.
- ✅ **End-of-Call Summary**: Summarizes next steps.

## Files Changed
- `backend/src/day5_agent.py`: SDR Agent logic.
- `backend/shared-data/day5_sdr_content.json`: Razorpay content.
- `backend/README.md`: Updated instructions and progress.

## Verification
- Run: `uv run python src/day5_agent.py dev`
- Test: Act as a customer, ask about pricing, provide details, and check the saved lead file.

---
