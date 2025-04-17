from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

support_req = Blueprint('support_requests', __name__)

@support_req.route('/make_support_request', methods=['PUT'])
def make_support_request():
    current_app.logger.info('PUT /support_req route')
    s_request_info = s_request_info.json
    s_request_id = s_request_info['RequestID']
    s_request_description = s_request_info['RequestDescription']
    s_type = s_request_info['Type']
    query = 'INSERT INTO SupportRequests (SupportRequestType, SupportRequestDescription) VALUES (%s, %s)'
    data = (s_request_id, s_request_description, s_type)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'request made!'


@support_req.route('/support_request_types', methods=['GET'])
def get_s_request_types():
    cursor = db.get_db().cursor()
    query = "SELECT SupportTypeID, SupportType FROM SupportTypes" 
    cursor.execute(query)
    rows = cursor.fetchall()
    types = [{"SupportTypeID": row["SupportTypeID"], "SupportType": row["SupportType"]} for row in rows]
    return make_response(types, 200)