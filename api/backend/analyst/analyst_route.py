from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict


analyst = Blueprint ('analyst', __name__)


@analyst.route('/analyst', methods = ['GET'])
def get_club_performance():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT
    c.ClubName,
    i.InterestName,
    et.EventType,
    COUNT(DISTINCT a.NUID) AS TotalAttendance
FROM Clubs c
JOIN Events e ON c.ClubId = e.ClubId
JOIN EventTypes et ON e.Type = et.EventTypeId
LEFT JOIN Attendance a ON e.EventID = a.EventID
LEFT JOIN AppealsTo ap ON c.ClubId = ap.ClubId
LEFT JOIN Interests i ON ap.InterestID = i.InterestID
GROUP BY c.ClubName, i.InterestName, et.EventType
ORDER BY et.EventType, TotalAttendance DESC;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

