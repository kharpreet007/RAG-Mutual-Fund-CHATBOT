# Problem Statement: Mutual Fund FAQ Assistant (Facts-Only Q&A)

## Overview

The objective of this project is to build a **facts-only FAQ assistant** for mutual fund schemes, using **Groww** as the reference product context. The assistant will answer objective, verifiable queries related to mutual funds by retrieving information exclusively from official public sources, such as **AMC (Asset Management Company)** websites, **AMFI**, and **SEBI**.

The system must **strictly avoid** providing investment advice, opinions, or recommendations. Every response must include a single, clear source link and adhere to defined constraints around clarity, accuracy, and compliance.

---

## Objective

Design and implement a lightweight **Retrieval-Augmented Generation (RAG)**-based assistant that:

- Answers factual queries about mutual fund schemes
- Uses a curated corpus of official documents
- Provides concise, source-backed responses

---

## Target Users

| User Segment | Use Case |
|---|---|
| **Retail investors** | Comparing mutual fund schemes using verified facts |
| **Customer support & content teams** | Handling repetitive mutual fund queries efficiently |

---

## Scope of Work

### 1. Corpus Definition

- Select **one Asset Management Company (AMC)**
- Collect **15–25 official public URLs**, including:
  - Scheme factsheets
  - KIM (Key Information Memorandum)
  - SID (Scheme Information Document)
  - AMC FAQ / help pages
  - AMFI / SEBI guidance pages
  - Statement and tax document download guides

### 2. FAQ Assistant Requirements

The assistant must answer **facts-only queries**, such as:

| Query Type | Example |
|---|---|
| Expense ratio | _"What is the expense ratio of XYZ fund?"_ |
| Exit load details | _"What is the exit load for ABC scheme?"_ |
| Minimum SIP amount | _"What is the minimum SIP amount?"_ |
| ELSS lock-in period | _"What is the lock-in period for ELSS funds?"_ |
| Riskometer classification | _"What is the risk level of this fund?"_ |
| Benchmark index | _"What benchmark does this scheme track?"_ |
| Statement / capital gains downloads | _"How do I download my capital gains report?"_ |

**Response constraints:**

- Each response is limited to a **maximum of 3 sentences**
- Each response includes **exactly one citation link**
- Each response includes a footer:
  > _"Last updated from sources: \<date\>"_

### 3. Refusal Handling

The assistant must **refuse non-factual or advisory queries**, such as:

- _"Should I invest in this fund?"_
- _"Which fund is better?"_

**Refusal responses should:**

- Be polite and clearly worded
- Reinforce the facts-only limitation
- Provide a relevant educational link (e.g., AMFI or SEBI resource)

### 4. User Interface (Minimal)

The solution should include a simple interface with:

- A **welcome message**
- **Three example questions**
- A visible **disclaimer**:
  > _"Facts-only. No investment advice."_

---

## Constraints

### Data and Sources

- Use **only official public sources** (AMC, AMFI, SEBI)
- Do **not** use third-party blogs or aggregator websites

### Privacy and Security

Do not collect, store, or process:

- PAN or Aadhaar numbers
- Account numbers
- OTPs
- Email addresses or phone numbers

### Content Restrictions

- No investment advice or recommendations
- No performance comparisons or return calculations
- For performance-related queries, provide a **link to the official factsheet only**

### Transparency

- Responses must be **short, factual, and verifiable**
- Every answer must include a **source link** and **last updated date**

---

## Expected Deliverables

### README Document

- Setup instructions
- Selected AMC and schemes
- Architecture overview (RAG approach)
- Known limitations

### Disclaimer Snippet

> _"Facts-only. No investment advice."_

---

## Success Criteria

| # | Criterion |
|---|---|
| 1 | Accurate retrieval of factual mutual fund information |
| 2 | Strict adherence to facts-only responses |
| 3 | Consistent inclusion of valid source citations |
| 4 | Proper refusal of advisory queries |
| 5 | Clean, minimal, and user-friendly interface |

---

## Summary

The goal is to build a **trustworthy, transparent, and compliant** mutual fund FAQ assistant that prioritizes **accuracy over intelligence**. The system should ensure that users receive only verified, source-backed financial information, without any advisory bias or speculative content.
