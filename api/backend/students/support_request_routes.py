@students.route('/get_request_types/<nuid>', methods=['GET'])
def get_request_types(nuid):
    cursor = db.get_db().cursor()
    query = "SELECT RequestTypeID, RequestType FROM RequestTypes"
    cursor.execute(query)
    rows = cursor.fetchall()
    types = [{"RequestTypeID": row["RequestTypeID"], "RequestType": row["RequestType"]} for row in rows]
    return make_response(types, 200)

@students.route('/support_request/<nuid>', methods=['POST'])
def support_request(nuid):
    current_app.logger.info('POST /support_request')
    s_request_info = request.get_json()
    s_type = s_request_info['Type']
    s_request_description = s_request_info['RequestDescription']

    query = '''
        INSERT INTO SupportRequests (NUID, SupportRequestType, SupportRequestDescription)
        VALUES (%s, %s, %s)
    '''
    data = (nuid, s_type, s_request_description)

    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()

    return make_response({'message': 'Request submitted successfully!'}, 200)
