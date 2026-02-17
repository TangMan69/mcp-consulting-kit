import httpx
from bs4 import BeautifulSoup

def fetch_html(url: str, timeout: float = 10.0) -> str:
    resp = httpx.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text

def extract_article(url: str) -> dict:
    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")

    title = soup.title.string.strip() if soup.title else None
    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    text = "\n\n".join(paragraphs)

    return {"url": url, "title": title, "text": text}

def extract_links(url: str) -> list[dict]:
    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a in soup.find_all("a", href=True):
        links.append({"text": a.get_text(" ", strip=True), "href": a["href"]})
    return links

def extract_tables(url: str) -> list[list[list[str]]]:
    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")
    tables_data: list[list[list[str]]] = []
    for table in soup.find_all("table"):
        rows_data: list[list[str]] = []
        for row in table.find_all("tr"):
            cells = [c.get_text(" ", strip=True) for c in row.find_all(["th", "td"])]
            if cells:
                rows_data.append(cells)
        if rows_data:
            tables_data.append(rows_data)
    return tables_data
