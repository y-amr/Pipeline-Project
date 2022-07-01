import logging

from app import app
from app.Base import init_db

if __name__ == "__main__":
    init_db()
    logging.info("URL du serveur : http://127.0.0.1:%s", app.config['SERVER_PORT'])
    app.run(threaded=True, port=app.config['SERVER_PORT'])
