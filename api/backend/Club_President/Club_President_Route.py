########################################################
# club_president blueprint of endpoints
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

club_president = Blueprint('club_president', __name__)

@club_president.route('/attendance', methods=['GET'])
def get_attendancecount():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT 
    c.ClubName AS ClubName,
    e.Name AS EventName,
    COUNT(a.NUID) AS AttendanceCount
    FROM Events e
    JOIN Clubs c ON e.ClubId = c.ClubId
    LEFT JOIN Attendance a ON e.EventID = a.EventID
    GROUP BY c.ClubName, e.Name
    ORDER BY AttendanceCount DESC;

    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@club_president.route('/create_event', methods=['PUT'])
def create_club_event():
    current_app.logger.info('PUT /club_president route')
    event_info = request.json
    name = event_info['Name']
    location = event_info['Location']
    start_time = event_info['StartTime']
    end_time = event_info['EndTime']
    club_id = event_info['ClubID']
    event_type_name = event_info['Type']  
    poster_img_link = event_info['PosterImg'] 

    cursor = db.get_db().cursor()
    cursor.execute("SELECT EventTypeID FROM EventTypes WHERE EventType = %s", (event_type_name,))
    result = cursor.fetchone()
    if result is None:
        return make_response(f"Event type '{event_type_name}' not found.", 400)
    event_type_id = result['EventTypeID']

    insert_img_query = "INSERT INTO Images (ImageLink) VALUES (%s)"
    cursor.execute(insert_img_query, (poster_img_link,))
    poster_img_id = cursor.lastrowid  # gets auto-incremented ImageID

    insert_event_query = '''
        INSERT INTO Events (Name, Location, StartTime, EndTime, ClubId, PosterImg, Type)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    event_data = (name, location, start_time, end_time, club_id, poster_img_id, event_type_id)
    cursor.execute(insert_event_query, event_data)
    db.get_db().commit()
    return make_response("Event created successfully!", 200)

@club_president.route('/member_contact_information', methods=['GET'])
def get_member_contact():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT s.FirstName, s.LastName, s.Email, c.ClubName
    FROM Membership m
    JOIN Students s ON m.NUID = s.NUID
    JOIN Clubs c ON m.ClubId = c.ClubId
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@club_president.route('/make_request', methods=['PUT'])
def make_request():
    current_app.logger.info('PUT /club_president route')
    request_info = request.json
    request_id = request_info['RequestID']
    request_description = request_info['RequestDescription']
    status = request_info['Status']
    created_time = request_info['CreatedTime']
    type = request_info['Type']
    executive_id = request_info['ExecutiveID']
    executive_club = request_info['ExecutiveClub']
    executive_position = request_info['ExecutivePosition']

    query = 'INSERT INTO Requests (RequestDescription, Status, CreatedTime, Type, ExecutiveID, ExecutiveClub, ExecutivePosition) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    data = (request_description, status, created_time, type, executive_id, executive_club, executive_position)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'request made!'

@club_president.route('/obtain_anonamous_feedback', methods=['GET'])
def obtain_anonamous_feedback():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT c.ClubName, f.Description, f.Rating
    FROM Feedback f
    JOIN Clubs c ON f.ClubID = c.ClubId
    ORDER BY c.ClubName, f.Rating DESC;

    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@club_president.route('/attendance_by_event_type', methods=['GET'])
def attendance_by_event_type():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT et.EventType, COUNT(a.NUID) AS TotalAttendance, c.ClubName
    FROM Events e
    JOIN EventTypes et ON e.Type = et.EventTypeId
    JOIN Clubs c ON e.ClubId = c.ClubId
    LEFT JOIN Attendance a ON e.EventID = a.EventID
    GROUP BY c.ClubName, et.EventType
    ORDER BY TotalAttendance DESC;

    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@club_president.route('/event_types', methods=['GET'])
def get_event_types():
    cursor = db.get_db().cursor()
    query = "SELECT EventTypeID, EventType FROM EventTypes"
    cursor.execute(query)
    rows = cursor.fetchall()
    types = [{"EventTypeID": row["EventTypeID"], "EventType": row["EventType"]} for row in rows]
    return make_response(types, 200)