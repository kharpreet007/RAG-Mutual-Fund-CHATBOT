# Edge Cases — Mutual Fund FAQ Assistant

> **Project:** Facts-Only Mutual Fund FAQ Assistant  
> **Derived From:** [Architecture](file:///Users/harpreetkaur/Desktop/Milestone-MF/docs/architecture.md) · [Implementation Plan](file:///Users/harpreetkaur/Desktop/Milestone-MF/docs/implementation-plan.md)  
> **Last Updated:** June 2026

---

## Table of Contents

1. [Query Input Edge Cases](#1-query-input-edge-cases)
2. [Query Classification Edge Cases](#2-query-classification-edge-cases)
3. [PII & Security Edge Cases](#3-pii--security-edge-cases)
4. [Retrieval & RAG Edge Cases](#4-retrieval--rag-edge-cases)
5. [Response Generation Edge Cases](#5-response-generation-edge-cases)
6. [Data Ingestion Edge Cases](#6-data-ingestion-edge-cases)
7. [API & Backend Edge Cases](#7-api--backend-edge-cases)
8. [User Interface Edge Cases](#8-user-interface-edge-cases)
9. [Compliance & Content Edge Cases](#9-compliance--content-edge-cases)
10. [Edge Case Test Matrix](#10-edge-case-test-matrix)

---

## 1. Query Input Edge Cases

Edge cases related to the raw text input received from the user.

| # | Edge Case | Example Input | Expected Behavior | Severity |
|---|---|---|---|---|
| 1.1 | **Empty query** | `""` or `"   "` | Return error: _"Please enter a valid question."_ | 🟡 Medium |
| 1.2 | **Single character** | `"a"` | Process normally; will likely return "I don't have this information" | 🟢 Low |
| 1.3 | **Very long query** (>1000 chars) | A paragraph-length question | Truncate to 500 characters before processing; inform user | 🟡 Medium |
| 1.4 | **Special characters only** | `"@#$%^&*()"` | Return: _"Please enter a valid question."_ | 🟢 Low |
| 1.5 | **HTML/script injection** | `"<script>alert('xss')</script>"` | Sanitize input; strip HTML tags before processing | 🔴 High |
| 1.6 | **SQL injection attempt** | `"'; DROP TABLE funds; --"` | Treat as plain text; no SQL database is used (ChromaDB is vector-based) | 🟡 Medium |
| 1.7 | **Unicode / emoji input** | `"What is the expense ratio 🤔?"` | Strip emojis; process the text content normally | 🟢 Low |
| 1.8 | **Query in non-English language** | `"HDFC मिड कैप फंड का एक्सपेंस रेश्यो क्या है?"` | Attempt to process; may return "I don't have this information" as corpus is in English | 🟡 Medium |
| 1.9 | **Multiple questions in one query** | `"What is the expense ratio and exit load of HDFC Mid-Cap?"` | Answer the first identifiable question; retrieval may cover both if context is available | 🟡 Medium |
| 1.10 | **Query with excessive whitespace** | `"  What   is   the   expense   ratio  ?"` | Normalize whitespace before processing | 🟢 Low |
| 1.11 | **Repeated identical queries** | Same query submitted 50 times rapidly | Rate limit: max 10 requests/minute; return 429 after threshold | 🟡 Medium |
| 1.12 | **Query with only numbers** | `"12345"` | Process normally; will return "I don't have this information" | 🟢 Low |

---

## 2. Query Classification Edge Cases

Edge cases where the query classifier may misclassify user intent.

### 2.1 Ambiguous Queries (Factual vs. Advisory)

| # | Edge Case | Query | Correct Classification | Risk |
|---|---|---|---|---|
| 2.1.1 | **Implicit advice-seeking** | "Is HDFC Mid-Cap Fund safe?" | ADVISORY — "safe" implies opinion | May be classified as FACTUAL if "safe" is not in keyword list |
| 2.1.2 | **Comparative phrasing without "compare"** | "How does HDFC Mid-Cap differ from Small Cap?" | ADVISORY — implies comparison | May slip through if "differ" is not in keyword list |
| 2.1.3 | **Future-oriented factual** | "When is the next dividend date for HDFC Equity Fund?" | FACTUAL — asking about a scheduled event | May be flagged as ADVISORY due to "next" / future phrasing |
| 2.1.4 | **Negated advisory** | "I'm not asking for advice, just tell me the expense ratio" | FACTUAL | Keyword "advice" may trigger false ADVISORY classification |
| 2.1.5 | **Return-related factual** | "What is the CAGR of HDFC Small Cap Fund?" | FACTUAL — but should redirect to factsheet | May generate an answer instead of redirecting |
| 2.1.6 | **Process-related query** | "How do I start a SIP in HDFC Nifty 50?" | FACTUAL — operational process question | May be misclassified as ADVISORY |
| 2.1.7 | **Conditional phrasing** | "If I invest 5000 monthly, what happens?" | ADVISORY — hypothetical investment scenario | May partially match factual patterns |
| 2.1.8 | **Keyword in scheme name** | "Tell me about HDFC Balanced Advantage Fund" | FACTUAL | "Advantage" might trigger advisory keyword matching if poorly configured |

### 2.2 Mitigation Strategies

| Strategy | Description |
|---|---|
| **Whole-phrase matching** | Match full phrases like "should I invest" rather than individual words like "invest" |
| **Context-aware classification** | Check if advisory keywords appear as part of a scheme name vs. as query intent |
| **Confidence scoring** | If classification confidence is low, default to FACTUAL and rely on prompt guardrails |
| **LLM fallback classifier** | For ambiguous cases, use a lightweight LLM call to determine intent |

---

## 3. PII & Security Edge Cases

Edge cases related to detecting and handling personally identifiable information.

| # | Edge Case | Example Input | Detection Challenge | Expected Behavior |
|---|---|---|---|---|
| 3.1 | **PAN in natural sentence** | "My PAN ABCDE1234F shows wrong name" | PAN embedded in conversational text | Detect PAN regex → refuse |
| 3.2 | **Partial PAN** | "My PAN starts with ABCDE" | Doesn't match full PAN pattern | Allow — incomplete PAN is not sensitive |
| 3.3 | **Aadhaar with dashes** | "My Aadhaar is 1234-5678-9012" | Dashes instead of spaces | Regex should handle optional separators |
| 3.4 | **Phone number in text** | "Call me on 9876543210 for details" | Phone embedded in sentence | Detect phone regex → refuse |
| 3.5 | **Phone with country code** | "+91-9876543210" | Dash separator with country code | Regex should handle `+91` prefix with optional separators |
| 3.6 | **Email in query** | "Send statement to user@email.com" | Email embedded in request | Detect email regex → refuse |
| 3.7 | **Numeric scheme code resembling Aadhaar** | "What about scheme 123456789012?" | 12-digit number that isn't Aadhaar | May trigger false positive — add context check |
| 3.8 | **Account number in query** | "My folio number is 1234567890123" | Long numeric string | Detect → refuse (err on the side of caution) |
| 3.9 | **OTP in query** | "My OTP is 456789" | 6-digit number | May not be detected by current patterns — add OTP regex |
| 3.10 | **PII in mixed-language text** | "Mera PAN ABCDE1234F hai" | PII in Hindi-English mix | Regex is language-agnostic; should still detect |
| 3.11 | **False positive: fund NAV** | "NAV is 45.6789" | Decimal number, not PII | Should NOT trigger PII detection |
| 3.12 | **False positive: AUM value** | "AUM is 12345 crore" | Large number, not PII | Should NOT trigger account number detection |
| 3.13 | **Encoded PII** | "PAN: A-B-C-D-E-1-2-3-4-F" | Characters separated by dashes | May evade regex — normalize input before detection |

### PII False Positive Mitigation

| Issue | Mitigation |
|---|---|
| NAV/AUM numbers triggering account detection | Require account numbers to be ≥9 digits AND not preceded by currency/financial terms |
| Scheme codes triggering Aadhaar detection | Check if 12-digit number appears in context with "scheme", "folio", or fund-related terms |
| Short OTPs | Add specific 4-6 digit OTP pattern, but only trigger if preceded by "OTP", "code", or "verification" |

---

## 4. Retrieval & RAG Edge Cases

Edge cases in the vector search and context retrieval pipeline.

| # | Edge Case | Scenario | Expected Behavior | Severity |
|---|---|---|---|---|
| 4.1 | **No relevant chunks found** | Query about a non-HDFC fund or unrelated topic | Return: _"I don't have this information in my sources."_ | 🟡 Medium |
| 4.2 | **All chunks below similarity threshold** | Vague query: "Tell me something about funds" | Return: _"I don't have this information in my sources."_ | 🟡 Medium |
| 4.3 | **Wrong scheme retrieved** | "Expense ratio of HDFC Small Cap" retrieves HDFC Mid-Cap chunks | Re-ranker should boost scheme-name match; if still wrong, answer will be inaccurate | 🔴 High |
| 4.4 | **Ambiguous scheme name** | "HDFC Index Fund" — matches both Nifty 50 and Sensex Index funds | Return top match; or ask for clarification if scores are very close | 🟡 Medium |
| 4.5 | **Misspelled scheme name** | "HDFC Midcap Fund" (no hyphen) or "HDFC Smol Cap" | Embedding similarity should handle minor typos; major misspellings may fail | 🟡 Medium |
| 4.6 | **Abbreviation usage** | "BAF" for Balanced Advantage Fund, "ETF" for Exchange Traded Fund | May not match if abbreviation isn't in the corpus text | 🟡 Medium |
| 4.7 | **Cross-scheme query** | "Do HDFC Mid-Cap and Small Cap have the same exit load?" | Retriever may return chunks from only one scheme | 🟡 Medium |
| 4.8 | **Generic category query** | "What are the debt funds available?" | Should retrieve chunks from debt-category schemes | 🟡 Medium |
| 4.9 | **ChromaDB collection empty** | Ingestion pipeline failed or not run | API should check collection size; return service error if empty | 🔴 High |
| 4.10 | **Stale data in vector store** | Data scraped weeks ago; fund details have changed | Include `Last updated from sources: <date>` so user is aware of data freshness | 🟡 Medium |
| 4.11 | **Duplicate chunks in retrieval** | Same content retrieved multiple times from overlapping chunks | Deduplicate by content hash before passing to LLM | 🟢 Low |
| 4.12 | **Chunk too small for context** | Important fact split across two chunks, only one retrieved | Chunk overlap (50 tokens) should mitigate; increase overlap if issue persists | 🟡 Medium |

---

## 5. Response Generation Edge Cases

Edge cases in the LLM's response output.

| # | Edge Case | Scenario | Expected Behavior | Severity |
|---|---|---|---|---|
| 5.1 | **LLM exceeds 3-sentence limit** | Complex query leads to verbose response | Post-validation truncates or regenerates; log the violation | 🟡 Medium |
| 5.2 | **LLM provides investment advice despite prompt** | "This fund has good potential" in response | Post-validation detects advisory language; response is blocked and regenerated | 🔴 High |
| 5.3 | **LLM hallucination** | LLM invents a fact not in the context (e.g., wrong expense ratio) | Cannot be fully prevented; low temperature (0.1) and strict grounding reduce risk | 🔴 High |
| 5.4 | **LLM returns empty response** | Model fails to generate any text | Fallback: _"I couldn't generate an answer. Please try rephrasing your question."_ | 🟡 Medium |
| 5.5 | **LLM omits citation** | Response generated without source URL | Post-validation appends citation from chunk metadata | 🟡 Medium |
| 5.6 | **LLM omits last-updated footer** | Response missing the date footer | Post-validation appends footer using scrape date from metadata | 🟡 Medium |
| 5.7 | **LLM generates disclaimer in answer body** | "Disclaimer: I am not a financial advisor..." mixed into the answer | Remove LLM-generated disclaimers; use only the system-level disclaimer | 🟢 Low |
| 5.8 | **LLM responds in wrong language** | Answer generated in Hindi when query is in Hindi | Prompt specifies English-only responses; add explicit language instruction | 🟡 Medium |
| 5.9 | **LLM contradicts context** | Context says 0.75% expense ratio; LLM says 1.2% | Cannot be fully prevented; log and flag for review | 🔴 High |
| 5.10 | **Multiple citation URLs in response** | LLM provides 2+ links | Post-validation keeps only the first (or most relevant) citation | 🟡 Medium |
| 5.11 | **Groq API returns content moderation block** | Query triggers Groq's built-in content filters | Catch the moderation exception; return a generic error message | 🟡 Medium |
| 5.12 | **Response contains markdown formatting** | LLM outputs `**bold**` or `# headers` | Strip markdown from API response; render plain text or allow controlled markdown in Next.js UI | 🟢 Low |
| 5.13 | **Groq rate limit hit during generation** | Too many requests to Groq API in short window | Implement retry with exponential backoff; return user-friendly error after retries exhausted | 🟡 Medium |
| 5.14 | **LLaMA 3 ignores system prompt constraints** | LLM answers despite being told to refuse advisory queries | Post-validation catches advisory language; regenerate or block response | 🔴 High |

---

## 6. Data Ingestion Edge Cases

Edge cases during scraping, cleaning, chunking, and embedding.

| # | Edge Case | Scenario | Expected Behavior | Severity |
|---|---|---|---|---|
| 6.1 | **Groww page returns 403/404** | URL blocked or page removed | Log the failure; skip the URL; continue with remaining schemes | 🟡 Medium |
| 6.2 | **Groww page structure changed** | HTML selectors no longer match | Scraper returns empty/partial data; log warning; flag for manual review | 🔴 High |
| 6.3 | **JavaScript-rendered content** | Key data loaded via JS (not in initial HTML) | `requests` + `BeautifulSoup` cannot parse JS; may need `Selenium` or API fallback | 🔴 High |
| 6.4 | **Rate limiting by Groww** | Too many requests in short time → 429 error | Add 1–2 second delay between requests; retry with exponential backoff | 🟡 Medium |
| 6.5 | **Captcha / bot protection** | Groww serves a captcha page instead of content | Log failure; manual intervention required; consider using cached data | 🔴 High |
| 6.6 | **Encoding issues** | Page contains non-UTF-8 characters (e.g., ₹ symbol) | Ensure UTF-8 encoding; replace or handle special characters gracefully | 🟡 Medium |
| 6.7 | **Missing data fields** | A scheme page lacks expense ratio or exit load info | Store partial data; mark missing fields as `null` in metadata | 🟡 Medium |
| 6.8 | **Duplicate content across pages** | Common AMC-level info repeated on every scheme page | Deduplicate at chunk level using content hashing | 🟢 Low |
| 6.9 | **Very large page content** | A scheme page has unusually long content (>50KB text) | Chunker handles this naturally; just generates more chunks | 🟢 Low |
| 6.10 | **Empty page after cleaning** | All content stripped during cleaning | Skip the page; log warning; do not create empty chunks | 🟡 Medium |
| 6.11 | **BGE-small model download failure** | First-run download of `BAAI/bge-small-en-v1.5` (~130 MB) fails due to network issues | Retry download; allow manual model placement in cache directory | 🟡 Medium |
| 6.12 | **ChromaDB write failure** | Disk full or permission error | Catch exception; log error; alert user to check disk space | 🔴 High |
| 6.13 | **BGE-small OOM on large batch** | Embedding a very large number of chunks at once exhausts RAM | Process embeddings in batches of 50–100 chunks; BGE-small is lightweight (~130 MB) but batch size matters | 🟡 Medium |

---

## 7. API & Backend Edge Cases

Edge cases in the FastAPI application layer.

| # | Edge Case | Scenario | Expected Behavior | Severity |
|---|---|---|---|---|
| 7.1 | **Malformed JSON in request body** | `POST /ask` with invalid JSON | Return 422 Unprocessable Entity (FastAPI's default Pydantic validation) | 🟡 Medium |
| 7.2 | **Missing `query` field** | `POST /ask` with `{}` | Return 422 with field-level validation error | 🟡 Medium |
| 7.3 | **Request body too large** | Multi-MB payload sent to `/ask` | Limit request body size (e.g., 10KB max); return 413 | 🟡 Medium |
| 7.4 | **Concurrent requests overload** | 100+ simultaneous queries | Uvicorn's async handling + connection limits; add request queue or rate limiter | 🟡 Medium |
| 7.5 | **CORS preflight failure** | Next.js frontend on `localhost:3000`, FastAPI on `localhost:8000` | Ensure CORS middleware allows `localhost:3000`; configure proxy in `next.config.js` | 🟡 Medium |
| 7.6 | **API key not configured** | `.env` missing `GROQ_API_KEY` | App startup should fail gracefully with clear error message | 🔴 High |
| 7.7 | **ChromaDB not initialized** | Ingestion not run before starting API | Check for ChromaDB collection on startup; return 503 if missing | 🔴 High |
| 7.8 | **Groq API timeout** | LLM takes >30 seconds to respond | Set timeout (e.g., 15s); return error: _"Response took too long. Please try again."_ | 🟡 Medium |
| 7.9 | **Groq API quota exhausted** | Free tier limit reached | Catch quota error; return 503 with user-friendly message | 🔴 High |
| 7.10 | **Unexpected exception in pipeline** | Unhandled error in retriever/generator | Global exception handler returns 500 with generic error message; log full trace | 🔴 High |
| 7.11 | **Next.js build failure** | Frontend fails to compile | Check for syntax errors, missing dependencies; ensure `npm run build` passes | 🟡 Medium |
| 7.12 | **Request with unsupported HTTP method** | `PUT /ask` or `DELETE /ask` | Return 405 Method Not Allowed | 🟢 Low |
| 7.13 | **Next.js ↔ FastAPI proxy misconfiguration** | API requests from frontend 404 or timeout | Verify `next.config.js` rewrites point to correct backend URL | 🟡 Medium |
| 7.14 | **BGE-small model not loaded at API start** | First request triggers model download, causing timeout | Pre-load model during FastAPI startup event; add health check for model readiness | 🟡 Medium |

---

## 8. User Interface Edge Cases

Edge cases in the Next.js frontend chat interface.

| # | Edge Case | Scenario | Expected Behavior | Severity |
|---|---|---|---|---|
| 8.1 | **Rapid submit clicks** | User clicks Send 10 times quickly | Debounce: disable button after first click; re-enable after response | 🟡 Medium |
| 8.2 | **Enter key + click simultaneously** | Both events fire for the same query | Prevent duplicate submissions via flag | 🟢 Low |
| 8.3 | **Very long bot response** | Response text overflows message bubble | CSS: `word-wrap: break-word`; scrollable message area | 🟡 Medium |
| 8.4 | **Network timeout** | API doesn't respond within 15 seconds | Show timeout error message; re-enable input | 🟡 Medium |
| 8.5 | **Network disconnected** | User is offline when sending query | Catch `fetch` error; display: _"Network error. Please check your connection."_ | 🟡 Medium |
| 8.6 | **Browser back/forward** | User navigates away and back | Chat history is lost (state in React, no persistence); show welcome message again | 🟢 Low |
| 8.7 | **Mobile viewport** | Screen width < 400px | Responsive design: stack elements vertically; adjust font sizes; test with Next.js responsive utilities | 🟡 Medium |
| 8.8 | **Copy-paste long text** | User pastes a full document into the input | Limit input field to 500 characters with counter | 🟡 Medium |
| 8.9 | **Special characters in response** | Response contains `<`, `>`, `&` | Escape HTML entities before rendering to prevent XSS | 🔴 High |
| 8.10 | **Citation link broken** | Source URL returns 404 when user clicks | Cannot control external URLs; add note: _"Link opens the source page on Groww"_ | 🟢 Low |
| 8.11 | **Screen reader accessibility** | Visually impaired user using screen reader | Add `aria-label`, `role` attributes to chat elements | 🟡 Medium |
| 8.12 | **Keyboard-only navigation** | User navigates via Tab/Enter only | Ensure all interactive elements are focusable and operable | 🟡 Medium |
| 8.13 | **Browser auto-translate** | Chrome auto-translates the UI to another language | Disclaimer and footer may be mistranslated; add `translate="no"` to critical elements | 🟢 Low |
| 8.14 | **Next.js hydration mismatch** | Server-rendered HTML doesn't match client-rendered output | Ensure chat state is initialized client-side only (`"use client"` directive); avoid SSR for dynamic chat state | 🟡 Medium |
| 8.15 | **Next.js hot reload breaks state** | During development, HMR resets chat messages | Expected dev behavior; not a production concern; use React state persistence if needed | 🟢 Low |

---

## 9. Compliance & Content Edge Cases

Edge cases related to regulatory compliance and content restrictions.

| # | Edge Case | Scenario | Expected Behavior | Severity |
|---|---|---|---|---|
| 9.1 | **Performance-related factual query** | "What was the 1-year return of HDFC Mid-Cap?" | Redirect to factsheet: _"For performance data, visit the official factsheet: [link]"_ | 🟡 Medium |
| 9.2 | **Return calculation request** | "If I invest 10,000 monthly, how much will I get?" | Refuse: this is a projection/advisory request | 🔴 High |
| 9.3 | **Tax-related query** | "Is HDFC ELSS eligible for 80C deduction?" | Answer factually if info is in corpus; do NOT provide tax advice | 🟡 Medium |
| 9.4 | **Regulatory query** | "Is HDFC AMC SEBI registered?" | Answer factually if in corpus; otherwise redirect to SEBI website | 🟡 Medium |
| 9.5 | **Scheme closure query** | "Is HDFC Defence Fund closed for subscription?" | Answer factually if in corpus; include last-updated date for freshness context | 🟡 Medium |
| 9.6 | **NFO (New Fund Offer) query** | "Is there any new HDFC fund launching?" | Out of scope: _"I don't have this information in my sources."_ | 🟢 Low |
| 9.7 | **Complaint/grievance** | "I want to file a complaint about HDFC AMC" | Not in scope; redirect to HDFC AMC or SEBI SCORES portal | 🟡 Medium |
| 9.8 | **Transactional request** | "Buy 100 units of HDFC Mid-Cap Fund" | Refuse: _"I cannot process transactions. Visit Groww or your broker."_ | 🔴 High |
| 9.9 | **Portfolio-level query** | "What percentage of my portfolio is in HDFC funds?" | Refuse: requires user-specific data that is not collected or stored | 🔴 High |
| 9.10 | **Third-party comparison** | "Is HDFC Mid-Cap better than SBI Mid-Cap?" | Refuse: ADVISORY + cross-AMC comparison is out of scope | 🔴 High |
| 9.11 | **Outdated information served** | Expense ratio changed after last scrape | Last-updated footer alerts users; recommend periodic re-ingestion | 🟡 Medium |
| 9.12 | **Disclaimer missing from response** | Bug causes disclaimer to not render | Post-validation always appends disclaimer; UI renders it as a fixed element | 🔴 High |

---

## 10. Edge Case Test Matrix

A consolidated test matrix for integration testing. All edge cases should be tested before deployment.

### Priority Legend

| Priority | Label | Description |
|---|---|---|
| 🔴 | **P0 — Critical** | Must be handled; failure causes security/compliance risk |
| 🟡 | **P1 — Important** | Should be handled; failure causes poor user experience |
| 🟢 | **P2 — Nice-to-have** | Good to handle; failure is cosmetic or minor |

### Summary by Category

| Category | Total | 🔴 Critical | 🟡 Important | 🟢 Low |
|---|---|---|---|---|
| Query Input | 12 | 1 | 5 | 6 |
| Query Classification | 8 | 0 | 8 | 0 |
| PII & Security | 13 | 0 | 9 | 4 |
| Retrieval & RAG | 12 | 2 | 8 | 2 |
| Response Generation | 14 | 4 | 7 | 3 |
| Data Ingestion | 13 | 3 | 8 | 2 |
| API & Backend | 14 | 4 | 9 | 1 |
| User Interface | 15 | 1 | 9 | 5 |
| Compliance & Content | 12 | 4 | 6 | 2 |
| **Total** | **113** | **19** | **69** | **25** |

### Top 19 Critical (P0) Edge Cases

| # | Category | Edge Case | Test Query / Scenario |
|---|---|---|---|
| 1 | Input | XSS injection | `<script>alert('xss')</script>` |
| 2 | Retrieval | Wrong scheme retrieved | "Expense ratio of HDFC Small Cap" → verify correct scheme in response |
| 3 | Retrieval | ChromaDB empty | Start API without running ingestion |
| 4 | Response | LLM provides investment advice | Check all responses for advisory keywords |
| 5 | Response | LLM hallucination | Cross-verify generated facts against scraped data |
| 6 | Response | LLM contradicts context | Compare response with retrieved chunks |
| 7 | Ingestion | Page structure changed | Modify HTML fixture; verify scraper handles gracefully |
| 8 | Ingestion | JS-rendered content | Verify data presence in raw HTML vs. rendered page |
| 9 | Ingestion | ChromaDB write failure | Simulate disk full scenario |
| 10 | API | API key not configured | Start app without `.env` (missing `GROQ_API_KEY`) |
| 11 | API | ChromaDB not initialized | Start app without running ingestion |
| 12 | API | Groq quota exhausted | Simulate API quota error |
| 13 | API | Unhandled exception | Inject fault in retriever pipeline |
| 14 | UI | Special chars in response | Ensure HTML entities are escaped in Next.js components |
| 15 | Compliance | Return calculation request | "If I invest 10,000 monthly, how much will I get?" |
| 16 | Compliance | Transactional request | "Buy 100 units of HDFC Mid-Cap Fund" |
| 17 | Compliance | Portfolio query | "What percentage of my portfolio is in HDFC funds?" |
| 18 | Compliance | Disclaimer missing | Verify disclaimer in every response |
| 19 | Response | LLaMA 3 ignores system prompt | Verify post-validation catches advisory content from LLM |

---

### Automation Strategy

| Layer | Approach | Tool |
|---|---|---|
| **Unit tests** | Test PII patterns, classifier keywords, response validation | `pytest` |
| **API tests** | Test all endpoints with edge case inputs | `pytest` + `httpx` (async) |
| **Integration tests** | Test full pipeline: query → classify → retrieve → generate | `pytest` |
| **UI tests** | Test React components, rendering, error states | `Jest` + `React Testing Library` / Manual |
| **Compliance audit** | Review a sample of 50 responses for advisory language | Manual review |

---

> **Document Version:** 1.0  
> **Status:** Draft — Pending Review  
> **References:**  
> - [Architecture](file:///Users/harpreetkaur/Desktop/Milestone-MF/docs/architecture.md)  
> - [Implementation Plan](file:///Users/harpreetkaur/Desktop/Milestone-MF/docs/implementation-plan.md)  
> - [Problem Statement](file:///Users/harpreetkaur/Desktop/Milestone-MF/docs/problemStatement.md)
