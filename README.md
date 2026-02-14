🎙️ HR Voice Screening System

An AI-powered resume analysis and automated voice screening platform that helps HR teams shortlist and evaluate candidates efficiently.

🚀 Overview

This system allows candidates to upload resumes, automatically analyzes them against job descriptions using AI, and triggers an automated voice screening call. The results and transcripts are stored for HR review.

🏗️ Architecture Overview
┌─────────────────────────────────────────────────────────┐
│                     FRONTEND (Next.js)                  │
│  - Resume Upload Page                                  │
│  - Candidate Dashboard                                  │
│  - HR Review Panel                                      │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│              BACKEND (Next.js API Routes)               │
│  /api/upload-resume    - Handle PDF upload              │
│  /api/analyze-resume   - Parse & match against JD       │
│  /api/trigger-call     - Initiate voice screening       │
│  /api/webhook/call     - Receive call results           │
└──────────────┬────────────────┬─────────────────────────┘
               │                │
               ▼                ▼
    ┌──────────────┐   ┌──────────────────┐
    │  Claude API  │   │  Vapi.ai / Bland │
    │  (Analysis)  │   │  (Voice Calls)   │
    └──────────────┘   └──────────────────┘
               │                │
               ▼                ▼
    ┌─────────────────────────────────┐
    │   Database (Supabase/JSON)      │
    │   - Candidates                  │
    │   - Job Descriptions            │
    │   - Call Transcripts            │
    └─────────────────────────────────┘

🧠 Core Features
1️⃣ Resume Upload

Candidates upload resumes (PDF)

Files stored securely (e.g., Supabase Storage)

2️⃣ AI Resume Analysis

Extract text from PDF

Match resume against Job Description

Generate:

Skill match score

Strengths & weaknesses

Screening recommendation

3️⃣ Automated Voice Screening

Trigger AI voice call

Ask dynamic screening questions

Record responses

Store transcript & evaluation

4️⃣ HR Dashboard

View candidate profiles

Resume match score

Call transcript

Final AI summary

🛠️ Tech Stack
Frontend

Next.js

React

Tailwind CSS (optional)

Axios / Fetch API

Backend

Next.js API Routes

File handling with FormData

AI integration via API calls

AI Services

Claude API → Resume analysis & scoring

Vapi.ai / Bland.ai → Voice screening automation

Database

Supabase (Postgres + Storage)

Or JSON-based storage (for MVP)