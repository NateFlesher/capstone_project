from flask import Blueprint, request, jsonify




api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata', methods = [])
def getdata():
    return {'some': 'value'}