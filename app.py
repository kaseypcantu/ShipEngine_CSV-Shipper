import os
from dataclasses import dataclass

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from dotenv import load_dotenv
from markupsafe import escape
# from typing import Optional, List, Dict

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_DB_URL')

db = SQLAlchemy(app)
db_session = db.session


def db_add(obj):
    db_session.add(obj)
    return db_session.commit()


def db_rm(obj):
    db_session.remove(obj)
    return db_session.commit()


@dataclass
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    pw_hash = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), default=func.now(), server_default=func.now()
    )

    # x = datetime.datetime.now()  |  x.strftime('- %a %b[%m]-%d-%Y @ %I:%M:%S %p -')

    #  [EXAMPLE]: usage of __init__(self) on a given class
    # def __init__(self, first_name: str, last_name: str,
    #              email: str, username: str, pw_hash: str):
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.email = email
    #     self.username = username
    #     self.pw_hash = pw_hash

    @property
    def __repr__(self):
        return f'<User {self.username}>'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/user/<string:username>", methods=['GET'])
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404(
        description=f"There is no data with the username: {escape(username)}"
    )
    return render_template("show_user.html", user=user)


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port='9999',
        debug=True
    )
