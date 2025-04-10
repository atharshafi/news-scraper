from sqlalchemy.orm import Session
from app import models

def get_articles(db: Session):
    return db.query(models.Article).all()

def search_articles(db: Session, keyword: str):
    return db.query(models.Article).filter(models.Article.title.contains(keyword)).all()

def add_article(db: Session, article_data):
    db_article = models.Article(**article_data)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article
