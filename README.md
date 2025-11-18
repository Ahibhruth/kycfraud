 KYC–AI Fraud detection and KYC Verification Dashboard

A full-stack KYC (Know Your Customer) and AML (Anti-Money Laundering) verification system built using FastAPI backend + React/Node frontend.
The application validates customer identity documents (Aadhaar, PAN, Passport), performs AML risk assessment, and generates structured reports with visual dashboards.

Features
1)KYC Verification

Aadhaar structural validation (regex + Verhoeff checksum)

PAN pattern validation

Passport pattern validation

OCR-based document extraction (if enabled)

Automatic field matching (Name, DOB, Address)

2)AML Risk Engine

Sanction list flag detection

High-risk country checks

PEP (Politically Exposed Person) flag

Risk scoring model

Red-flag behavior detection (multiple accounts, mismatch in documents)

3)Dashboard & UI

Clean React UI

Customer onboarding page

Risk score visualization

Status color coding: Green (Low), Yellow (Medium), Red (High)

Export reports as PDF

 4)Backend

FastAPI (Python)

Modular service-based architecture

Validation utilities (checksum, regex, patterns)

AML rule-based engine

Fully REST API-based design

CORS enabled for frontend communication

5) Deployment

Backend: Render / Uvicorn

Frontend: Github Pages

Environment variables for security keys

.gitignore to exclude node_modules/, .env, and build files

--------------------------------------------------------------------------

Tech Stack
Frontend

React.js

JavaScript / TypeScript

Axios (API calls)

Tailwind / CSS modules

Backend

FastAPI

Python 3.10

Uvicorn server

Pydantic for validation

Other Tools

Git & GitHub

Render (backend hosting)

Vercel/Netlify (frontend hosting)
