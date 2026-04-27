# ✍️ Upwork Cover Letter Agent

A local Python web app that generates human, job-winning Upwork cover letters using the **Groq API** (free). Paste a job description, get a personalised proposal in seconds, and keep every letter saved in a single **Word document** — your permanent library of winning proposals.

---

## How It Works

```
Job Description (you paste)
        │
        ▼
  ┌─────────────────────────────────────────────────┐
  │  PASS 1 — Analyse Job                           │
  │  Extracts: keyword, industry, tech stack,       │
  │  client pain point, tone, urgency               │
  └──────────────────┬──────────────────────────────┘
                     │
                     ▼
  ┌─────────────────────────────────────────────────┐
  │  Read Word Doc — Past Letters for this Keyword  │
  │  (used as context for the AI — learns your      │
  │  successful patterns over time)                 │
  └──────────────────┬──────────────────────────────┘
                     │
                     ▼
  ┌─────────────────────────────────────────────────┐
  │  PASS 2 — Pick Portfolio Links                  │
  │  Selects 1–3 most relevant projects from        │
  │  your full portfolio for this specific job      │
  └──────────────────┬──────────────────────────────┘
                     │
                     ▼
  ┌─────────────────────────────────────────────────┐
  │  PASS 3 — Generate Cover Letter                 │
  │  Human tone, 150–200 words, mirrors client      │
  │  language, includes relevant keywords           │
  └──────────────────┬──────────────────────────────┘
                     │
                     ▼
  ┌─────────────────────────────────────────────────┐
  │  PASS 4 — Polish & Humanise                     │
  │  Removes AI buzzwords, checks opening,          │
  │  ensures closing question                       │
  └──────────────────┬──────────────────────────────┘
                     │
                     ▼
  ┌─────────────────────────────────────────────────┐
  │  Save to cover_letters.docx                     │
  │  Keyword + date + job desc + letter             │
  │  Single file — your permanent library           │
  └─────────────────────────────────────────────────┘
```

---

## Features

- **4-pass AI pipeline** — analyse → select portfolio → write → polish
- **Groq API** (free tier, no cost for typical usage)
- **Single Word file** — every letter stored with keyword, date, job description
- **Past letter retrieval** — if you've written for the same keyword before, the AI references those letters to improve over time
- **Smart portfolio matching** — picks the 1–3 most relevant project links for each job
- **Human-first writing rules** — no buzzwords, mirrors client language, ends with a question
- **Full logging** — INFO and ERROR logs so you can see exactly what the agent is doing
- **Clean web UI** — dark themed, shows progress steps, one-click copy and Word download

---

## Project Structure

```
upwork_agent/
├── app.py              # Flask web server + UI
├── upwork_agent.py     # Core AI agent logic
├── requirements.txt    # Python dependencies
├── .env.example        # Configuration template
├── .gitignore
├── README.md
└── cover_letters.docx  # Created automatically on first use
```

---

## Quick Start

### 1. Get a Free Groq API Key

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up (free — no credit card needed)
3. Click **API Keys** → **Create API Key**
4. Copy your key

---

### 2. Clone / Download the Project

```bash
# If using git:
git clone <your-repo-url>
cd upwork_agent

# Or just download and unzip the folder, then:
cd upwork_agent
```

---

### 3. Set Up Python Environment

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Open .env and add your Groq API key:
# GROQ_API_KEY=gsk_your_key_here
```

Your `.env` file should look like:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxx
GROQ_MODEL=llama-3.3-70b-versatile
WORD_FILE=cover_letters.docx
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=false
LOG_LEVEL=INFO
```

---

### 6. Run the App

```bash
python app.py
```

You'll see:

```
2025-04-27 10:00:00 [INFO] flask_app — Starting Upwork Cover Letter Agent on http://127.0.0.1:5000
2025-04-27 10:00:00 [INFO] flask_app — Word file: /path/to/cover_letters.docx
2025-04-27 10:00:00 [INFO] flask_app — Groq model: llama-3.3-70b-versatile
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## Using the App

1. **Paste the full job description** from Upwork into the text box
   - Copy everything: title, description, requirements
   - The more detail, the better the personalisation
2. **Click "Generate Cover Letter"**
   - Watch the 4 progress steps complete (usually 20–35 seconds)
3. **Review the letter** — copy it with one click
4. **Download the Word file** — all letters saved permanently
5. **Customise before sending** — look for `[Client Name]` or `[Hi there]` placeholders and personalise

---

## The Word Document (cover_letters.docx)

This is your **single source of truth**. Every generated letter is stored here with:

- **Keyword** (e.g. `WordPress Website Troubleshooting`)
- **Date and time** generated
- **Industry + tech stack** detected
- **Original job description** (so you can reference it later)
- **Cover letter** that was generated

When you generate a new letter for the **same keyword**, the AI automatically reads your past letters and uses them as reference — so it gets better with every use.

> **Back this file up** — it's your library of winning proposals.

---

## Customising Your Profile

Open `upwork_agent.py` and find the `FREELANCER_PROFILE` section near the top.

You can update:
- Your portfolio links (add new projects as you complete them)
- Your skills and experience
- Your differentiators

Keep it updated — the AI uses this data to write every letter.

---

## Updating Proposal Writing Tips

Open `upwork_agent.py` and find the `PROPOSAL_TIPS` section.

You can add or modify the rules the AI follows when writing letters — for example, if you discover a new pattern that works, add it here.

---

## Available Groq Models

The default model is `llama-3.3-70b-versatile` which is fast and free. Other options:

| Model | Speed | Quality |
|-------|-------|---------|
| `llama-3.3-70b-versatile` | Fast | ⭐⭐⭐⭐⭐ (recommended) |
| `llama-3.1-8b-instant` | Very fast | ⭐⭐⭐ |
| `mixtral-8x7b-32768` | Medium | ⭐⭐⭐⭐ |
| `gemma2-9b-it` | Fast | ⭐⭐⭐⭐ |

Change it in `.env`:
```
GROQ_MODEL=llama-3.1-8b-instant
```

---

## Logging

The app logs everything to the terminal. Log levels:

| Level | What it shows |
|-------|--------------|
| `DEBUG` | Every detail, including full API payloads |
| `INFO` | Normal operation — steps, timings, file saves |
| `WARNING` | Non-critical issues |
| `ERROR` | Problems that need attention |

Set in `.env`: `LOG_LEVEL=DEBUG`

Example log output:
```
2025-04-27 10:01:00 [INFO] upwork_agent — Starting cover letter generation pipeline
2025-04-27 10:01:00 [INFO] upwork_agent — Pass 1: Analysing job description...
2025-04-27 10:01:00 [INFO] upwork_agent — Calling Groq API | model=llama-3.3-70b-versatile | messages=2
2025-04-27 10:01:03 [INFO] upwork_agent — Groq API response received | chars=312
2025-04-27 10:01:03 [INFO] upwork_agent — Job analysis: keyword='WordPress Troubleshooting' industry='E-commerce'
2025-04-27 10:01:03 [INFO] upwork_agent — Reading past letters for keyword: 'WordPress Troubleshooting'
2025-04-27 10:01:03 [INFO] upwork_agent — No past letters found for keyword 'WordPress Troubleshooting'
2025-04-27 10:01:03 [INFO] upwork_agent — Pass 2: Selecting relevant portfolio links...
2025-04-27 10:01:06 [INFO] upwork_agent — Pass 3: Generating cover letter...
2025-04-27 10:01:12 [INFO] upwork_agent — Cover letter generated | chars=872
2025-04-27 10:01:12 [INFO] upwork_agent — Pass 4: Polishing cover letter...
2025-04-27 10:01:16 [INFO] upwork_agent — Saved successfully to 'cover_letters.docx'
2025-04-27 10:01:16 [INFO] upwork_agent — Pipeline complete ✓
```

---

## Troubleshooting

**"GROQ_API_KEY is not set"**
→ Make sure you created a `.env` file (not just `.env.example`) and added your key.

**"Generation failed"**
→ Check the terminal for the full error. Usually it's a Groq rate limit (wait a few seconds and retry).

**Word file won't open**
→ Make sure `python-docx` is installed: `pip install python-docx`

**Port already in use**
→ Change `FLASK_PORT=5001` in your `.env` file.

**Letters sound too generic**
→ Paste more of the job description — include the full text, not just the title.

---

## Tips for Best Results

1. **Paste the full job post** — title, description, requirements, even the client's questions
2. **Generate more letters** — the AI gets smarter as it references your past successful ones
3. **Always customise** before sending — replace `[Client Name]` and tweak the opening line
4. **Add new portfolio links** to `upwork_agent.py` as you complete projects
5. **Adjust the tone** in `PROPOSAL_TIPS` if you find something that works better for your niche

---

## Requirements

- Python 3.10+
- Free Groq API account
- Internet connection (for API calls)

---

## License

Personal use. All portfolio links and profile data belong to the respective owner.
