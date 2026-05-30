# Prospect Research Agent

## Overview

Prospect Research Agent is an AI-powered web application that enriches company profiles from website URLs. The system intelligently scrapes relevant company pages, extracts key business information, and uses Google Gemini to generate structured business insights.

The project was developed for the AI & Automation Developer Hackathon.

---

## Features

### Research Pipeline

* Smart website scraping using:

  * Sitemap discovery
  * Internal link extraction
  * Fuzzy matching for relevant pages
* Multi-approach scraping fallback strategy
* HTML cleaning and token optimization
* Email and phone extraction using regex
* AI-powered company enrichment using Google Gemini
* Structured JSON output

### Web Application

#### Backend APIs

##### POST /enrich

Input:

```json
{
  "url": "https://example.com"
}
```

Output:

```json
{
  "website_name": "",
  "company_name": "",
  "address": "",
  "mobile_number": "",
  "mail": [],
  "core_service": "",
  "target_customer": "",
  "probable_pain_point": "",
  "outreach_opener": ""
}
```

##### GET /results

Returns all previously enriched companies.

---

## Technology Stack

### Backend

* FastAPI
* Requests
* BeautifulSoup4
* RapidFuzz
* Google Gemini API
* Python

### Frontend

* React
* Vite
* Axios

---

## Project Structure

```text
research_agent/
│
├── backend/
│   ├── main.py
│   ├── scraper.py
│   ├── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── components/
│   │       ├── EnrichForm.jsx
│   │       └── ResultsTable.jsx
│   │
│   ├── package.json
│   └── index.html
│
├── README.md
└── results.json
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd research_agent
```

---

### Backend Setup

```bash
cd backend

python -m venv .venv

source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run backend:

```bash
uvicorn main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

Swagger docs:

```text
http://localhost:8000/docs
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## Smart Scraping Strategy

The scraper uses multiple approaches:

### Approach 1

Sitemap discovery:

```text
https://company.com/sitemap.xml
```

### Approach 2

Homepage link extraction and fuzzy matching.

Target pages:

* About
* Contact
* Services
* Solutions
* Team
* Leadership

### Approach 3

Homepage fallback scraping.

---

## Token Optimization

Before sending content to Gemini:

* Removes scripts
* Removes styles
* Removes navigation bars
* Removes cookie banners
* Removes footers
* Removes hidden elements
* Cleans whitespace
* Truncates long content

This significantly reduces token usage.

---

## Output Schema

```json
{
  "website_name": "",
  "company_name": "",
  "address": "",
  "mobile_number": "",
  "mail": [],
  "core_service": "",
  "target_customer": "",
  "probable_pain_point": "",
  "outreach_opener": ""
}
```

---

## Example Result

```json
{
  "website_name": "HMJCA",
  "company_name": "HMJ & COMPANY",
  "address": "No 7, 9th Main, Jayanagar 2nd Block, Bengaluru, 560011",
  "mobile_number": "+91 9663395333",
  "mail": [
    "hari@hmjca.com",
    "mani@hmjca.com"
  ],
  "core_service": "Accounting, auditing, tax planning, GST compliance, and corporate law advisory services.",
  "target_customer": "Businesses and individuals.",
  "probable_pain_point": "Managing compliance and complex tax regulations.",
  "outreach_opener": "Hi, I came across HMJ & COMPANY and was impressed by your comprehensive accounting and compliance services."
}
```

---

## Deployment

### Backend

* Render
* Railway

### Frontend

* Vercel
* Netlify

---

## Author

Sahil Suriya

AI/ML Engineer

Built for the AI & Automation Developer Hackathon.
