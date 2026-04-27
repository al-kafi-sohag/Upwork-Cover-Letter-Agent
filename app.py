"""
app.py
======
Flask web interface for the Upwork Cover Letter Agent.
Run: python app.py
"""

import os
import logging
from flask import Flask, render_template_string, request, jsonify, send_file
from dotenv import load_dotenv

load_dotenv()

from upwork_agent import generate, WORD_FILE

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("flask_app")

app = Flask(__name__)

# ─────────────────────────── HTML template ──────────────────────────
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Upwork Cover Letter Agent</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0f172a;
    color: #e2e8f0;
    min-height: 100vh;
  }
  .header {
    background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
    border-bottom: 1px solid #1e40af44;
    padding: 20px 32px;
    display: flex;
    align-items: center;
    gap: 14px;
  }
  .header-icon { font-size: 28px; }
  .header h1 { font-size: 20px; font-weight: 700; color: #93c5fd; }
  .header p  { font-size: 13px; color: #64748b; margin-top: 2px; }
  .container { max-width: 1100px; margin: 0 auto; padding: 32px 24px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  @media (max-width: 768px) { .grid { grid-template-columns: 1fr; } }

  .card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 24px;
  }
  .card h2 { font-size: 14px; font-weight: 600; color: #93c5fd; margin-bottom: 14px; text-transform: uppercase; letter-spacing: .5px; }

  textarea {
    width: 100%;
    height: 280px;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    color: #e2e8f0;
    font-size: 14px;
    line-height: 1.6;
    padding: 14px;
    resize: vertical;
    outline: none;
    transition: border-color .2s;
  }
  textarea:focus { border-color: #3b82f6; }
  textarea::placeholder { color: #475569; }

  .btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    border: none;
    transition: all .2s;
    margin-top: 14px;
  }
  .btn-primary {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    width: 100%;
    justify-content: center;
  }
  .btn-primary:hover { background: linear-gradient(135deg, #3b82f6, #2563eb); transform: translateY(-1px); }
  .btn-primary:disabled { opacity: .5; cursor: not-allowed; transform: none; }
  .btn-secondary {
    background: #0f172a;
    color: #93c5fd;
    border: 1px solid #3b82f6;
    font-size: 13px;
    padding: 8px 16px;
  }
  .btn-secondary:hover { background: #1e3a5f; }

  .output-area {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 16px;
    min-height: 280px;
    font-size: 14px;
    line-height: 1.7;
    white-space: pre-wrap;
    color: #e2e8f0;
    position: relative;
  }
  .output-placeholder { color: #475569; }

  .badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    margin-right: 6px;
    margin-bottom: 6px;
  }
  .badge-blue   { background: #1e3a5f; color: #93c5fd; border: 1px solid #1e40af; }
  .badge-green  { background: #14532d; color: #86efac; border: 1px solid #166534; }
  .badge-purple { background: #3b0764; color: #d8b4fe; border: 1px solid #6b21a8; }

  .meta-row { margin-bottom: 14px; }
  .meta-label { font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 6px; }

  .spinner {
    display: none;
    width: 18px; height: 18px;
    border: 2px solid #ffffff44;
    border-top-color: white;
    border-radius: 50%;
    animation: spin .7s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  .steps {
    display: none;
    margin-top: 14px;
    padding: 12px 16px;
    background: #0f172a;
    border: 1px solid #1e40af44;
    border-radius: 8px;
  }
  .step {
    font-size: 12px;
    color: #64748b;
    padding: 3px 0;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .step.active { color: #93c5fd; }
  .step.done   { color: #86efac; }
  .step-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; flex-shrink: 0; }

  .error-box {
    background: #450a0a;
    border: 1px solid #dc2626;
    border-radius: 8px;
    padding: 14px;
    color: #fca5a5;
    font-size: 13px;
    margin-top: 14px;
    display: none;
  }

  .copy-btn {
    position: absolute;
    top: 10px; right: 10px;
    background: #334155;
    border: none;
    color: #93c5fd;
    padding: 5px 10px;
    border-radius: 5px;
    font-size: 11px;
    cursor: pointer;
    display: none;
  }
  .copy-btn:hover { background: #1e40af; }

  .word-download {
    margin-top: 12px;
    display: none;
    align-items: center;
    gap: 8px;
    background: #14532d;
    border: 1px solid #166534;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    color: #86efac;
  }
  .word-download a { color: #86efac; text-decoration: underline; cursor: pointer; }

  .tips {
    margin-top: 16px;
    padding: 12px 16px;
    background: #0f172a;
    border: 1px dashed #334155;
    border-radius: 8px;
    font-size: 12px;
    color: #64748b;
    line-height: 1.6;
  }
  .tips strong { color: #93c5fd; }
</style>
</head>
<body>

<div class="header">
  <div class="header-icon">✍️</div>
  <div>
    <h1>Upwork Cover Letter Agent</h1>
    <p>AI-powered proposal writer · Groq API · Single Word file storage</p>
  </div>
</div>

<div class="container">
  <div class="grid">

    <!-- LEFT: Input -->
    <div>
      <div class="card">
        <h2>📋 Job Description</h2>
        <textarea id="jobDesc" placeholder="Paste the full Upwork job description here...&#10;&#10;The more detail you paste, the better the proposal will be personalised to the client."></textarea>
        <button class="btn btn-primary" id="generateBtn" onclick="generate()">
          <div class="spinner" id="spinner"></div>
          <span id="btnText">Generate Cover Letter</span>
        </button>
        <div class="error-box" id="errorBox"></div>
      </div>

      <!-- Progress steps -->
      <div class="steps" id="steps">
        <div class="step" id="step1"><div class="step-dot"></div> Analysing job description…</div>
        <div class="step" id="step2"><div class="step-dot"></div> Selecting portfolio links…</div>
        <div class="step" id="step3"><div class="step-dot"></div> Writing cover letter…</div>
        <div class="step" id="step4"><div class="step-dot"></div> Polishing &amp; humanising…</div>
        <div class="step" id="step5"><div class="step-dot"></div> Saving to Word document…</div>
      </div>

      <div class="tips">
        <strong>Tips for best results:</strong><br>
        Paste the full job post — title, description, requirements.<br>
        The AI reads the client's exact words to mirror them back naturally.<br>
        If you've generated a letter for a similar job before, it will be used as reference.
      </div>
    </div>

    <!-- RIGHT: Output -->
    <div>
      <div class="card">
        <h2>📄 Generated Cover Letter</h2>

        <div class="meta-row" id="metaRow" style="display:none">
          <div class="meta-label">Detected</div>
          <div id="metaBadges"></div>
        </div>

        <div style="position:relative">
          <div class="output-area" id="output">
            <span class="output-placeholder">Your cover letter will appear here…</span>
          </div>
          <button class="copy-btn" id="copyBtn" onclick="copyLetter()">Copy</button>
        </div>

        <div class="word-download" id="wordDownload">
          💾 Saved to Word file — <a onclick="downloadWord()">Download cover_letters.docx</a>
          &nbsp;|&nbsp; <span id="hasPastNote"></span>
        </div>

        <div class="meta-row" id="portfolioRow" style="display:none; margin-top:14px">
          <div class="meta-label">Portfolio Links Used</div>
          <div id="portfolioLinks" style="font-size:12px; color:#64748b; line-height:1.8;"></div>
        </div>
      </div>
    </div>

  </div>
</div>

<script>
let currentLetter = "";

function setStep(n, state) {
  const el = document.getElementById("step" + n);
  el.className = "step " + state;
}

async function generate() {
  const jd = document.getElementById("jobDesc").value.trim();
  if (!jd) { showError("Please paste a job description first."); return; }

  // Reset UI
  document.getElementById("errorBox").style.display = "none";
  document.getElementById("output").innerHTML = '<span class="output-placeholder">Thinking…</span>';
  document.getElementById("copyBtn").style.display = "none";
  document.getElementById("wordDownload").style.display = "none";
  document.getElementById("metaRow").style.display = "none";
  document.getElementById("portfolioRow").style.display = "none";

  // Button loading state
  const btn = document.getElementById("generateBtn");
  btn.disabled = true;
  document.getElementById("spinner").style.display = "block";
  document.getElementById("btnText").textContent = "Generating…";

  // Show steps
  const stepsEl = document.getElementById("steps");
  stepsEl.style.display = "block";
  for (let i = 1; i <= 5; i++) setStep(i, "");

  // Animate steps (approximate timing)
  const delays = [0, 4000, 8000, 13000, 18000];
  delays.forEach((d, i) => {
    setTimeout(() => setStep(i + 1, "active"), d);
  });

  try {
    const resp = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_description: jd })
    });

    const data = await resp.json();

    if (!resp.ok || data.error) {
      showError(data.error || "Something went wrong. Check the terminal for details.");
      return;
    }

    // Mark all steps done
    for (let i = 1; i <= 5; i++) setStep(i, "done");

    // Show letter
    currentLetter = data.letter;
    document.getElementById("output").textContent = data.letter;
    document.getElementById("copyBtn").style.display = "block";

    // Meta badges
    document.getElementById("metaRow").style.display = "block";
    let badges = `<span class="badge badge-blue">🔑 ${data.keyword}</span>`;
    badges += `<span class="badge badge-purple">🏭 ${data.industry}</span>`;
    (data.tech_stack || []).forEach(t => { badges += `<span class="badge badge-green">${t}</span>`; });
    document.getElementById("metaBadges").innerHTML = badges;

    // Portfolio
    if (data.portfolio) {
      document.getElementById("portfolioRow").style.display = "block";
      document.getElementById("portfolioLinks").textContent = data.portfolio;
    }

    // Word download
    document.getElementById("wordDownload").style.display = "flex";
    document.getElementById("hasPastNote").textContent = data.has_past
      ? "✓ Used past letters as reference"
      : "First entry for this keyword";

  } catch (err) {
    showError("Network error: " + err.message);
  } finally {
    btn.disabled = false;
    document.getElementById("spinner").style.display = "none";
    document.getElementById("btnText").textContent = "Generate Cover Letter";
  }
}

function showError(msg) {
  const box = document.getElementById("errorBox");
  box.textContent = "❌ " + msg;
  box.style.display = "block";
  document.getElementById("steps").style.display = "none";
}

function copyLetter() {
  navigator.clipboard.writeText(currentLetter).then(() => {
    const btn = document.getElementById("copyBtn");
    btn.textContent = "Copied!";
    setTimeout(() => btn.textContent = "Copy", 2000);
  });
}

function downloadWord() {
  window.location.href = "/download";
}
</script>
</body>
</html>"""


# ─────────────────────────── routes ─────────────────────────────

@app.route("/")
def index():
    logger.info("GET / — serving UI")
    return render_template_string(HTML)


@app.route("/generate", methods=["POST"])
def api_generate():
    data = request.get_json()
    job_description = (data or {}).get("job_description", "").strip()

    if not job_description:
        logger.warning("Generate called with empty job description")
        return jsonify({"error": "Job description is required."}), 400

    logger.info(f"POST /generate — job desc length={len(job_description)} chars")

    try:
        result = generate(job_description)
        return jsonify(result)
    except ValueError as e:
        logger.error(f"ValueError: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return jsonify({"error": f"Generation failed: {str(e)}"}), 500


@app.route("/download")
def download():
    if not os.path.exists(WORD_FILE):
        logger.warning("Download requested but Word file does not exist")
        return "No Word file found. Generate a cover letter first.", 404
    logger.info(f"Serving Word file: {WORD_FILE}")
    return send_file(
        os.path.abspath(WORD_FILE),
        as_attachment=True,
        download_name="cover_letters.docx",
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


# ─────────────────────────── main ───────────────────────────────

if __name__ == "__main__":
    host  = os.getenv("FLASK_HOST", "127.0.0.1")
    port  = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    logger.info(f"Starting Upwork Cover Letter Agent on http://{host}:{port}")
    logger.info(f"Word file: {os.path.abspath(WORD_FILE)}")
    logger.info(f"Groq model: {os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')}")

    app.run(host=host, port=port, debug=debug)
