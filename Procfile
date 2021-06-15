web: cd backend/app/ && uvicorn backend.app.main:app --host=0.0.0.0 --port=$PORT
worker: cd backend/app/ && chmod +x start_workers.sh && ./start_workers.sh
scheduler: cd backend/app/ && chmod +x start_scheduler.sh && ./start_scheduler.sh