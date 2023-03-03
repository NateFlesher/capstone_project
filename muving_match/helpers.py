from functools import wraps
from muving_match.models import db, User, CustomerProfile, MuverProfile

import secrets
from flask import request, jsonify, json

from muving_match.models import User

import decimal
import requests

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['a-access-token'].split(' ')[1]

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            our_user = User.query.filter_by(id = id).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is invalid'})

        except:
            owner = User.query.fileter_by(token=token).first()
            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid'})

        return our_flask_function(our_user, *args, **kwargs)
    return decorated


def get_user_location(user_id, is_muver):
    if is_muver == True:
        print('Getting muver profile')
        user_profile = MuverProfile.query.filter_by(user_id=user_id).first()
    else:
        print('Getting customer profile')
        user_profile = CustomerProfile.query.filter_by(user_id=user_id).first()

    print(user_profile)

    if not user_profile:
        return {'zip_code': 90210, 'latitude': 34.1030032, 'longitude': -118.4104684}
    zip_code = user_profile.zip_code
    response = requests.get(f'https://nominatim.openstreetmap.org/search?q={zip_code}&format=json')
    data = response.json()
    latitude = data[0]['lat']
    longitude = data[0]['lon']
    print(latitude)
    print(longitude)

    return {'zip_code': zip_code, 'latitude': latitude, 'longitude': longitude}

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default






# <h2>Change Email</h2>
#   <form method="POST" action="{{ url_for('site.change_email') }}">
#     <label for="email">New Email:</label>
#     <input type="email" id="email" name="email" required>
#     <br><br>
#     <button type="submit" class="btn btn-primary">Change Email</button>
#   </form>

#   <h2>Change Password</h2>
#   <form method="POST" action="{{ url_for('site.change_password') }}">
#     <label for="password">New Password:</label>
#     <input type="password" id="password" name="password" required>
#     <br><br>
#     <label for="confirm_password">Confirm Password:</label>
#     <input type="password" id="confirm_password" name="confirm_password" required>
#     <br><br>
#     <button type="submit" class="btn btn-primary">Change Password</button>
#   </form>