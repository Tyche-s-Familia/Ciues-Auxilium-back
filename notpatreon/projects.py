from flask import Blueprint, jsonify, request

from .dbmodels import db, User, Project

projects = Blueprint('/projects', __name__, url_prefix='/projects')


@projects.route('/', methods=['POST'])
def create_project():
    current_user = User.query.filter_by(id=1).first()
    try:
        new_project = Project(
            name=request.json['name'],
            authors=[current_user]
        )
    except KeyError:
        return {'message': 'You must provide a project name'}
    db.session.add(new_project)
    db.session.commit()
    return jsonify(new_project.serialize())
