import feedparser
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import requests
import json
import os

# =========================

# 🔧 CONFIG

# =========================

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

KEYWORDS = "backend developer php laravel javascript OR java backend"

# ⭐ Priority countries

PRIORITY = ["Germany", "Netherlands"]

# 📁 Store seen jobs

SEEN_FILE = "seen_jobs.json"

# 🌍 FEEDS

FEEDS = [
# --- Asia ---
{"name": "China", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=China"},
{"name": "Thailand", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Thailand"},
{"name": "Malaysia", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Malaysia"},
{"name": "Singapore", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Singapore"},
{"name": "Saudi Arabia", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Saudi Arabia"},
{"name": "Japan", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Japan"},
{"name": "Taiwan", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Taiwan"},
{"name": "Turkey", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Turkey"},
{"name": "Oman", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Oman"},
{"name": "Kuwait", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Kuwait"},
{"name": "Qatar", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Qatar"},

# --- Remote Only ---
{"name": "Yemen (Remote)", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&f_WT=2"},
{"name": "Egypt (Remote)", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&f_WT=2"},
{"name": "Albania (Remote)", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&f_WT=2"},
{"name": "Belgium (Remote)", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&f_WT=2"},
{"name": "Latvia (Remote)", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&f_WT=2"},
{"name": "Portugal (Remote)", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&f_WT=2"},
{"name": "Romania (Remote)", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&f_WT=2"},

# --- Europe ---
{"name": "Denmark", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Denmark"},
{"name": "Finland", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Finland"},
{"name": "France", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=France"},
{"name": "Germany", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Germany"},
{"name": "Greece", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Greece"},
{"name": "Hungary", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Hungary"},
{"name": "Ireland", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Ireland"},
{"name": "Italy", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Italy"},
{"name": "Luxembourg", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Luxembourg"},
{"name": "Netherlands", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Netherlands"},
{"name": "Norway", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Norway"},
{"name": "Spain", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Spain"},
{"name": "UK", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=United Kingdom"},
{"name": "Sweden", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Sweden"},

# --- Oceania ---
{"name": "Australia", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=Australia"},
{"name": "New Zealand", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=New Zealand"},

# --- USA ---
{"name": "USA", "url": f"https://www.linkedin.com/jobs-guest/jobs/rss/?keywords={KEYWORDS}&location=United States"},

]

# =========================

# 📦 LOAD / SAVE SEEN JOBS

# =========================

def load_seen():
if os.path.exists(SEEN_FILE):
with open(SEEN_FILE, "r") as f:
return set(json.load(f))
return set()

def save_seen(seen):
with open(SEEN_FILE, "w") as f:
json.dump(list(seen), f)

# =========================

# ⏱ FILTER LAST 24H

# =========================

def is_recent(entry):
if hasattr(entry, "published_parsed"):
published = datetime(*entry.published_parsed[:6])
return published > datetime.utcnow() - timedelta(days=1)
return True

# =========================

# 📥 FETCH + FILTER

# =========================

def fetch_jobs():
seen = load_seen()
new_seen = set(seen)
jobs = []

```
for feed in FEEDS:
    parsed = feedparser.parse(feed["url"])

    for entry in parsed.entries:
        job_id = entry.link

        if job_id in seen:
            continue

        if not is_recent(entry):
            continue

        title = entry.title
        link = entry.link
        country = feed["name"]

        job_text = f"[{country}] {title}\n{link}"

        # ⭐ Priority boost
        if country in PRIORITY:
            jobs.insert(0, "🔥 PRIORITY\n" + job_text)
        else:
            jobs.append(job_text)

        new_seen.add(job_id)

save_seen(new_seen)
return jobs[:50]
```

# =========================

# 📧 EMAIL

# =========================

def send_email(jobs):
if not jobs:
return

```
body = "\n\n".join(jobs)

msg = MIMEText(body)
msg['Subject'] = "🔥 Backend Jobs (24h)"
msg['From'] = EMAIL
msg['To'] = EMAIL

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(EMAIL, PASSWORD)
    server.send_message(msg)
```

# =========================

# 🤖 TELEGRAM

# =========================

def send_telegram(jobs):
if not jobs:
return

```
for job in jobs[:10]:  # avoid spam
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": job
    }
    requests.post(url, data=data)
```

# =========================

# 🚀 MAIN

# =========================

if **name** == "**main**":
jobs = fetch_jobs()

```
if jobs:
    send_email(jobs)
    send_telegram(jobs)
    print(f"Sent {len(jobs)} jobs")
else:
    print("No new jobs")
```

