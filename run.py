from app.scheduler.tweet_scheduler import TweetScheduler
from fastapi import FastAPI
from app.api.routes import router
import uvicorn
import threading

app = FastAPI(title="SEI Agent")
app.include_router(router)

def run_scheduler():
    scheduler = TweetScheduler()
    scheduler.start()

if __name__ == "__main__":
    # Start scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    # Run the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=8000) 