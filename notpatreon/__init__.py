import os
from flask_cors import CORS

from flask import Flask


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.update(
        SECRET_KEY=os.environ['SECRET_KEY'],
        SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URI'],
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    from notpatreon.dbmodels import db, initialize_db
    db.init_app(app)
    initialize_db(app)

    from notpatreon import users
    from notpatreon import projects
    app.register_blueprint(users.users)
    app.register_blueprint(projects.projects)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()