from flask import Blueprint, jsonify, request

from .dbmodels import db, User

users = Blueprint('/users', __name__, url_prefix='/users')


@users.route('/', methods=['GET'])
def get_users():
    print(User.query.all())
    users = [user.serialize() for user in User.query.all()]
    return jsonify(users)


@users.route('/<int:user_id>')
def get_user_info(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return {'message': 'Requested user does not exist!'}
    return jsonify(user.serialize())


@users.route('/', methods=['POST'])
def create_user():
    try:
        new_user = User(
            username=request.json['username'], email=request.json['email']
        )
    except KeyError:
        return {'message': 'You must provide a username and email address'}
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize())
