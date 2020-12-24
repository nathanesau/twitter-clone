from flask import jsonify, request, url_for, abort
from flasgger import swag_from
from app import db
from app.models import User
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
@swag_from('docs/get_user.yml')
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users/', methods=['GET'])
@token_auth.login_required
@swag_from('docs/get_users.yml')
def get_users():
    data = User.query.all()
    return jsonify([user.to_dict() for user in data])


@bp.route('/users/<int:id>/followers', methods=['GET'])
@token_auth.login_required
@swag_from('docs/get_followers.yml')
def get_followers(id):
    user = User.query.get_or_404(id)
    followers = user.followers.all()
    return jsonify([user.to_dict() for user in followers])


@bp.route('/users/<int:id>/followed', methods=['GET'])
@token_auth.login_required
@swag_from('docs/get_followed.yml')
def get_followed(id):
    user = User.query.get_or_404(id)
    followed = user.followed.all()
    return jsonify([user.to_dict() for user in followed])


@bp.route('/users', methods=['POST'])
@swag_from('docs/create_user.yml')
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a differetn email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
@swag_from('docs/update_user.yml')
def update_user(id):
    if token_auth.current_user().id != id:
        abort(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())
