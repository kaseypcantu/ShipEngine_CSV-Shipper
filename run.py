import os
import logging

from csv_shipper import create_app, load_dotenv, db

load_dotenv()

app = create_app()

if __name__ == "__main__":
    log: logging.Logger = app.logger
    log.setLevel(logging.DEBUG)
    db.create_all()
    app.run(host="127.0.0.1", port=os.getenv("APP_PORT"), debug=True)
