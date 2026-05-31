import os
from dotenv import load_dotenv
from langchain.tools import tool
import requests
from tavily import TavilyClient
from rich import print
from bs4 import BeautifulSoup
from readability import Document
import re
import trafilatura


load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

tavily = TavilyClient(api_key=api_key)


def clean_llm_payload(text: str) -> str:
    """
    Cleans raw web strings to prevent API schema/function-calling validation errors.
    Strips markdown links, brackets, and structural tokens that break Llama models.
    """
    if not text or not isinstance(text, str):
        return ""

    # 1. Convert markdown links [Text](URL) -> to just 'Text'
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    # 2. Strip structural Markdown header elements (#, ##, etc.)
    text = re.sub(r"#+\s+", "", text)

    # 3. Strip structural curly and square brackets which break JSON payloads
    text = re.sub(r"[{}\[\]\"]", "", text)

    # 4. Normalize spacing and remove internal escaped line breaks
    text = text.replace("\\n", " ").replace("\n", " ")
    text = " ".join(text.split())

    return text


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""
    results = tavily.search(query=query, max_results=5)

    out = []

    for r in results["results"]:
        # We sanitize the snippet content right here
        safe_snippet = clean_llm_payload(r["content"][:300])

        out.append(f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {safe_snippet}\n")

    return "\n----\n".join(out)


@tool
def scrape_url(url: str) -> str:
    """
    Scrape and extract clean readable content from a URL.
    Uses multiple extraction strategies for better reliability.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    try:
        # ── Fetch page ─────────────────────────────────────
        response = requests.get(url, headers=headers, timeout=15)

        response.raise_for_status()

        html = response.text

        # ──────────────────────────────────────────────────
        # Strategy 1 → trafilatura (BEST for articles/blogs)
        # ──────────────────────────────────────────────────
        extracted = trafilatura.extract(
            html, include_comments=False, include_tables=False
        )

        if extracted and len(extracted.strip()) > 200:
            cleaned = re.sub(r"\s+", " ", extracted)
            return cleaned[:5000]

        # ──────────────────────────────────────────────────
        # Strategy 2 → readability
        # ──────────────────────────────────────────────────
        doc = Document(html)
        clean_html = doc.summary()

        soup = BeautifulSoup(clean_html, "html.parser")

        for tag in soup(
            ["script", "style", "nav", "footer", "header", "aside", "form"]
        ):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        if text and len(text.strip()) > 200:
            cleaned = re.sub(r"\s+", " ", text)
            return cleaned[:5000]

        # ──────────────────────────────────────────────────
        # Strategy 3 → fallback full page extraction
        # ──────────────────────────────────────────────────
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(
            ["script", "style", "nav", "footer", "header", "aside", "form"]
        ):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        cleaned = re.sub(r"\s+", " ", text)

        if cleaned:
            return cleaned[:5000]

        return "Could not extract meaningful content from the page."

    except requests.exceptions.Timeout:
        return "Request timed out while scraping the URL."

    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {str(e)}"

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
