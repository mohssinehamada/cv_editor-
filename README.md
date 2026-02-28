# Resume–Job Description Matcher & Tailoring Advisor (BYOK)

A web app that compares a resume with a job description, scores fit, and produces practical, non-fabricated, ATS-friendly improvement suggestions. Users bring their own LLM API key (BYOK); keys are never stored server-side.

## Goals
- Compare JD and resume for skills, responsibilities, keywords, seniority signals, and ATS structure.
- Produce actionable edits: what to add/remove/rewrite/reorder.
- Provide a prioritized top-10 change list plus section-level suggestions and bullet rewrites.
- Export revised resumes (optional: Markdown/DOCX/PDF).

## Non‑Goals
- No fake experience, companies, degrees, or metrics.
- No job application automation.
- No permanent storage of API keys.

## Tech Stack
- Frontend: Node.js + TypeScript
- Backend: FastAPI (Python)
- Parsing: `pypdf`, `python-docx`
- LLM providers: `openai`, `anthropic`, `google-generativeai`, `mistralai`
- Embeddings / ranking (Phase 2): `sentence-transformers`

## Core Requirements
- BYOK security: API keys are in-memory per session; no logging or persistence.
- Safety: suggestions must be grounded in provided resume evidence or phrased conditionally.
- Output: match score breakdown, top 10 changes, section rewrites, keyword coverage map.

## Repository Structure (current)
- `apps/`
- `services/`
- `Backend/` (agent instructions)
- `frontend/` (agent instructions)
- `infra/` (agent override instructions)
- `tests/`
- `Project.md` (full spec)

## Status
- Planning / scaffolding.

## Next Steps
- Implement backend API with FastAPI.
- Implement frontend UI in Node.js + TypeScript.
- Add parsers and provider adapters.

