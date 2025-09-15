from apscheduler.schedulers.blocking import BlockingScheduler
from agents.fetch_news_agent import fetch_news
from agents.emotion_extraction_agent import extract_emotions
from agents.embedding_agent import create_embeddings


fetch_news()

scheduler = BlockingScheduler()
scheduler.add_job(fetch_news, "interval", hours=24)
scheduler.add_job(extract_emotions, "interval", hours=24)
scheduler.add_job(create_embeddings, "interval", hours=24)

scheduler.start()
