import re
from flask import Blueprint, jsonify, request
from flask import session as ses

from .dbmodels import db, User, Project

projects = Blueprint('/projects', __name__, url_prefix='/projects')

@projects.route('/', methods=['GET'])
def get_projects():
    print(Project.query.all())
    projects = [project.serialize() for project in Project.query.all()]
    return jsonify(projects)


@projects.route('/', methods=['POST'])
def create_project():
    user_id = ses.get('user_id')
    print(user_id)
    current_user = User.query.filter_by(id = user_id).first()
    try:
        new_project = Project(
            name=request.json['name'],
            authors=[current_user],
            description=request.json['description']
        )
    except KeyError:
        return {'message': 'You must provide a project name'}
    db.session.add(new_project)
    db.session.commit()
    return jsonify(new_project.serialize())
