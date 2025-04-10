# Pre-configured website selectors
WEBSITE_CONFIGS = {
    "sciencedaily": {
        "name": "Science Daily",
        "base_url": "https://www.sciencedaily.com/news/computers_math/artificial_intelligence/",
        "selectors": {
            "article_container": "div.tab-pane.active div.latest-head",
            "title": "a",
            "url": "a",
            "summary": "div.latest-summary",
            "date": None,
            "image": None
        },
        "url_prefix": "https://www.sciencedaily.com",
        "requires_js": False
    },

"arxiv": {
    "name": "Arxiv AI",
    "base_url": "https://arxiv.org/list/cs.AI/recent",
    "selectors": {
        "article_container": "li.arxiv-result",  # Changed from dl.arxiv
        "title": "p.title.is-5.mathjax",  # Updated selector
        "url": "a[href*='/abs/']",  # More specific URL selector
        "summary": "p.abstract.mathjax",
        "authors": "p.authors",
        "date": "p.is-size-7"
    },
    "url_prefix": "https://arxiv.org",
    "requires_js": False
},

    "techcrunch": {
    "name": "TechCrunch AI",
    "base_url": "https://techcrunch.com/category/artificial-intelligence/",
    "selectors": {
        "article_container": "div.loop-card",  # Updated container
        "title": "h3.loop-card__title a",  # Updated
        "url": "h3.loop-card__title a",  # Updated
        "summary": "div.loop-card-excerpt",  # May need adjustment
        "date": "time.loop-card__date"
    },
    "url_prefix": "",
    "requires_js": False
},
    "wired": {
    "name": "Wired AI",
    "base_url": "https://www.wired.com/tag/artificial-intelligence/",
    "selectors": {
        "article_container": "div[class*='SummaryItemContent']",
        "title": "h3[class*='SummaryItemHed']",  # Updated
        "url": "a[class*='SummaryItemHedLink']",
        "summary": "p[class*='SummaryItemDeck']",
        "date": "time"
    },
    "url_prefix": "https://www.wired.com",
    "requires_js": False
},

    "towards_ai": {
        "name": "Towards AI",
        "base_url": "https://towardsdatascience.com/tagged/artificial-intelligence",
        "selectors": {
            "article_container": "article",
            "title": "h3 a",
            "url": "h3 a",
            "summary": "div.ef > div",
            "date": "span[datetime]",
            "author": "a[href*='/authors/']"
        },
        "url_prefix": "https://towardsdatascience.com",
        "requires_js": True  # Changed to True
    }
}