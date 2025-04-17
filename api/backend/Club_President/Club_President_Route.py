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
import pymysql.cursors

club_president = Blueprint('club_president', __name__)

@club_president.route('/attendance/<clubid>', methods=['GET'])
def get_attendancecount(clubid):

    cursor = db.get_db().cursor()
    the_query = f'''
    SELECT 
    c.ClubName AS ClubName,
    e.Name AS EventName,
    COUNT(a.NUID) AS AttendanceCount
    FROM Events e
    JOIN Clubs c ON e.ClubId = c.ClubId
    LEFT JOIN Attendance a ON e.EventID = a.EventID
    WHERE c.ClubId = {clubid}
    GROUP BY c.ClubName, e.Name
    ORDER BY AttendanceCount DESC;

    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@club_president.route('/create_event', methods=['POST'])
def create_club_event():
    current_app.logger.info('POST /club_president route')
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

@club_president.route('/member_contact_information/<clubid>', methods=['GET'])
def get_member_contact(clubid):

    cursor = db.get_db().cursor()
    the_query = f'''
    SELECT s.FirstName, s.LastName, s.Email, c.ClubName
    FROM Membership m
    JOIN Students s ON m.NUID = s.NUID
    JOIN Clubs c ON m.ClubId = c.ClubId
    WHERE c.ClubId = {clubid}
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

@club_president.route('/obtain_anonamous_feedback/<clubid>', methods=['GET'])
def obtain_anonamous_feedback(clubid):

    cursor = db.get_db().cursor()
    the_query = f'''
    SELECT c.ClubName, f.Description, f.Rating
    FROM Feedback f
    JOIN Clubs c ON f.ClubID = c.ClubId
    WHERE c.ClubId = {clubid}
    ORDER BY c.ClubName, f.Rating DESC;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@club_president.route('/attendance_by_event_type/<clubid>', methods=['GET'])
def attendance_by_event_type(clubid):

    cursor = db.get_db().cursor()
    the_query = f'''
    SELECT et.EventType, COUNT(a.NUID) AS TotalAttendance, c.ClubName
    FROM Events e
    JOIN EventTypes et ON e.Type = et.EventTypeId
    JOIN Clubs c ON e.ClubId = c.ClubId
    LEFT JOIN Attendance a ON e.EventID = a.EventID
    WHERE c.Clubid = {clubid}
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

@club_president.route('/profile/<nuid>', methods =['GET'])
def exec_profile(nuid):
    cursor = db.get_db().cursor()
    query = f'''
    SELECT c.ClubId, s.FirstName, c.ClubName,
    GROUP_CONCAT(ex.Position SEPARATOR ', ') AS Positions
    FROM Clubs c
    JOIN Executives ex ON c.ClubId = ex.ClubID
    JOIN Students s ON s.NUID = ex.NUID
    WHERE  s.NUID = {nuid}
    GROUP BY 
        s.NUID, c.ClubId, s.FirstName, c.ClubName;

    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    response = make_response(jsonify(rows))
    response.status_code = 200
    return response

@club_president.route('/event/<int:clubid>', methods=['GET'])
def get_event_by_name(clubid):

    cursor = db.get_db().cursor(pymysql.cursors.DictCursor)
    query = '''
        SELECT e.EventID, e.Name, e.Location, e.StartTime, e.EndTime,
               i.ImageLink AS PosterImgLink, et.EventType
        FROM   Events e
        JOIN   EventTypes et ON e.Type = et.EventTypeID
        JOIN   Images     i  ON e.PosterImg = i.ImageID
        WHERE  e.ClubId = %s
        LIMIT  1
    '''
    cursor.execute(query, (clubid,))
    row = cursor.fetchone()
    if not row:
        return make_response("Event not found.", 404)
    return make_response(jsonify(row), 200)

@club_president.route('/edit_event/<int:eventid>', methods=['PUT'])
def edit_event(eventid):
    info = request.json
    name        = info['Name']
    location    = info['Location']
    start_time  = info['StartTime']
    end_time    = info['EndTime']
    event_type  = info['Type']
    poster_link = info['PosterImg']

    cursor = db.get_db().cursor()

    # translate event‑type name ► id
    cursor.execute(
        "SELECT EventTypeID FROM EventTypes WHERE EventType = %s",
        (event_type,)
    )
    row = cursor.fetchone()
    if not row:
        return make_response(f"Event type '{event_type}' not found.", 400)
    event_type_id = row['EventTypeID']

    # store / update poster image (new row each time for simplicity)
    cursor.execute("INSERT INTO Images (ImageLink) VALUES (%s)", (poster_link,))
    new_img_id = cursor.lastrowid

    update_q = '''
        UPDATE Events
        SET    Name=%s, Location=%s, StartTime=%s, EndTime=%s,
               Type=%s, PosterImg=%s
        WHERE  EventID=%s
    '''
    data = (name, location, start_time, end_time, event_type_id, new_img_id, eventid)
    cursor.execute(update_q, data)
    db.get_db().commit()
    return make_response("Event updated successfully!", 200)

@club_president.route('/events/<int:clubid>', methods=['GET'])
def list_events(clubid):
    """Return EventID and Name for every event in this club."""
    cursor = db.get_db().cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT EventID, Name FROM Events WHERE ClubId = %s ORDER BY StartTime DESC",
        (clubid,)
    )
    return make_response(jsonify(cursor.fetchall()), 200)