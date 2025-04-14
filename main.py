from app.infrastructure.logger import setup_logger
from app.server.server import run_server

setup_logger()

if __name__ == "__main__":
    run_server()
