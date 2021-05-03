from flask import Blueprint, jsonify, request 
from flask import session as ses
import bcrypt


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


@users.route('/register', methods=['POST'])
def create_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    
    if not username:
        return 'Missing username', 400
    if not email:
        return 'Missing email', 400
    if not password:
        return 'Missing password', 400
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    new_user = User(username=username, email=email, hash=hashed.decode('utf-8'))
    
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize())

@users.route('/login', methods=['POST'])
def login_user():
    email = request.json['email']
    password = request.json['password']
    
    if not email:
        return 'Missing email', 400
    if not password:
        return 'Missing password', 400
    
    user = User.query.filter_by(email=email).first()
    if user is None:
        return {'message': 'Requested user does not exist!'}

    if bcrypt.checkpw(password.encode('utf-8'), user.hash.encode('utf-8')):
        ses['user_id'] = user.id
        return f'Welcome back {email}'
    else:
        return 'Wrong password!'

@users.route('/logout')
def log_out():

    ses.pop('user_id')
    return 'Logged out'

# @users.route('/edit/<int:user_id>', methods=['GET','POST'])
# def edit_user(user_id):
#     user = User.query.filter_by(id=user_id).first()
#     if user is None:
#         return {'message': 'Requested user does not exist!'}
#     if 'user_id' not in ses:
#         return {'message': 'Please login'}
#     if ses['user_id'] != user_id:
#         return {'message': "can't edit other users"}
#     if ses['user_id'] == user_id:


#         user.image_url = request.json['image_url']
#         user.credits = request.json['credits']
   

    
    
#         db.session.merge(user)
#         db.session.commit()
#         return "merged"