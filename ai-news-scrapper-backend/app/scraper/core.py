import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models import Article
from app.database import SessionLocal

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


class Scraper:
    def __init__(self, config: Dict):
        self.config = config
        self.base_url = config["base_url"]
        self.selectors = config["selectors"]
        self.url_prefix = config.get("url_prefix", "")

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"Error fetching page: {str(e)}")
            return None

    def extract_articles(self, soup: BeautifulSoup) -> List[Dict]:
        articles = []
        containers = soup.select(self.selectors["article_container"])

        for container in containers:
            try:
                article = {
                    "title": self._extract_text(container, self.selectors["title"]),
                    "url": self._extract_url(container, self.selectors["url"]),
                    "summary": self._extract_text(container, self.selectors.get("summary")),
                    "date": self._extract_text(container, self.selectors.get("date")),
                    "source": self.config["name"]
                }
                articles.append(article)
            except Exception as e:
                print(f"Error extracting article: {str(e)}")
                continue

        return articles

    def _extract_text(self, container, selector: Optional[str]) -> Optional[str]:
        if not selector:
            return None
        element = container.select_one(selector)
        return element.get_text(strip=True) if element else None

    def _extract_url(self, container, selector: Optional[str]) -> Optional[str]:
        if not selector:
            return None
        element = container.select_one(selector)
        if not element or not element.get("href"):
            return None
        url = element["href"]
        return self.url_prefix + url if self.url_prefix and not url.startswith("http") else url


def scrape_and_save(site_name: str, db: Session = SessionLocal()):
    from app.scraper.configs import WEBSITE_CONFIGS
    config = WEBSITE_CONFIGS.get(site_name)

    if not config:
        raise ValueError(f"No configuration found for {site_name}")

    scraper = Scraper(config)
    soup = scraper.fetch_page(config["base_url"])
    if not soup:
        return []

    articles = scraper.extract_articles(soup)

    # Save to database
    for article_data in articles:
        db_article = Article(**article_data)
        db.add(db_article)

    db.commit()
    return articles