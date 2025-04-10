import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.models import Article

# Configure headers to mimic a real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}


def save_articles_to_db(db: Session, articles: list):
    """Save the scraped articles to the database."""
    for article in articles:
        # Check if article already exists
        exists = db.query(Article).filter(Article.url == article["url"]).first()
        if not exists:
            db_article = Article(
                title=article["title"],
                url=article["url"],
                summary=article.get("summary"),
                date=article.get("date"),
                source=article.get("source", "unknown")
            )
            db.add(db_article)
    db.commit()


def scrape_sciencedaily():
    """Scrape AI news from ScienceDaily"""
    url = "https://www.sciencedaily.com/news/computers_math/artificial_intelligence/"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []

        for block in soup.select("div.tab-pane.active div.latest-head"):
            title_tag = block.find("a")
            if not title_tag:
                continue

            summary_tag = block.find_next_sibling("div", class_="latest-summary")

            articles.append({
                "title": title_tag.get_text(strip=True),
                "url": "https://www.sciencedaily.com" + title_tag["href"],
                "summary": summary_tag.get_text(strip=True) if summary_tag else "No summary available",
                "source": "ScienceDaily"
            })

        return articles

    except Exception as e:
        print(f"ScienceDaily scraping error: {str(e)}")
        return []


def scrape_mit_tech_review():
    """Scrape AI news from MIT Technology Review"""
    url = "https://www.technologyreview.com/category/artificial-intelligence/"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []

        for block in soup.select("div.teaserItem"):
            title_tag = block.select_one("h3 a")
            if not title_tag:
                continue

            summary_tag = block.select_one("p.teaserItem__excerpt")
            url = title_tag["href"]
            if not url.startswith("http"):
                url = "https://www.technologyreview.com" + url

            articles.append({
                "title": title_tag.get_text(strip=True),
                "url": url,
                "summary": summary_tag.get_text(strip=True) if summary_tag else "No summary available",
                "source": "MIT Technology Review"
            })

        return articles

    except Exception as e:
        print(f"MIT Tech Review scraping error: {str(e)}")
        return []


def scrape_ai_news(db: Session):
    """Main function to scrape from all sources"""
    all_articles = []

    # Scrape from ScienceDaily
    science_daily_articles = scrape_sciencedaily()
    all_articles.extend(science_daily_articles)

    # Scrape from MIT Tech Review
    mit_articles = scrape_mit_tech_review()
    all_articles.extend(mit_articles)

    # Save to database
    if all_articles:
        save_articles_to_db(db, all_articles)
        print(f"Successfully saved {len(all_articles)} articles to database")
    else:
        print("No articles were scraped")

    return all_articles