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

#------------------------------------------------------------
# Creating a new Blueprint object, which is a collection of 
# routes.
club_president = Blueprint('club_president', __name__)

#------------------------------------------------------------
# Get all Attendance from the system
@club_president.route('/attendance', methods=['GET'])
def get_attendancecount():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT e.Name AS EventName, COUNT(a.NUID) AS AttendanceCount
    FROM Events e
    LEFT JOIN Attendance a ON e.EventID = a.EventID
    WHERE e.ClubId = 2 -- Replace with Tyla's ClubID (2 for Business Society)
    GROUP BY e.Name
    ORDER BY AttendanceCount DESC;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response(theData)

#------------------------------------------------------------
# Insert events info for events with particular EventID
@club_president.route('/create_event', methods=['PUT'])
def create_club_event():
    current_app.logger.info('PUT /club_president route')
    event_info = request.json
    event_id = event_info['EventID']
    name = event_info['Name']
    location = event_info['Location']
    start_time = event_info['StartTime']
    end_time = event_info['EndTime']
    club_id = event_info['ClubID']
    poster_img = event_info['PosterImg']
    type = event_info['Type']

    query = 'INSERT INTO Events (Name, Location, StartTime, EndTime, ClubId, Type)'
    data = (name, location, start_time, end_time, club_id, type, event_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'event created!'





