from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def initialize_db(app):
    @app.cli.command('initialize-db')
    def initialize():
        print(
            'WARNING: THIS WILL DELETE ALL CURRENTLY'
            ' EXISTING TABLES FROM THE DATABASE.'
        )
        print('Press ENTER to continue')
        input()
        db.drop_all()
        db.create_all()


project_supporters = db.Table(
    'project_supporters',
    db.Column(
        'user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True
    ),
    db.Column(
        'project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True
    )
)

project_authors = db.Table(
    'project_authors',
    db.Column(
        'user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True
    ),
    db.Column(
        'project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True
    )
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(999), unique=True, nullable=False)
    email = db.Column(db.String(999), unique=True, nullable=False)
    hash = db.Column(db.String(999), nullable=False)
    # image_url =db.Column(db.String(999), nullable=True, default=None)
    # credits = db.Column(db.Integer, default=0)
    # bio = db.Column(db.Text(), default=None)
    projects_created = db.relationship(
        'Project',
        secondary=project_authors,
        lazy='subquery'
    )
    projects_supporting = db.relationship(
        'Project',
        secondary=project_supporters,
        lazy='subquery'
    )
    
    # projects_created = db.relationship('Project', backref='author', lazy=True)

    def __repr__(self):
        return f'User {self.id} - ({self.username} -- {self.email})'

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'projects_created': [
                project.id for project in self.projects_created
            ]
        }


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(999), unique=True, nullable=False)
    description = db.Column(db.Text())
    # image_url =db.Column(db.String(999), nullable=True, default=None)

    authors = db.relationship(
        'User',
        secondary=project_authors,
        lazy='subquery'
    )
    supporters = db.relationship(
        'User',
        secondary=project_supporters,
        lazy='subquery'
    )

    def __repr__(self):
        return f'Project {self.id} - ({self.name} -- {self.authors})'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description':self.description,
            # 'image_url':self.image_url,
            'author_id': self.authors[0].id
        }
