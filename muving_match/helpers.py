from functools import wraps
from muving_match.models import db, User, CustomerProfile

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


# def get_user_location(id):
#     query = db.session.query(CustomerProfile.zip_code)
#     if not query:
#         return None

#     zip_code = query[0]
#     response = requests.get(f'https://nominatim.openstreetmap.org/search?q={zip_code}&format=json')
#     data = response.json()
#     latitude = data[0]['lat']
#     longitude = data[0]['lon']

#     return {'zip_code': zip_code, 'latitude': latitude, 'longitude': longitude}

    # @site.route('/')
# def home():
#     # Get the user's zip code from the database
#     customer_profile = CustomerProfile.query.filter_by(user_id=current_user.id).first()
#     customer_id = customer_profile.customer_id
#     user_zipcode = get_user_location(customer_id)
#     print(user_zipcode)
    
#     # Create a Map object centered on the user's zip code
#     mymap = Map(
#         identifier="mymap",
#         lat=user_zipcode.latitude,
#         lng=user_zipcode.longitude,
#         zoom=12,
#         style="height:500px;width:100%;",
#         markers=[(user_zipcode.lat, user_zipcode.lng)]
#     )


#     # Render the template with the map
#     return render_template('index.html', mymap=mymap, GOOGLEMAPS_APIKEY=current_app.config['GOOGLEMAPS_API_KEY'])

#   <!-- <div id="map">{{mymap.html}}</div> -->


# {% block scripts %}
#   {{mymap.js}}
# {% endblock %} -->





class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default