import requests
from bs4 import BeautifulSoup
import os
import re
import time

SOURCES = [
    ("FIFA World Cup records and statistics", "https://en.wikipedia.org/wiki/FIFA_World_Cup_records_and_statistics"),
    ("History of the FIFA World Cup", "https://en.wikipedia.org/wiki/History_of_the_FIFA_World_Cup"),
    ("FIFA World Cup", "https://en.wikipedia.org/wiki/FIFA_World_Cup"),
    ("List of FIFA World Cup hosts", "https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_hosts"),
    ("List of FIFA World Cup songs and anthems", "https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_songs_and_anthems"),
    ("List of FIFA World Cup finals", "https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals"),
    ("Economics of the FIFA World Cup", "https://en.wikipedia.org/wiki/Economics_of_the_FIFA_World_Cup"),
    ("2026 FIFA World Cup qualification", "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_qualification"),
    ("National team appearances in the FIFA World Cup", "https://en.wikipedia.org/wiki/National_team_appearances_in_the_FIFA_World_Cup"),
    ("List of FIFA World Cup hat-tricks", "https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_hat-tricks"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# ---------------------------
# TEXT CLEANING
# ---------------------------
def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# ---------------------------
# TABLE EXTRACTION (KEY FIX)
# ---------------------------
def extract_tables(soup: BeautifulSoup) -> str:
    tables_text = []

    for table in soup.find_all("table"):
        rows = []
        for tr in table.find_all("tr"):
            cols = tr.find_all(["td", "th"])
            cols = [c.get_text(" ", strip=True) for c in cols]

            if len(cols) >= 2:
                rows.append(" | ".join(cols))

        if rows:
            tables_text.append("\n".join(rows))

    return "\n\n".join(tables_text)


# ---------------------------
# HEADING EXTRACTION
# ---------------------------
def extract_headings(soup: BeautifulSoup) -> str:
    headings = []
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(strip=True)
        if text and len(text) > 2:
            headings.append(f"\n# {text}\n")
    return "\n".join(headings)


# ---------------------------
# MAIN SCRAPER
# ---------------------------
def scrape_url(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    # remove junk
    for tag in soup(["script", "style", "noscript", "footer", "nav", "header"]):
        tag.decompose()

    # remove obvious UI blocks
    for tag in soup.find_all(["div", "section"], class_=re.compile(
        r"nav|footer|sidebar|ad|cookie|popup|modal|menu|breadcrumb"
    )):
        tag.decompose()

    # extract structured parts FIRST
    headings = extract_headings(soup)
    tables = extract_tables(soup)

    # extract remaining text
    body_text = soup.get_text("\n")

    # basic cleaning (no aggressive filtering)
    body_text = clean_text(body_text)

    # combine in priority order
    full_text = f"""
HEADINGS:
{headings}

TABLES:
{tables}

BODY:
{body_text}
"""

    return clean_text(full_text)


# ---------------------------
# SAVE
# ---------------------------
def save_document(title: str, content: str, output_dir: str):
    if len(content) < 100:
        return False

    filename = re.sub(r"[^a-zA-Z0-9\s]", "", title)
    filename = re.sub(r"\s+", "_", filename)[:60] + ".txt"

    path = os.path.join(output_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return True


# ---------------------------
# MAIN
# ---------------------------
def main():
    os.makedirs("documents", exist_ok=True)

    print("=" * 60)
    print("RAG-READY SCRAPER (FIXED VERSION)")
    print("=" * 60)

    success = 0

    for title, url in SOURCES:
        print(f"\nScraping: {title}")

        try:
            text = scrape_url(url)

            if save_document(title, text, "documents"):
                print(f"✓ Saved ({len(text)} chars)")
                success += 1
            else:
                print("✗ Too little content")

        except Exception as e:
            print(f"✗ Error: {e}")

        time.sleep(1)

    print("\n" + "=" * 60)
    print(f"Done: {success}/{len(SOURCES)} sources saved")
    print("=" * 60)


if __name__ == "__main__":
    main()