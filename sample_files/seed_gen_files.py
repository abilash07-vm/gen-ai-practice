import os, json, csv, zipfile, textwrap, random, io, math
from datetime import datetime, timedelta
from pathlib import Path

base = Path("/mnt/data/langchain_learning_corpus")
if base.exists():
    import shutil
    shutil.rmtree(base)
base.mkdir(parents=True, exist_ok=True)

folders = [
    "text",
    "markdown",
    "data",
    "code/python",
    "code/javascript",
    "code/java",
    "code/c_cpp",
    "code/misc",
    "config",
    "markup",
    "logs",
    "emails",
    "docs",
    "office",
    "media_like",
]
for f in folders:
    (base / f).mkdir(parents=True, exist_ok=True)

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

# README
readme = """# LangChain Learning Corpus

This zip contains 120+ sample files across many formats to help you learn:

- document loaders
- text splitting
- metadata extraction
- chunking strategies
- vector stores
- RAG pipelines
- retrievers
- filtering by source/type
- multi-format ingestion

## Included categories
- Plain text, notes, transcripts, FAQs
- Markdown docs and wiki pages
- Structured data: CSV, TSV, JSON, JSONL, NDJSON
- Config files: YAML, TOML, INI, ENV, properties, conf
- Markup: HTML, XML, SVG, LaTeX, RST
- Code files in many languages
- Logs and pseudo application traces
- Email samples (.eml)
- Office-style files: DOCX, XLSX, PPTX, PDF

## Suggested exercises
1. Load only text-like files and inspect metadata
2. Compare chunking for markdown vs plain text
3. Build a retriever over product docs + tickets
4. Filter by extension or folder
5. Try separate loaders for PDF/DOCX/XLSX/PPTX
6. Create parent-child retrieval using long reports
7. Build source-aware answers using metadata

Generated on: {generated}
""".format(generated=datetime.now().isoformat(timespec="seconds"))
write(base / "README.md", readme)

# Text files
text_files = {
    "customer_support_notes.txt": """Customer Support Notes

Issue categories:
1. Login failures after password reset
2. PDF export timing out for reports above 20 pages
3. Search returning stale cache results
4. Users asking for dark mode in admin portal

Observed pattern:
Most login failures are caused by users reusing an old browser tab after reset.
""",
    "product_requirements.txt": """Product Requirements Summary

Project: Knowledge Assistant
Target users: internal operations teams
Core features:
- ingest PDFs, DOCX, and webpages
- semantic search over policies
- answer generation with citations
- source filters by department
Non-functional:
- response time under 4 seconds for top 5 answers
- support documents up to 50 MB
""",
    "meeting_transcript.txt": """Meeting Transcript

Asha: We need a clearer ingestion pipeline for mixed file formats.
Rahul: Let's separate parsing, cleaning, and chunking.
Asha: Also record file type, source path, owner, and created date.
Rahul: That metadata will help retrieval filters later.
""",
    "incident_report.txt": """Incident Report

Date: 2026-04-20
Severity: Medium
Service: document-indexer
Summary: The indexer skipped 37 XML files after a malformed character sequence.
Resolution: Added fallback encoding detection and quarantine queue.
Preventive action: Add validation before chunking.
""",
    "employee_handbook_excerpt.txt": """Employee Handbook Excerpt

Working hours are flexible between 8:00 AM and 7:00 PM local time.
Employees are encouraged to document project decisions in the team wiki.
Confidential customer data must not be copied to public repositories.
""",
    "faq_plain_text.txt": """FAQ

Q: What is LangChain used for?
A: It helps build applications with LLMs, tools, retrieval, and workflows.

Q: Why does chunk size matter?
A: It changes context quality, recall, and token usage.
""",
    "research_abstract.txt": """Research Abstract

Hybrid retrieval combines sparse lexical signals with dense vector representations.
In enterprise search, hybrid retrieval often improves first-pass recall for short factual queries.
Future work includes better reranking and source attribution.
""",
    "shopping_list_dataset.txt": """Shopping List Dataset

milk
bread
coffee
notebook
hdmi cable
wireless mouse
standing desk mat
""",
    "travel_itinerary.txt": """Travel Itinerary

Day 1: Arrive in Bengaluru, hotel check-in, evening client dinner.
Day 2: Office visit, architecture review, data pipeline workshop.
Day 3: Customer demo, feedback capture, return flight.
""",
    "book_chapter_excerpt.txt": """Book Chapter Excerpt

Chapter 4 discusses information retrieval systems and how ranking quality depends on indexing,
query understanding, document representation, and evaluation metrics such as precision and recall.
""",
    "customer_feedback.txt": """Customer Feedback

"The search is fast, but I need better filtering by date."
"Please show the document title and page number in answers."
"The summarization feature is useful for meeting notes."
""",
    "training_schedule.txt": """Training Schedule

Week 1: Loaders and parsers
Week 2: Chunking and embeddings
Week 3: Retrieval and reranking
Week 4: Agents, tools, and memory
""",
}
for name, content in text_files.items():
    write(base / "text" / name, content)

# More text variants
for i in range(1, 9):
    write(base / "text" / f"note_{i:02d}.txt", f"Sample note {i}\n\nThis is a short learning note for LangChain practice.\nTopic: metadata extraction, chunking, and retrieval.\nDocument id: TXT-{i:02d}\n")

# Markdown files
markdown_docs = {
    "architecture_overview.md": """# Architecture Overview

## Components
- loader
- parser
- splitter
- embedder
- vector store
- retriever
- answer chain

## Notes
Use metadata fields like `source`, `owner`, `team`, and `doc_type`.
""",
    "api_reference.md": """# API Reference

## POST /ingest
Uploads a document and triggers parsing.

## POST /query
Accepts user question and optional filters.

## GET /health
Returns service health and dependency status.
""",
    "release_notes.md": """# Release Notes

## v1.2.0
- added JSONL loader
- improved markdown heading splitting
- fixed bad UTF-8 fallback

## v1.1.0
- initial retrieval pipeline
""",
    "onboarding_guide.md": """# Onboarding Guide

1. Clone the repo
2. Create a virtual environment
3. Install dependencies
4. Add environment variables
5. Run the ingestion script
""",
    "team_wiki_page.md": """# Team Wiki

## Naming convention
Use lowercase filenames with underscores.

## Documentation rule
Add summary, owner, date, and tags at the top of every design note.
""",
    "prompt_patterns.md": """# Prompt Patterns

## Retrieval QA
Answer only from the provided context.

## Summarization
Summarize with bullet points, risks, and next steps.

## Extraction
Return JSON with stable keys and null for unknown values.
""",
    "dataset_card.md": """# Dataset Card

**Name:** Support Tickets Lite  
**Language:** English  
**Rows:** 500 synthetic examples  
**Use cases:** classification, semantic search, summarization
""",
    "knowledge_base_article.md": """# Resetting Two-Factor Authentication

If a user loses access to their authenticator device, verify identity through the support checklist.
After approval, disable the existing MFA method and enforce re-enrollment on next login.
""",
}
for name, content in markdown_docs.items():
    write(base / "markdown" / name, content)
for i in range(1, 9):
    write(base / "markdown" / f"lesson_{i:02d}.md", f"# Lesson {i}\n\nThis markdown lesson explains a LangChain concept.\n\n## Topic\nChunking strategy {i}\n\n## Example\nUse recursive splitting for long prose and header-based splitting for markdown.\n")

# Structured data
products = [
    ["product_id","name","category","price","stock","rating"],
    ["P001","Wireless Mouse","Accessories",799,120,4.4],
    ["P002","Mechanical Keyboard","Accessories",2499,75,4.6],
    ["P003","USB-C Hub","Accessories",1599,63,4.1],
    ["P004","Laptop Stand","Office",1899,40,4.5],
    ["P005","Noise Cancelling Headphones","Audio",6999,22,4.7],
]
with open(base / "data" / "products.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(products)

tickets = [
    ["ticket_id","priority","team","status","summary"],
    ["T1001","High","Platform","Open","API gateway timeout under load"],
    ["T1002","Low","Design","Closed","Icon misalignment on dashboard"],
    ["T1003","Medium","Search","Open","Ranking quality drop on short queries"],
    ["T1004","High","Security","Investigating","Expired certificate on staging"],
]
with open(base / "data" / "support_tickets.tsv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f, delimiter="\t").writerows(tickets)

inventory = [
    {"sku":"SKU-100","name":"Notebook","warehouse":"WH-A","qty":180},
    {"sku":"SKU-101","name":"Marker","warehouse":"WH-A","qty":72},
    {"sku":"SKU-102","name":"Webcam","warehouse":"WH-B","qty":15},
]
write(base / "data" / "inventory.json", json.dumps(inventory, indent=2))
write(base / "data" / "users.jsonl", "\n".join(json.dumps(x) for x in [
    {"user_id":1,"name":"Anita","role":"admin","active":True},
    {"user_id":2,"name":"Kiran","role":"analyst","active":True},
    {"user_id":3,"name":"Leela","role":"viewer","active":False},
]))
write(base / "data" / "events.ndjson", "\n".join(json.dumps(x) for x in [
    {"ts":"2026-04-20T09:10:00","event":"login","user":"Anita"},
    {"ts":"2026-04-20T09:12:00","event":"upload","user":"Kiran"},
    {"ts":"2026-04-20T09:18:00","event":"query","user":"Anita"},
]))
write(base / "data" / "metrics.xml", """<?xml version="1.0" encoding="UTF-8"?>
<metrics>
  <service name="ingest">
    <latency_p95_ms>840</latency_p95_ms>
    <error_rate>0.02</error_rate>
  </service>
  <service name="query">
    <latency_p95_ms>620</latency_p95_ms>
    <error_rate>0.01</error_rate>
  </service>
</metrics>
""")
write(base / "data" / "countries.yaml", """countries:
  - code: IN
    name: India
    region: Asia
  - code: US
    name: United States
    region: North America
  - code: DE
    name: Germany
    region: Europe
""")
write(base / "data" / "sales_report.toml", """[summary]
quarter = "Q1-2026"
revenue = 1250000
currency = "INR"

[regions]
south = 420000
west = 350000
north = 280000
east = 200000
""")
for i in range(1, 11):
    write(base / "data" / f"sample_data_{i:02d}.json", json.dumps({
        "id": i,
        "title": f"Sample data record {i}",
        "tags": ["langchain", "learning", f"set-{(i%3)+1}"],
        "score": round(0.5 + i/20, 2)
    }, indent=2))

# Config files
config_files = {
    ".env": "OPENAI_API_KEY=demo-key\nAPP_ENV=development\nVECTOR_DB=chroma\nTOP_K=5\n",
    "settings.ini": "[app]\nname = rag_demo\nmode = local\n\n[retrieval]\nchunk_size = 800\noverlap = 120\n",
    "application.properties": "server.port=8000\napp.name=knowledge-assistant\nretriever.topK=5\n",
    "docker.conf": "workers=2\nthreads=4\nlog_level=info\n",
    "pipeline.yaml": "loader: unstructured\nsplitter: recursive\nembedding_model: text-embedding-demo\nvector_store: chroma\n",
    "service.toml": 'name = "query-service"\nversion = "0.1.0"\n[http]\nport = 8080\ntimeout = 30\n',
    "parser_rules.conf": "allow_pdf=true\nallow_docx=true\nallow_html=true\nmax_file_size_mb=50\n",
    "mappings.json": json.dumps({"txt":"text/plain","md":"text/markdown","json":"application/json"}, indent=2),
    "feature_flags.yml": "flags:\n  enable_reranker: true\n  enable_citations: true\n  enable_feedback: false\n",
    "airflow_like.cfg": "[scheduler]\nmax_threads = 4\n\n[logging]\nlevel = INFO\n",
}
for name, content in config_files.items():
    write(base / "config" / name, content)
for i in range(1, 11):
    write(base / "config" / f"profile_{i:02d}.env", f"PROFILE=profile_{i:02d}\nCACHE_TTL={i*10}\nENABLE_TRACE={'true' if i%2 else 'false'}\n")

# Markup and misc parsable files
markup_files = {
    "landing_page.html": """<!doctype html>
<html><head><title>Knowledge Portal</title></head>
<body>
<h1>Knowledge Portal</h1>
<p>This portal hosts policies, guides, and troubleshooting notes.</p>
<ul><li>Search</li><li>Browse</li><li>Summarize</li></ul>
</body></html>""",
    "faq_page.htm": """<html><body><h2>FAQ</h2><p>How do I reset my password? Use the account security page.</p></body></html>""",
    "catalog.xml": """<?xml version="1.0"?><catalog><book id="b1"><title>IR Basics</title></book><book id="b2"><title>LLM Systems</title></book></catalog>""",
    "diagram.svg": """<svg xmlns="http://www.w3.org/2000/svg" width="400" height="120">
<rect x="10" y="10" width="100" height="40" fill="#eaeaea" stroke="#333"/>
<text x="25" y="35" font-size="14">Loader</text>
<rect x="145" y="10" width="100" height="40" fill="#eaeaea" stroke="#333"/>
<text x="160" y="35" font-size="14">Splitter</text>
<rect x="280" y="10" width="100" height="40" fill="#eaeaea" stroke="#333"/>
<text x="295" y="35" font-size="14">Retriever</text>
</svg>""",
    "paper.tex": r"""\documentclass{article}
\begin{document}
\section*{Sample LaTeX Note}
This is a small document for parser experiments.
\end{document}
""",
    "guide.rst": """Guide
=====

Overview
--------

This is a reStructuredText sample for documentation ingestion.
""",
    "notes.xhtml": """<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml"><body><p>XHTML sample.</p></body></html>""",
}
for name, content in markup_files.items():
    write(base / "markup" / name, content)
for i in range(1, 9):
    write(base / "markup" / f"web_fragment_{i:02d}.html", f"<html><body><h3>Fragment {i}</h3><p>Sample HTML fragment for ingestion test {i}.</p></body></html>")

# Logs
for i in range(1, 13):
    lines = []
    start = datetime(2026, 4, 20, 9, 0, 0) + timedelta(minutes=i)
    for j in range(12):
        ts = (start + timedelta(seconds=j*15)).isoformat()
        level = ["INFO", "INFO", "WARN", "INFO", "ERROR"][j % 5]
        lines.append(f"{ts} {level} service=document-indexer request_id=req-{i:02d}-{j:02d} message=sample_log_event_{j}")
    write(base / "logs" / f"app_log_{i:02d}.log", "\n".join(lines) + "\n")

# Emails
for i in range(1, 9):
    eml = f"""From: sender{i}@example.com
To: learner@example.com
Subject: Sample Email {i}
Date: Wed, 22 Apr 2026 10:0{i}:00 +0530
MIME-Version: 1.0
Content-Type: text/plain; charset="UTF-8"

Hello,
This is sample email number {i} for LangChain email parsing experiments.
Regards,
Team Demo
"""
    write(base / "emails" / f"sample_email_{i:02d}.eml", eml)

# Code samples
code_map = {
    ("code/python", "app.py"): """from fastapi import FastAPI\napp = FastAPI()\n\n@app.get('/health')\ndef health():\n    return {'status': 'ok'}\n""",
    ("code/python", "chunking_demo.py"): """def split_text(text, size=200):\n    return [text[i:i+size] for i in range(0, len(text), size)]\n""",
    ("code/python", "retriever_stub.py"): """class Retriever:\n    def __init__(self, store):\n        self.store = store\n\n    def search(self, query):\n        return self.store.get(query, [])\n""",
    ("code/javascript", "server.js"): """const http = require('http');\nhttp.createServer((req,res)=>{res.end('ok');}).listen(3000);\n""",
    ("code/javascript", "utils.js"): """export function normalize(text){ return text.trim().toLowerCase(); }\n""",
    ("code/java", "Main.java"): """public class Main {\n  public static void main(String[] args){\n    System.out.println(\"Hello LangChain\");\n  }\n}\n""",
    ("code/java", "Ticket.java"): """public class Ticket {\n  private String id;\n  private String status;\n}\n""",
    ("code/c_cpp", "main.c"): """#include <stdio.h>\nint main(){ printf(\"hello\\n\"); return 0; }\n""",
    ("code/c_cpp", "sort.cpp"): """#include <vector>\n#include <algorithm>\nint main(){ std::vector<int> v={3,1,2}; std::sort(v.begin(), v.end()); }\n""",
    ("code/misc", "script.sh"): "#!/bin/bash\necho \"ingest started\"\n",
    ("code/misc", "build.bat"): "@echo off\necho Building sample project\n",
    ("code/misc", "deploy.ps1"): "Write-Output \"Deploying demo stack\"\n",
    ("code/misc", "app.go"): "package main\nimport \"fmt\"\nfunc main(){ fmt.Println(\"hello\") }\n",
    ("code/misc", "analyze.rb"): "puts 'ruby sample'\n",
    ("code/misc", "index.php"): "<?php echo 'php sample'; ?>\n",
    ("code/misc", "service.kt"): "fun main(){ println(\"kotlin sample\") }\n",
    ("code/misc", "ios.swift"): "print(\"swift sample\")\n",
    ("code/misc", "analysis.r"): "x <- c(1,2,3)\nmean(x)\n",
    ("code/misc", "style.css"): "body { font-family: Arial; margin: 16px; }\n",
    ("code/misc", "query.sql"): "SELECT ticket_id, status FROM tickets WHERE priority = 'High';\n",
}
for (folder, name), content in code_map.items():
    write(base / folder / name, content)

# More code variety
extra_code = [
    ("code/python", f"module_{i:02d}.py", f"def func_{i}():\n    return 'module {i}'\n") for i in range(1, 9)
] + [
    ("code/javascript", f"widget_{i:02d}.ts", f"export const item{i}: string = 'widget {i}';\n") for i in range(1, 7)
] + [
    ("code/misc", f"tool_{i:02d}.scala", f"object Tool{i} extends App {{ println(\"scala {i}\") }}\n") for i in range(1, 4)
]
for folder, name, content in extra_code:
    write(base / folder / name, content)

# Docs folder
for i in range(1, 11):
    write(base / "docs" / f"case_study_{i:02d}.md", f"# Case Study {i}\n\nProblem: improve search quality for dataset {i}.\nApproach: better chunking, metadata enrichment, and reranking.\nOutcome: simulated improvement in first relevant hit.\n")
for i in range(1, 7):
    write(base / "docs" / f"policy_{i:02d}.txt", f"Policy {i}\n\nThis is a sample policy document intended for retrieval practice.\nDocument classification: internal\nReview cycle: annual\n")

# Media-like captions/subtitles
write(base / "media_like" / "video_subtitles.srt", """1
00:00:00,000 --> 00:00:02,000
Welcome to the retrieval tutorial.

2
00:00:02,100 --> 00:00:05,000
In this lesson, we compare chunk sizes and overlaps.
""")
write(base / "media_like" / "meeting_captions.vtt", """WEBVTT

00:00:00.000 --> 00:00:02.000
Today we review document ingestion metrics.

00:00:02.100 --> 00:00:05.000
Next, we discuss metadata normalization.
""")

# Office files
from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from pptx import Presentation
from pptx.util import Inches

# DOCX
doc = Document()
doc.add_heading("Sample Project Proposal", 0)
doc.add_paragraph("This DOCX file is included for loader and parser experiments.")
doc.add_heading("Objectives", level=1)
for item in [
    "Ingest mixed document formats",
    "Store metadata for filtering",
    "Enable semantic retrieval with citations",
]:
    doc.add_paragraph(item, style="List Bullet")
doc.add_heading("Notes", level=1)
doc.add_paragraph("Use this file to test DOCX loading, text extraction, and metadata capture.")
doc.save(base / "office" / "sample_proposal.docx")

# Another DOCX
doc2 = Document()
doc2.add_heading("Employee Policy Memo", 0)
doc2.add_paragraph("Hybrid work is supported subject to team approval and security guidelines.")
doc2.add_paragraph("Sensitive documents must remain inside approved storage systems.")
doc2.save(base / "office" / "policy_memo.docx")

# XLSX
wb = Workbook()
ws = wb.active
ws.title = "Sales"
ws.append(["Month", "Revenue", "Cost", "Profit"])
rows = [
    ("Jan", 120000, 80000, 40000),
    ("Feb", 140000, 90000, 50000),
    ("Mar", 135000, 88000, 47000),
    ("Apr", 150000, 93000, 57000),
]
for r in rows:
    ws.append(r)
wb.save(base / "office" / "quarterly_sales.xlsx")

wb2 = Workbook()
ws2 = wb2.active
ws2.title = "Tickets"
ws2.append(["Ticket", "Priority", "Status", "Owner"])
for r in [["T1","High","Open","Anita"],["T2","Low","Closed","Kiran"],["T3","Medium","Open","Leela"]]:
    ws2.append(r)
wb2.save(base / "office" / "ticket_tracker.xlsx")

# PPTX
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Knowledge Assistant Demo"
slide.placeholders[1].text = "Mixed-format ingestion\nSemantic retrieval\nSource citations"
slide2 = prs.slides.add_slide(prs.slide_layouts[5])
slide2.shapes.title.text = "Pipeline"
tx = slide2.shapes.add_textbox(Inches(1), Inches(1.5), Inches(8), Inches(3))
tf = tx.text_frame
tf.text = "Loader -> Splitter -> Embeddings -> Vector Store -> Retriever -> Answer"
prs.save(base / "office" / "demo_deck.pptx")

prs2 = Presentation()
slide = prs2.slides.add_slide(prs2.slide_layouts[0])
slide.shapes.title.text = "Weekly Review"
slide.placeholders[1].text = "Synthetic slide deck for LangChain practice"
prs2.save(base / "office" / "weekly_review.pptx")

# PDF
pdf_path = base / "office" / "sample_report.pdf"
c = canvas.Canvas(str(pdf_path), pagesize=A4)
w, h = A4
c.setFont("Helvetica-Bold", 16)
c.drawString(72, h - 72, "Sample PDF Report")
c.setFont("Helvetica", 11)
lines = [
    "This PDF is a simple sample for LangChain learning.",
    "It contains plain text content across a few lines.",
    "You can use it to test PDF loaders and chunking behavior.",
    "Consider extracting metadata such as title and file path.",
]
y = h - 110
for line in lines:
    c.drawString(72, y, line)
    y -= 18
c.showPage()
c.save()

pdf_path2 = base / "office" / "troubleshooting_note.pdf"
c = canvas.Canvas(str(pdf_path2), pagesize=A4)
c.setFont("Helvetica-Bold", 14)
c.drawString(72, h - 72, "Troubleshooting Note")
c.setFont("Helvetica", 11)
for idx, line in enumerate([
    "Symptom: answers returned without citations.",
    "Cause: retriever metadata was not preserved after chunking.",
    "Fix: carry source id, title, and page markers into chunks.",
]):
    c.drawString(72, h - 110 - idx*18, line)
c.showPage()
c.save()

# Create manifest
all_files = []
for p in sorted(base.rglob("*")):
    if p.is_file():
        all_files.append(str(p.relative_to(base)))
write(base / "manifest.txt", "\n".join(all_files) + "\n")

# Zip
zip_path = Path("/mnt/data/langchain_learning_corpus_125_files.zip")
if zip_path.exists():
    zip_path.unlink()

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for p in sorted(base.rglob("*")):
        if p.is_file():
            zf.write(p, arcname=str(p.relative_to(base)))

print(f"Created: {zip_path}")
print(f"Total files: {len(all_files)}")
print("Sample files:")
for item in all_files[:20]:
    print("-", item)