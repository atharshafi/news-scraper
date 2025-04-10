from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import SessionLocal, engine
from app.scraper.core import scrape_and_save
from app.scraper.configs import WEBSITE_CONFIGS


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/sites/", response_model=List[str])
def get_available_sites():
    """List all pre-configured websites"""
    return list(WEBSITE_CONFIGS.keys())

@app.post("/scrape/{site_name}")
def scrape_site(site_name: str, db: Session = Depends(get_db)):
    """Scrape articles from a specific website"""
    try:
        articles = scrape_and_save(site_name, db)
        return {"message": f"Successfully scraped {len(articles)} articles from {site_name}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@app.get("/articles/", response_model=List[schemas.Article])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Read all articles from database"""
    return db.query(models.Article).offset(skip).limit(limit).all()

@app.get("/search/", response_model=List[schemas.Article])
def search_articles(q: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Search articles by keyword"""
    return (
        db.query(models.Article)
        .filter(models.Article.title.contains(q) | models.Article.summary.contains(q))
        .offset(skip)
        .limit(limit)
        .all()
    )

# Add this temporary route to inspect problematic articles
@app.get("/debug/articles")
def debug_articles(db: Session = Depends(get_db)):
    return db.query(models.Article).filter(models.Article.title == None).all()