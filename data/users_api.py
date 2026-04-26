import flask
from flask import jsonify, make_response
from data import db_session
from data.users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__
)


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'user': {
                'id': user.id,
                'surname': user.surname,
                'name': user.name,
                'city_from': user.city_from
            }
        }
    )