import requests
import json
import re
import time
import ast
import google.genai as genai
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from rapidfuzz import fuzz
import google.generativeai as genai


API_KEY = "AIzaSyC2wmMXMPVmsIjMBLqGhl3nqOZT8VkdMB8"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-3.5-flash")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

TARGET_PAGE_KEYWORDS = [
    "about",
    "about-us",
    "contact",
    "contact-us",
    "services",
    "solutions",
    "products",
    "team",
    "leadership"
]

EMPTY_PROFILE = {
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

def normalize_url(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def fetch_page(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            return r.text
    except:
        pass
    return None


def extract_links(base_url, html):

    soup = BeautifulSoup(html, "lxml")

    domain = urlparse(base_url).netloc

    links = []

    for a in soup.find_all("a", href=True):

        full = urljoin(base_url, a["href"])

        if urlparse(full).netloc == domain:
            links.append(full)

    return list(set(links))


def score_url(url):

    path = urlparse(url).path.lower()

    best = 0

    for keyword in TARGET_PAGE_KEYWORDS:

        score = fuzz.partial_ratio(keyword, path)

        best = max(best, score)

    return best


def clean_html(html):

    soup = BeautifulSoup(html, "lxml")

    for tag in soup(
        [
            "script",
            "style",
            "header",
            "footer",
            "nav",
            "form",
            "svg",
            "img"
        ]
    ):
        tag.decompose()

    text = soup.get_text("\n")

    lines = [x.strip() for x in text.splitlines()]

    lines = [x for x in lines if len(x) > 20]

    return "\n".join(lines)


def extract_emails(text):

    emails = re.findall(
        r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
        text
    )

    return list(set(emails))


def extract_phone(text):

    patterns = [
        r"\+[\d\s\-\(\)]{7,20}",
        r"\d{10,13}"
    ]

    for p in patterns:

        m = re.search(p, text)

        if m:
            return m.group()

    return ""

SYSTEM_PROMPT = """
Extract company information.

Rules:

1. Use ONLY website text.
2. Never hallucinate.
3. Missing values = empty string.
4. Emails must exist in text.
5. Phone must exist in text.

Return ONLY JSON:

{
  "website_name":"",
  "company_name":"",
  "address":"",
  "mobile_number":"",
  "mail":[],
  "core_service":"",
  "target_customer":"",
  "probable_pain_point":"",
  "outreach_opener":""
}
"""


def enrich_company(url: str):

    result = EMPTY_PROFILE.copy()

    try:

        url = normalize_url(url)

        homepage = fetch_page(url)

        if not homepage:
            return result

        links = extract_links(url, homepage)

        links = sorted(
            links,
            key=score_url,
            reverse=True
        )[:4]

        pages = [url] + links

        text_parts = []

        for page in pages:

            html = fetch_page(page)

            if html:

                text_parts.append(
                    clean_html(html)
                )

        scraped_text = "\n".join(text_parts)

        emails = extract_emails(scraped_text)

        phone = extract_phone(scraped_text)

        prompt = f"""
{SYSTEM_PROMPT}

Website URL:
{url}

Website Content:
{scraped_text[:8000]}
"""

        response = model.generate_content(prompt)

        raw = response.text.strip()

        raw = raw.replace("```json", "")
        raw = raw.replace("```", "")

        profile = json.loads(raw)

        result.update(profile)

        if not result["mail"]:
            result["mail"] = emails[:3]

        if not result["mobile_number"]:
            result["mobile_number"] = phone

        return result

    except Exception as e:

        print(e)

        return result
    
# ========= 9. MAIN EXECUTION =========
if __name__ == "__main__":

    urls = json.loads(
        input(
            'Enter URLs JSON array: '
        )
    )

    results = []

    for url in urls:
        try:
            data = enrich_company(url)
            results.append(data)

        except Exception as e:
            print(f"Error processing {url}: {e}")

    with open(
        "results.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("\n=== FINAL OUTPUT ===\n")

    print(
        json.dumps(
            results,
            indent=2,
            ensure_ascii=False
        )
    )