import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Habit Tracker API (dev)")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Habit Tracker API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
