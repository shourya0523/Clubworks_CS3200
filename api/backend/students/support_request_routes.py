@students.route('/get_request_types/<nuid>', methods=['GET'])
def get_request_types():
    cursor = db.get_db().cursor()
    query = "SELECT RequestTypeID, RequestType FROM RequestTypes"
    cursor.execute(query)
    rows = cursor.fetchall()
    types = [{"RequestTypeID": row["RequestTypeID"], "RequestType": row["RequestType"]} for row in rows]
    return make_response(types, 200)

@students.route('/support_request/<nuid>', methods=['GET'])
def support_request():
    current_app.logger.info('PUT /student_routes')
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