import uvicorn
from app.infrastructure.logger import setup_logger
from app.app import app

setup_logger()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)