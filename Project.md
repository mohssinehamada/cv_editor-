# Project: Resume–Job Description Matcher & Tailoring Advisor (BYO API Key)

## 1) Goal

Build a web app that:
1) Collects a **Job Description (JD)** and a **Resume** from a user  
2) **Compares** them for fit (skills, keywords, responsibilities, seniority signals, ATS structure)  
3) Produces **tailored, actionable edits**: what to **add / remove / rewrite / reorder** in the resume to improve interview chances  
4) Requires the user to provide **their own LLM API key** (Bring Your Own Key / BYOK) so the system does not incur model costs and does not store secrets.

The app should be useful for:
- ATS optimization (keyword coverage, formatting, section structure)
- Rewriting bullet points to reflect JD requirements
- Highlighting gaps and suggesting realistic additions (without inventing false experience)
- Producing an “ATS-friendly” revised resume (optional export)

---

## 2) Non-Goals (Explicit)

- We do **not** generate fake experience, fake companies, fake degrees, or unverifiable claims.
- We do **not** apply for jobs on the user’s behalf.
- We do **not** permanently store user-provided API keys.
- We do **not** provide legal/immigration advice.

---

## 3) Primary User Flow

1) User opens app
2) User selects an LLM provider (e.g., OpenAI, Anthropic, Google, Mistral, etc.)
3) User enters their **API key** (BYOK) + optional model choice
4) User uploads/pastes:
   - Job Description (text)
   - Resume (PDF/DOCX or text)
5) App runs analysis pipeline:
   - Parse + normalize resume
   - Extract structured signals from both documents
   - Compute match metrics + gaps
   - Generate recommendations + rewrites
6) App displays:
   - Match score breakdown (skills, responsibilities, keywords, seniority, ATS structure)
   - Prioritized change list
   - Suggested rewrites by section
   - Optional: Generated revised resume in ATS-friendly format
7) User can export:
   - JSON report
   - Markdown/Docx/PDF revised resume (optional)

---

## 4) Key Product Requirements

### 4.1 Output Must Be Practical
The system must provide:
- **Top 10 changes** (prioritized)
- **Section-level suggestions** (Summary, Skills, Experience, Projects, Education)
- **Bullet rewrites** (STAR/XYZ style options)
- **Keyword coverage map** (missing / weak / strong)
- **Warnings** when a suggestion would imply fabrication (“Only add if true”)

### 4.2 ATS-Friendly Guidance
- Encourage standard headings (Summary, Skills, Experience, Education, Projects)
- Avoid heavy tables/columns/graphics
- Keep consistent formatting, dates, titles
- Suggest role-relevant keywords naturally (not keyword stuffing)

### 4.3 BYOK Security<
- API keys never stored in DB
- Keep only in-memory for the session
- Optional: store encrypted in browser localStorage (user choice) — default OFF

---

## 5) System Architecture (High Level)

### 5.1 Components
- **Frontend**: Next.js/React UI
- **Backend API**: Node.js (Next API routes) or FastAPI (Python)
- **Document Parsing Layer**:
  - PDF text extraction
  - DOCX extraction
  - Plain text normalization
- **LLM Orchestrator**:
  - Provider-agnostic interface (OpenAI/Anthropic/etc.)
  - Prompt templates + structured JSON outputs
- **Scoring & Heuristics Engine** (non-LLM):
  - Keyword overlap metrics
  - Section completeness checks
  - ATS formatting heuristics
  - Seniority alignment hints
- **Report Generator**:
  - Human-readable UI sections
  - Exporters (JSON, Markdown, DOCX/PDF optional)
- Clean Architecture / Hexagonal:
  - `core/` domain (resume, job, scoring, recommendations)
  - `adapters/` (LLM providers, parsers, exporters)
  - `api/` (routes/controllers)
  - `ui/` (frontend)

---

## 6) Data Model (Conceptual)

### 6.1 Normalized Resume Schema (internal)
- `contact`: name, location, links (optional)
- `summary`: string
- `skills`: categorized list (languages, frameworks, tools, domains)
- `experience[]`:
  - company, title, start_date, end_date, location
  - bullets[]
- `projects[]`: name, description, tech, bullets[]
- `education[]`
- `certifications[]`
- `additional[]` (volunteering, publications, awards)

### 6.2 Normalized Job Description Schema (internal)
- `title`, `level` (junior/mid/senior inferred)
- `must_have_skills[]`
- `nice_to_have_skills[]`
- `responsibilities[]`
- `keywords[]`
- `domain_signals[]` (finance, healthcare, ads-tech, etc.)

---

## 7) Matching & Recommendation Logic

### 7.1 Heuristic Scoring (fast, deterministic)
- Skill overlap: Jaccard / weighted overlap
- Keyword coverage: TF-IDF-like weighting
- Responsibility alignment: cosine similarity on embeddings (optional)
- Seniority alignment signals:
  - leadership verbs, scope metrics, ownership phrases
- ATS checks:
  - missing sections
  - inconsistent dates
  - overly long bullets
  - too many buzzwords, low specificity

### 7.2 LLM-Assisted Extraction & Rewrite
Use the LLM for:
- Extracting structured fields from messy resume text
- Classifying JD requirements
- Proposing rewrite options and new bullets **only if consistent with provided resume content**
- Producing a final “tailored resume draft” (optional)

### 7.3 Safety Rule (No Fabrication)
All suggestions must be constrained:
- If user did not provide evidence of a skill/achievement, the system must phrase suggestions as:
  - “If you have experience with X, add it here”
  - “Consider adding a project demonstrating X”
- Never invent metrics or employers.

---

## 8) LLM Provider Integration (BYOK)

### 8.1 Provider Abstraction
Implement `LLMClient` interface:

- `generateText(prompt, options) -> text`
- `generateJSON(prompt, schema, options) -> json`
- `healthCheck()`

Adapters:
- `OpenAIClient`
- `AnthropicClient`
- `GeminiClient`
- `MistralClient`
(others can be added)

### 8.2 Key Handling Rules
- API key provided by user per session
- Stored:
  - Frontend state (memory) only, by default
  - Optionally localStorage (user toggle, clearly warned)
- Backend receives key in request header, uses it to call provider, never logs it.

---

## 9) API Design (Example)

### 9.1 Endpoints
- `POST /api/parse`
  - input: file or text
  - output: normalized text + basic structure (non-LLM)
- `POST /api/analyze`
  - input: `{ jobText, resumeText, provider, model }` + header `x-llm-api-key`
  - output: analysis JSON (scores, gaps, suggestions)
- `POST /api/rewrite`
  - input: `{ analysisId?, jobText, resumeStructured, targetRole }` + key header
  - output: revised resume (markdown + structured)
- `POST /api/export/docx` (optional)
  - input: revised resume structured
  - output: docx blob

### 9.2 Response JSON (Core)
- `scores`: overall, skills, keywords, responsibilities, seniority, ats
- `gaps`: missing skills, weak areas, missing sections
- `recommendations[]`:
  - `priority` (P0/P1/P2)
  - `action` (add/edit/remove/reorder)
  - `section`
  - `why`
  - `how`
  - `exampleRewrite` (optional)
  - `riskFlag` (fabrication risk boolean)
- `keywordMap`:
  - `presentStrong[]`, `presentWeak[]`, `missing[]`
- `rewrites`:
  - per-section suggested content

---

## 10) Prompting Strategy (Implementation Notes)

### 10.1 Use Structured Outputs
Prefer JSON output with a strict schema to reduce UI parsing issues.

### 10.2 Prompt Modules
- JD extraction prompt
- Resume extraction prompt
- Match analysis prompt (must cite evidence from resume text)
- Rewrite prompt (must not fabricate; only rewrite existing bullets unless user explicitly asks to add hypothetical items)

### 10.3 Evidence Requirement
When recommending a change, include:
- Which JD requirement it addresses
- Where in resume it is currently addressed (or missing)
- A suggested rewrite that preserves truthfulness

---

## 11) UI Requirements

### 11.1 Screens
1) **Input Screen**
   - Provider dropdown
   - API key input
   - JD text area
   - Resume upload (PDF/DOCX) + paste fallback
2) **Results Dashboard**
   - Overall match score + breakdown
   - “Top changes” list (editable checklist)
   - Keyword coverage panel
   - Section-by-section rewrite suggestions
3) **Editor (Optional)**
   - Side-by-side resume + suggested edits
   - Accept/reject suggestions
4) **Export**
   - Copy Markdown
   - Download DOCX/PDF (optional)

### 11.2 UX Considerations
- Clear warning: “Do not add skills you don’t have.”
- Fast feedback: heuristic results immediately, LLM results streaming if supported.

---

## 12) Observability & Quality

- Minimal logs; never log resume contents by default
- Provide “Download analysis JSON” for debugging
- Basic analytics optional (opt-in): which sections users view/accept

---

## 13) Testing Strategy

### 13.1 Unit Tests
- Parsers (PDF/DOCX)
- Scoring functions
- Keyword extraction normalization
- JSON schema validation

### 13.2 Integration Tests
- Provider adapters with mocked responses
- End-to-end: upload -> analyze -> rewrite -> export

### 13.3 Evaluation Dataset (Internal)
Create small set of sample resumes and JDs for:
- Data Scientist
- Backend Engineer
- DevOps/SRE
- Product Manager

Use consistent metrics:
- Keyword coverage improvement
- Readability checks (bullet length, specificity)
- Hallucination rate (should be near zero)

---

## 14) Tech Stack Recommendation

### Option A (Fastest Web Dev)
- Frontend: Next.js (App Router), React, Tailwind
- Backend: Next.js API routes
- Parsing: `pdf-parse` or `pdfjs`, `mammoth` for DOCX
- Validation: Zod
- Storage: none required; optional SQLite/Postgres for storing reports (without keys)

### Option B (Python-Friendly)
- Frontend: Next.js
- Backend: FastAPI
- Parsing: `pypdf`, `python-docx`
- Validation: Pydantic
- Storage: optional

---

## 15) Milestones

### Milestone 1: Core Analysis (MVP)
- Input UI (JD + resume + provider + key)
- Resume parsing
- Heuristic scoring + keyword map
- LLM-generated prioritized recommendations (JSON)
- Results dashboard

### Milestone 2: Rewrite Suggestions
- Section rewrites
- Bullet point rewrite generator
- Accept/reject suggestions UI

### Milestone 3: Export
- Export tailored resume (Markdown)
- Optional DOCX/PDF

### Milestone 4: Multi-Provider + Hardening
- Additional providers
- Better schema enforcement
- Improved safety checks
- Rate-limit and timeouts

---

## 16) Repository Structure (Suggested)

- `apps/web/`
  - `app/` routes
  - `components/`
  - `lib/`
- `services/core/`
  - `domain/` (schemas, scoring, normalization)
  - `adapters/` (LLM clients, parsers)
  - `prompts/`
- `services/api/` (if separate)
- `tests/`
- `project.md` (this file)

---

## 17) Acceptance Criteria

- User can paste JD + upload/paste resume and receive:
  - match score breakdown
  - top 10 prioritized changes
  - section-specific rewrite suggestions
  - keyword coverage map
- System does not store API keys and does not fabricate experience.
- Works with at least one provider end-to-end using BYOK.


